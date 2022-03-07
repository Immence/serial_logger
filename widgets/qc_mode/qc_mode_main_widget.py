from PySide6 import QtWidgets, QtGui
from bridges.program_state_bridge import ProgramStateBridge
from components.field_with_title import FieldWithTitle
from widgets.qc_mode.local_state_bridge import LocalStateBridge
from widgets.qc_mode.top_dock_widget import TopDockWidget

from  widgets.qc_mode.reading_list import ReadingList


class QcModeMainWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    _LSB: LocalStateBridge

    target_sg: float = 0
    pass_threshold: float = 0.001
    worst_reading: float = 0
    worst_reading_deviance: float = 0


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
        self._PSB.reading_received.connect(self._PSB.reading_received)
        reading_list_layout.addWidget(self.reading_list)
        
        ### ADD LAYOUTS
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(status_text_layout)
        main_layout.addLayout(run_status_layout)
        main_layout.addLayout(reading_list_layout)
        self.setLayout(main_layout)

    # Setters
    def set_target_sg(self, target_sg_str: str):
        try: 
            self.target_sg = float(target_sg_str.replace(",", "."))
            self.target_sg_frame.set_text(self.target_sg)
            print("Target sg set: {}".format(self.target_sg))

        except Exception as e:
            print(e)

    def set_pass_threshold(self, pass_threshold_str: str):
        try: 
            self.pass_threshold = float(pass_threshold_str.replace(",", "."))
            self.pass_threshold_frame.set_text(self.pass_threshold)
            print("Pass threshold set: {}".format(self.pass_threshold))

        except Exception as e:
            print(e)

    def set_reading_amount(self, reading_amount_str: str):
        try:
            self.reading_amount = int(reading_amount_str)
            self.reading_amount_frame.set_text(self.reading_amount)
            print(f"Reading amount set: {self.reading_amount}")
        except Exception as e:
            print(e)

    # Logic shit
    def check_reading(self, reading: dict):
        deviance = abs(self.target_sg-reading["SG"])
        if deviance > self.pass_threshold:
            print("FAIL")
        
        if deviance > self.worst_reading_deviance:
            self.worst_reading =  reading["SG"]
            self.worst_reading_deviance = deviance
        
            
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

        return status_text_layout
    
    def create_run_status_layout(self) -> QtWidgets.QVBoxLayout:
        self.run_status_frame = QtWidgets.QLabel("RUNNING")
        super_special_font = QtGui.QFont("Helvetica", pointSize=28, weight = QtGui.QFont.Bold)
        self.run_status_frame.setFont(super_special_font)
        self.run_status_frame.setMaximumHeight(200)
        self.worst_reading_frame = FieldWithTitle("Worst reading")

        run_status_layout = QtWidgets.QVBoxLayout()
        run_status_layout.addWidget(self.run_status_frame)
        run_status_layout.addWidget(self.worst_reading_frame)

        return run_status_layout

