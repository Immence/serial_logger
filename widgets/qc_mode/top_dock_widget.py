from PySide6 import QtWidgets

from components.input_with_title import InputWithTitle
from widgets.qc_mode.local_state_bridge import LocalStateBridge

class TopDockWidget(QtWidgets.QWidget):
    _LSB: LocalStateBridge

    target_input_frame: InputWithTitle
    threshold_input_frame: InputWithTitle

    def __init__(self, LSB: LocalStateBridge):
        QtWidgets.QWidget.__init__(self)

        self._LSB = LSB

        self.target_input_frame = InputWithTitle("Target SG")
        self.target_input_frame.emit_input.connect(self._LSB.target_sg_set)
        
        self.threshold_input_frame = InputWithTitle("Pass threshold")
        self.threshold_input_frame.emit_input.connect(self._LSB.pass_threshold_set)

        self.reading_amount_frame = InputWithTitle("Amount of readings")
        self.reading_amount_frame.emit_input.connect(self._LSB.reading_amount_set)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.target_input_frame)
        layout.addWidget(self.threshold_input_frame)
        self.setLayout(layout)
        