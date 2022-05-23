from datetime import datetime

import util.middlewares as Middlewares
import util.validators as Validators
from bridges.program_state_bridge import ProgramStateBridge
from components.text_widgets import ToggleTextEditWithTitle
from PySide6 import QtCore, QtWidgets


class TextVariableView(QtWidgets.QWidget):

    qr_code : ToggleTextEditWithTitle
    file_name : ToggleTextEditWithTitle

    qr_code_change = QtCore.Signal(str)
    file_name_change = QtCore.Signal(str)
    reading_amount_change = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
    
        self.layout = QtWidgets.QVBoxLayout()
        self.setMinimumWidth(320)
        self.qr_code = ToggleTextEditWithTitle(self, "QR code", Middlewares.replace_plus_signs, Validators.validate_qr_code)
        self.qr_code.emit_text_change.connect(self.qr_code_change)
        self.file_name = ToggleTextEditWithTitle(self, "Target file name")
        self.file_name.emit_text_change.connect(self.file_name_change)

        self.layout.addWidget(self.qr_code)
        self.layout.addWidget(self.file_name)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def start(self):
        self.file_name.set_default_text(datetime.now().strftime("%Y-%m-%d.csv"))

    def clear(self):
        self.qr_code.clear()

    def connect_signals(self, PSB : ProgramStateBridge):
        PSB.device_disconnected.connect(self.clear)
        PSB.qr_code_received.connect(self.qr_code.set_text)
        PSB.request_file_name.connect(self.file_name.get_text)
        self.qr_code_change.connect(PSB.qr_code_set)
        self.file_name_change.connect(PSB.file_name_set)
        self.start()
