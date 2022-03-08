from lib2to3.pgen2.token import COMMA
from PySide6 import QtWidgets, QtGui
from bridges.program_state_bridge import ProgramStateBridge
from components.field_with_title import FieldWithTitle
from widgets.qc_mode.last_reading_component import SingleReadingComponent
from widgets.qc_mode.local_state_bridge import LocalStateBridge
from widgets.qc_mode.top_dock_widget import TopDockWidget

from  widgets.qc_mode.reading_list import ReadingList

from util.commands import Commands
from global_values import COMMAND_QUEUE

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

        #Communication bridges
        self._PSB = PSB
        self._LSB = LocalStateBridge()
    
        #Program state bridge connections
       
        #Local state bridge connections
        self._LSB.reading_amount_set.connect(self.set_reading_amount)
        self._LSB.target_sg_set.connect(self.set_target_sg)
        self._LSB.pass_threshold_set.connect(self.set_pass_threshold)
        # Main layout
        status_text_layout = self.create_status_text_layout()
        run_status_layout = self.create_run_status_layout()
        reading_list_layout = QtWidgets.QVBoxLayout()
        ### READING LIST
        self.reading_list = ReadingList()
        self._PSB.qr_code_set.connect(self.handle_qr_code_set)
        self._PSB.connected.connect(self.handle_device_disconnected)
        self._PSB.disconnected.connect(self.handle_device_disconnected)
        self._PSB.connection_ready.connect(self.handle_device_ready)
        self._PSB.reading_received.connect(self.handle_reading_received)
        self._LSB.start_reading.connect(self.handle_program_start)
        reading_list_layout.addWidget(self.reading_list)
        
        ### ADD LAYOUTS
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(status_text_layout)
        main_layout.addLayout(run_status_layout)
        main_layout.addLayout(reading_list_layout)
        self.setLayout(main_layout)
        self.check_program_ready()


    # Setters
    def set_target_sg(self, target_sg_str: str):
        try: 
            self.target_sg = float(target_sg_str.replace(",", "."))
            self.target_sg_frame.set_text(self.target_sg)
            print("Target sg set: {}".format(self.target_sg))

        except Exception as e:
            print(e)
        self.check_program_ready()

    def set_pass_threshold(self, pass_threshold_str: str):
        try: 
            self.pass_threshold = float(pass_threshold_str.replace(",", "."))
            self.pass_threshold_frame.set_text(self.pass_threshold)
            print("Pass threshold set: {}".format(self.pass_threshold))

        except Exception as e:
            print(e)
        self.check_program_ready()

    def set_reading_amount(self, reading_amount_str: str):
        try:
            self.target_reading_amount = int(reading_amount_str)
            self.reading_amount_frame.set_text(self.target_reading_amount)
            print(f"Reading amount set: {self.target_reading_amount}")
        except Exception as e:
            print(e)
        self.check_program_ready()

    # Logic shit
    def check_reading(self, reading: dict):
        if float(reading["sg"]) == 0:
            self.status = False
            self.worst_reading = 0
            self.worst_reading_deviance = -self.target_sg
            self.worst_reading_frame.update_reading(reading)

        else:
            deviance = self.target_sg-float(reading["sg"])

            if abs(deviance) > self.pass_threshold:
                self.status = False
            
            if abs(deviance) > abs(self.worst_reading_deviance):
                self.worst_reading =  float(reading["sg"])
                self.worst_reading_deviance = round(deviance, 6)
                self.worst_reading_deviance_frame.set_text(self.worst_reading_deviance)
                self.worst_reading_frame.update_reading(reading)
            
    # This is for the main widget.
    def get_top_dock_widget(self) -> QtWidgets.QWidget:
        return TopDockWidget(self._LSB)

    #   Creating shit
    def create_status_text_layout(self) -> QtWidgets.QHBoxLayout:
        self.qr_code_frame = FieldWithTitle("QR code")
        self.target_sg_frame = FieldWithTitle("Target SG")
        self.pass_threshold_frame = FieldWithTitle("Pass threshold")
        self.reading_amount_frame = FieldWithTitle("Amount of readings")

        self._PSB.qr_code_set.connect(self.qr_code_frame.set_text)

        status_text_layout = QtWidgets.QVBoxLayout()
        status_text_layout.addWidget(self.qr_code_frame)
        status_text_layout.addWidget(self.reading_amount_frame)
        status_text_layout.addWidget(self.target_sg_frame)
        status_text_layout.addWidget(self.pass_threshold_frame)
        
        if self.target_reading_amount: self.reading_amount_frame.set_text(self.target_reading_amount)
        if self.pass_threshold: self.pass_threshold_frame.set_text(self.pass_threshold)
        if self.target_sg: self.target_sg_frame.set_text(self.target_sg)

        return status_text_layout
    
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

    def handle_device_ready(self):
        self.device_connection = True
        self.run_status_frame.setText("Getting QR-code..")
        COMMAND_QUEUE.put(Commands().get_identity())
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
            self.reading_list.reset_readings()
            COMMAND_QUEUE.put(Commands().get_freq_run())
        self.running = True
        self.run_status_frame.setText("Running..")

    def handle_reading_received(self, reading: dict):
        if self.running:
            self.check_reading(reading)
            self.reading_list.add_reading(reading)
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
        if not self.rerun:
            self.qr_code_frame.set_text("Not set")
        self.reading_list.reset_readings()
        self.worst_reading_frame.reset_reading()
        self.latest_reading_frame.reset_reading()

        self.worst_reading = None
        self.worst_reading_deviance = 0
        self.worst_reading_deviance_frame.set_text(self.worst_reading_deviance)
        self.readings_done = 0

        self.receiving_readings = False
        self.status = True