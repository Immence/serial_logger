from dataclasses import Field
from PySide6 import QtCore, QtGui, QtWidgets
from bridges.program_state_bridge import ProgramStateBridge
from components.field_with_title import FieldWithTitle
from widgets.qc_mode.local_state_bridge import LocalStateBridge
from widgets.qc_mode.top_dock_widget import TopDockWidget

from typing import List

class QcModeMainWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    _LSB: LocalStateBridge

    target_sg: float = 0
    pass_threshold: float = 0

    def __init__(self, PSB: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        self._PSB = PSB
        self._LSB = LocalStateBridge()
        # Central dock widget fields
        self.qr_code_frame = FieldWithTitle("QR code")
        self.target_sg_frame = FieldWithTitle("Target SG")
        self.pass_threshold_frame = FieldWithTitle("Pass threshold")
        #Program state bridge connections
        self._PSB.qr_code_set.connect(self.qr_code_frame.set_text)
        #Local state bridge connections
        self._LSB.target_sg_set.connect(self.set_target_sg)
        self._LSB.pass_threshold_set.connect(self.set_pass_threshold)
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.qr_code_frame)
        layout.addWidget(self.target_sg_frame)
        layout.addWidget(self.pass_threshold_frame)
        self.setLayout(layout)

    def set_target_sg(self, target_sg_str: str):
        print("Input:", target_sg_str)
        print("Target sg pre:", self.target_sg)

        try: 
            self.target_sg = float(target_sg_str.replace(",", "."))
            self.target_sg_frame.set_text(self.target_sg)
            print("Target sg post:", self.target_sg)

        except Exception as e:
            print(e)

    def set_pass_threshold(self, pass_threshold_str: str):
        print("Input:", pass_threshold_str)
        print("Target sg pre:", self.pass_threshold)

        try: 
            self.pass_threshold = float(pass_threshold_str.replace(",", "."))
            self.pass_threshold_frame.set_text(self.pass_threshold)
            print("Target sg post:", self.pass_threshold)

        except Exception as e:
            print(e)

    def get_top_dock_widget(self) -> QtWidgets.QWidget:
        return TopDockWidget(self._LSB)