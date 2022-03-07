from PySide6 import QtWidgets
from bridges.program_state_bridge import ProgramStateBridge
from components.field_with_title import FieldWithTitle
from widgets.qc_mode.local_state_bridge import LocalStateBridge
from widgets.qc_mode.top_dock_widget import TopDockWidget

class QcModeMainWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    _LSB: LocalStateBridge

    target_sg: float = 0
    pass_threshold: float = 0

    def __init__(self, PSB: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        #Communication bridges
        self._PSB = PSB
        self._LSB = LocalStateBridge()
        # Central dock widget fields
        self.qr_code_frame = FieldWithTitle("QR code")
        self.target_sg_frame = FieldWithTitle("Target SG")
        self.pass_threshold_frame = FieldWithTitle("Pass threshold")
        self.reading_amount_frame = FieldWithTitle("Amount of readings")
        #Program state bridge connections
        self._PSB.qr_code_set.connect(self.qr_code_frame.set_text)
        #Local state bridge connections
        self._LSB.reading_amount_set.connect(self.set_reading_amount)
        self._LSB.target_sg_set.connect(self.set_target_sg)
        self._LSB.pass_threshold_set.connect(self.set_pass_threshold)
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.qr_code_frame)
        layout.addWidget(self.reading_amount_frame)
        layout.addWidget(self.target_sg_frame)
        layout.addWidget(self.pass_threshold_frame)
        self.setLayout(layout)

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

    # This is for the main widget.
    def get_top_dock_widget(self) -> QtWidgets.QWidget:
        return TopDockWidget(self._LSB)