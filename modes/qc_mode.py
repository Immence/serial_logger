from PySide6 import QtCore, QtGui, QtWidgets

from widgets.qc_mode.qc_mode_main_widget import QcModeMainWidget
from bridges.program_state_bridge import ProgramStateBridge

class QcMode(QtWidgets.QWidget):

    PSB : ProgramStateBridge
    def __init__(self, psb: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)
        
        self.PSB = psb

        central_widget = QcModeMainWidget(self.PSB)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(central_widget)
        self.setLayout(layout)
