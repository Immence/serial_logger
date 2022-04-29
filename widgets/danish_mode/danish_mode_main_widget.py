from PySide6 import QtWidgets, QtGui
from widgets.danish_mode.local_state_bridge import LocalStateBridge
from bridges.program_state_bridge import ProgramStateBridge

class DanishModeMainWidget(QtWidgets.QWidget):
    _PSB: ProgramStateBridge
    _LSB: LocalStateBridge

    def __init__(self, PSB: ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        #Communication bridges
        self._PSB = PSB
        self._LSB = LocalStateBridge()

        #Program state bridge connections
        ####

        #Local state bridge connections
        ####

        #Layouts
        main_layout = QtWidgets.QHBoxLayout()
        