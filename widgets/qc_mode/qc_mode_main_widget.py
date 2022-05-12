from datetime import datetime

from bridges.program_state_bridge import ProgramStateBridge
from components.field_with_title import FieldWithTitle
from global_values import COMMAND_QUEUE
from PySide6 import QtCore, QtGui, QtWidgets
from util.commands import Commands
from widgets.qc_mode.last_reading_component import SingleReadingComponent
from widgets.qc_mode.local_state_bridge import LocalStateBridge
from widgets.qc_mode.readings_widget_addon import QcReadingsWidget
from widgets.views.options_view import QcOptionsLayout

QC_OUTPUT_FOLDER = "output_qc"

class QcModeMainWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    _LSB: LocalStateBridge

    target_sg: float = None
    pass_threshold: float = 0.001
    worst_reading: float = None
    worst_reading_deviance: float = 0
    target_reading_amount: int = 5
    readings_done: int = 0

    rerun = False
    running = False
    receiving_readings = False
    device_connection = False
    program_ready = False
    status = True


    def __init__(self, PSB: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)
        self.setContentsMargins(0, 10, 0, 0)

        #Communication bridges
        self._PSB = PSB
        self._LSB = LocalStateBridge()
    
        #Program state bridge connections
        self._PSB.bath_sg_set.connect(self.set_target_sg)
       
        #Local state bridge connections
        # Main layout
        self.options = QcOptionsLayout(self)
        self.options.bath_temperature_change.connect(self._PSB.bath_temperature_set)
        self.options.bath_sg_change.connect(self._PSB.bath_sg_set)
        self.options.bath_sg_change.connect(self.set_target_sg)
        self.options.reading_amount_change.connect(self.set_reading_amount)
        self.options.target_sg_change.connect(self.set_target_sg)
        self.options.pass_threshold_change.connect(self.set_pass_threshold)

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
        self._PSB.reading_received.connect(self.device_readings_widget.add_reading)
        self._PSB.reset_readings.connect(self.device_readings_widget.clear_readings)

        # Signals (need refactor)
        self._PSB.qr_code_set.connect(self.handle_qr_code_set)
        self._PSB.device_connected.connect(self.handle_device_disconnected)
        self._PSB.device_disconnected.connect(self.handle_device_disconnected)
        # self._PSB.device_ready.connect(self.handle_device_ready)
        self._PSB.reading_received.connect(self.handle_reading_received)
        self._LSB.start_reading.connect(self.handle_program_start)

        
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

    # Logic shit
    def check_reading(self, reading: dict):
        reading["target_sg"] = self.target_sg
        reading["accepted_deviance"] = self.pass_threshold

        if float(reading["sg"]) == 0:
            self.status = False
            self.worst_reading = 0
            self.worst_reading_deviance = -self.target_sg
            reading["deviance"] = self.worst_reading_deviance
            self.worst_reading_frame.update_reading(reading)

        else:
            deviance = round(self.target_sg-float(reading["sg"]), 6)
            reading["deviance"] = deviance
            if abs(deviance) > self.pass_threshold:
                self.status = False
            
            if abs(deviance) > abs(self.worst_reading_deviance):
                self.worst_reading =  float(reading["sg"])
                self.worst_reading_deviance = deviance
                self.worst_reading_deviance_frame.set_text(self.worst_reading_deviance)
                self.worst_reading_frame.update_reading(reading)

    
    def create_run_status_layout(self) -> QtWidgets.QVBoxLayout:
        self.run_status_frame = QtWidgets.QLabel("")
        super_special_font = QtGui.QFont("Helvetica", pointSize=28, weight = QtGui.QFont.Bold)
        self.run_status_frame.setFont(super_special_font)
        self.run_status_frame.setMaximumHeight(200)
        self.worst_reading_frame = SingleReadingComponent("Worst reading")
        self.worst_reading_deviance_frame = FieldWithTitle("Deviance")
        self.latest_reading_frame = SingleReadingComponent("Latest reading")
        self._PSB.reading_received.connect(self.latest_reading_frame.update_reading)
        run_status_layout = QtWidgets.QVBoxLayout()
        run_status_layout.addWidget(self.run_status_frame)
        run_status_layout.addWidget(self.worst_reading_frame)
        run_status_layout.addWidget(self.worst_reading_deviance_frame)
        run_status_layout.addWidget(self.latest_reading_frame)

        return run_status_layout

    def handle_device_disconnected(self):
        self.device_connection = False
        self.rerun = False
        self.running = False
        self.run_status_frame.setText("Disconnected")
        self.reset_vars()
        self.check_program_ready()

    def handle_qr_code_set(self):
        self.run_status_frame.setText("Waiting for other variables to be set")
        COMMAND_QUEUE.put(Commands().get_freq_run())
        self.receiving_readings = True
        self.rerun = True
        self.check_program_ready()

    def check_program_ready(self):
        self.program_ready = self.target_sg and self.pass_threshold and self.target_reading_amount and self.device_connection
        self._LSB.program_ready.emit(self.program_ready)
        if self.program_ready:
            self.run_status_frame.setText("Ready")
    
    def handle_program_start(self):
        self.worst_reading = None
        self.worst_reading_deviance = 0
        self.readings_done = 0
        if not self.receiving_readings:
            self.reset_vars()
            self._PSB.reset_readings.emit()
            COMMAND_QUEUE.put(Commands().get_freq_run())
        self.running = True
        self.run_status_frame.setText("Running..")

    def handle_reading_received(self, reading: dict):
        if self.running:
            self.check_reading(reading)
            self.readings_done += 1
            if self.readings_done >= self.target_reading_amount:
                COMMAND_QUEUE.put(Commands().get_freq_stop())
                self.receiving_readings = False
            
                if self.status:
                    self.run_status_frame.setText(f"Finished - Success!")
                elif not self.status:
                    self.run_status_frame.setText(f"Finished - YOU FAIL!")
        

    def reset_vars(self):
        self.running = False
        self._PSB.reset_readings.emit()
        self.worst_reading_frame.reset_reading()
        self.latest_reading_frame.reset_reading()

        self.worst_reading = None
        self.worst_reading_deviance = 0
        self.worst_reading_deviance_frame.set_text(self.worst_reading_deviance)
        self.readings_done = 0

        self.receiving_readings = False
        self.status = True
