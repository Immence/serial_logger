
from bridges.program_state_bridge import ProgramStateBridge
from components.data_containers.bath_reading import BathReading
from components.data_containers.device_reading import (DeviceReading,
                                                       QcDeviceReading)
from components.start_stop_button import StartStopButton
from components.success_indicator import SuccessIndicator
from global_values import COMMAND_QUEUE
from PySide6 import QtCore, QtGui, QtWidgets
from util.commands import Commands
from util.logger import Logger
from widgets.qc_mode.readings_widget_addon import QcReadingsWidget
from widgets.qc_mode.worst_reading_component import WorstReadingComponent
from widgets.views.options_view import QcOptionsLayout


class QcModeMainWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    logger : Logger

    run_button : StartStopButton
    success_indicator : SuccessIndicator
    device_readings_widget : QcReadingsWidget

    latest_bath_reading : BathReading = BathReading("23", "1.0352")

    pass_threshold: float = 0.001
    worst_reading: float = None
    worst_reading_deviance: float = 0
    target_reading_amount: int = None
    readings_done: int = 0

    # Program logic variables
    rerun = False
    program_ready = False
    program_running = False
    program_finished = False
    program_success = True
    
    recording_readings = False
    device_connection = False
    qr_code_set = False
    throw_reading = False

    running = QtCore.Signal(bool)
    success = QtCore.Signal(bool)
    ready = QtCore.Signal(bool)
    finished = QtCore.Signal(bool)

    def __init__(self, PSB: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)
        self.setContentsMargins(0, 10, 0, 0)

        #Communication bridges
        self._PSB = PSB
        self.logger = Logger(self._PSB)
           
        #Local state bridge connections
        # Main layout
        self.options = QcOptionsLayout(self)
        self.options.bath_temperature_change.connect(self.handle_bath_reading_temp_update)
        self.options.bath_sg_change.connect(self.handle_bath_reading_sg_update)
        self.options.bath_sg_change.connect(self.set_target_sg)
        self.options.reading_amount_change.connect(self.set_reading_amount)
        self.options.pass_threshold_change.connect(self.set_pass_threshold)
        self.options.force_start.clicked.connect(self.handle_force_start)
        self.options.set_default_values()

        run_status_layout = self.create_run_status_layout()

        ### READING LIST
        device_readings_layout = QtWidgets.QVBoxLayout()
        self.device_readings_widget = QcReadingsWidget()
        device_readings_title_bar = QtWidgets.QHBoxLayout()
        device_readings_title = QtWidgets.QLabel("Device readings")
        device_readings_reset_button = QtWidgets.QToolButton(self)
        device_readings_reset_button.clicked.connect(PSB.reset_readings)
        device_readings_reset_button.setText("Reset")
        device_readings_reset_button.setIcon(QtGui.QIcon.fromTheme("edit-undo"))
        device_readings_title_bar.addWidget(device_readings_title,alignment= QtCore.Qt.AlignHCenter)
        device_readings_title_bar.addWidget(device_readings_reset_button, alignment=QtCore.Qt.AlignRight)
        device_readings_layout.addLayout(device_readings_title_bar)
        device_readings_layout.addWidget(self.device_readings_widget)

        # Device readings signal
        self._PSB.reset_readings.connect(self.device_readings_widget.clear_readings)

        # Signals (need refactor)
        self._PSB.qr_code_set.connect(self.handle_qr_code_set)
        self._PSB.device_ready.connect(self.handle_device_ready)
        self._PSB.device_disconnected.connect(self.handle_device_disconnected)
        self._PSB.reading_received.connect(self.handle_reading_received)

        
        ### ADD LAYOUTS
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.options)
        main_layout.addLayout(run_status_layout)
        main_layout.addLayout(device_readings_layout, 1)
        self.setLayout(main_layout)
        self.check_program_ready()


    # Setters
    def set_target_sg(self, target_sg_str: str):
        try: 
            self.target_sg = float(target_sg_str.replace(",", "."))
            print("Target sg set: {}".format(self.target_sg))

        except Exception as e:
            self._PSB.emit_error(e)
            
        self.check_program_ready()

    def set_pass_threshold(self, pass_threshold_str: str):
        try: 
            self.pass_threshold = float(pass_threshold_str.replace(",", "."))
            print("Pass threshold set: {}".format(self.pass_threshold))

        except Exception as e:
            self._PSB.emit_error(e)
        self.check_program_ready()

    def set_reading_amount(self, reading_amount_str: str):
        try:
            self.target_reading_amount = int(reading_amount_str)
            print(f"Reading amount set: {self.target_reading_amount}")
        except Exception as e:
            self._PSB.emit_error(e)
        self.check_program_ready()

  

    
    def create_run_status_layout(self) -> QtWidgets.QVBoxLayout:
        #Big fancy button
        self.run_button = StartStopButton(self)
        self.run_button.setMinimumHeight(200)
        self.run_button.clicked.connect(self.handle_button_click)
        self.ready.connect(self.run_button.set_ready)
        self.running.connect(self.run_button.set_in_progress)
        self.finished.connect(self.run_button.set_finished)

        #Fancy indicator
        self.success_indicator = SuccessIndicator(self)
        self.running.connect(self.success_indicator.handle_progress_change)
        self.success.connect(self.success_indicator.handle_result)        
        self.ready.connect(self.success_indicator.handle_ready_change)
        self.finished.connect(self.success_indicator.handle_finish_change)

        #Worst reading thingy
        self.worst_reading_frame = WorstReadingComponent("Worst reading")
        
        #Final layout
        upper_layout = QtWidgets.QHBoxLayout()
        upper_layout.addWidget(self.run_button)
        upper_layout.addWidget(self.success_indicator, alignment=QtCore.Qt.AlignHCenter)
        run_status_layout = QtWidgets.QVBoxLayout()
        run_status_layout.addLayout(upper_layout)
        run_status_layout.addWidget(self.worst_reading_frame)
        
        return run_status_layout

    def set_program_ready(self, ready : bool):
        self.program_ready = ready
        self.ready.emit(self.program_ready)

    def set_program_running(self, program_running : bool):
        self.program_running = program_running
        self.running.emit(self.program_running)

    def set_program_success(self, success : bool):
        self.program_success = success
        self.success.emit(self.program_success)

    def set_program_finished(self, program_finished : bool):
        if program_finished:
            self.set_program_running(False)
        self.program_finished = program_finished
        self.finished.emit(self.program_finished)

    def start_device_idle(self):
        COMMAND_QUEUE.put(Commands.get_freq_run())

    def handle_device_ready(self):
        self.device_connection = True
        self.start_device_idle()
        self.check_program_ready()

    def handle_device_disconnected(self):
        self.device_connection = False
        self.qr_code_set = False
        self.reset_vars()
        self.check_program_ready()

    def handle_qr_code_set(self):
        self.qr_code_set = True
        self.check_program_ready()

    def check_program_ready(self):
        ready = self.latest_bath_reading.validate() and self.qr_code_set and self.pass_threshold and self.target_reading_amount and self.device_connection
        self.set_program_ready(ready)
    
    def handle_button_click(self):
        if self.program_finished:
            self.set_program_running(True)
            self.reset_vars()
            self.handle_program_start()
        else:
            COMMAND_QUEUE.put(Commands.get_freq_stop())
            self.throw_reading = True
            self.set_program_running(not self.program_running)

    def handle_force_start(self):
        if self.program_running:
            return
        # self.recording_readings = False
        self.throw_reading = False
        self.handle_program_start()

    def handle_program_start(self):
        self.worst_reading = None
        self.worst_reading_deviance = 0
        self.readings_done = 0
        
        # if not self.recording_readings:
        self.reset_vars()
            # self.recording_readings = True
        self.set_program_running(True)
        COMMAND_QUEUE.put(Commands().get_freq_read_n(self.target_reading_amount-1))
        # reading = DeviceReading(str(1337.75610),str(24.12),str(1339.41916),str(1.034))
        # self._PSB.reading_received.emit(reading)

    def handle_program_stop(self):
        self.set_program_running(False)
        self.reset_vars()
        # self.recording_readings = False

    def handle_program_finish(self):
        # self.recording_readings = False
        self.set_program_running(False)
        self.set_program_finished(True)

    # Logic shit
    def check_reading(self, qc_reading: QcDeviceReading):

        if float(qc_reading.sg) == 0:
            self.set_program_success(False)
            self.worst_reading = 0
            self.worst_reading_deviance = -self.target_sg
            self.worst_reading_frame.update_reading(qc_reading)

        else:
            deviance = qc_reading.deviance()
            if abs(deviance) > self.pass_threshold:
                self.set_program_success(False)
            
            if abs(deviance) > abs(self.worst_reading_deviance):
                self.worst_reading =  float(qc_reading.sg)
                self.worst_reading_deviance = deviance
                self.worst_reading_frame.update_reading(qc_reading)

    def handle_reading_received(self, reading : DeviceReading):
        qc_reading = QcDeviceReading(**reading.to_dict(), target_sg=self.latest_bath_reading.sg, pass_threshold = self.pass_threshold)
        
        # The fork usually sends an extra reading whenever it receives a command to stop. We want to throw this away.
        if self.throw_reading:
            # self.recording_readings = False
            self.throw_reading = False
            if self.program_running:
                self.handle_program_start()
                return
            else:
                self.handle_program_stop()
                return
            
        if self.program_running:
            self.check_reading(qc_reading)
            self.device_readings_widget.add_reading(qc_reading)
            self.readings_done += 1
            self.logger.write_to_csv(qc_reading.to_dict(), self.latest_bath_reading.to_dict())
            if self.readings_done >= self.target_reading_amount:
                self.handle_program_finish()
        
        else:
            self.device_readings_widget.add_reading(qc_reading)

    def handle_bath_reading_temp_update(self, temperature : str):
        self.latest_bath_reading = BathReading(temperature, self.latest_bath_reading.sg)
        self.check_program_ready()

    def handle_bath_reading_sg_update(self, sg : str):
        self.latest_bath_reading = BathReading(self.latest_bath_reading.temperature, sg)
        self.check_program_ready()

    def reset_vars(self):
        self._PSB.reset_readings.emit()
        self.device_readings_widget.clear_readings()
        self.worst_reading_frame.reset_reading()

        self.worst_reading = None
        self.worst_reading_deviance = 0
        self.readings_done = 0

        # self.recording_readings = False
        self.set_program_running(False)
        self.set_program_finished(False)
        self.set_program_success(True)
