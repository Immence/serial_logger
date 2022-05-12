from PySide6 import QtWidgets, QtCore
from bridges.local_state_bridge import LocalStateBridge
from bridges.program_state_bridge import ProgramStateBridge
from components.text_widgets import ToggleTextEditWithTitle

class OptionsLayout(QtWidgets.QFrame):

    bath_temperature : ToggleTextEditWithTitle
    bath_sg : ToggleTextEditWithTitle    

    bath_temperature_change = QtCore.Signal(str)
    bath_sg_change = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        self.layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel("Optional settings")
        self.bath_temperature = ToggleTextEditWithTitle(self, "Bath temperature")
        self.bath_temperature.set_text_width_max(70)
        self.bath_temperature.emit_text_change.connect(self.bath_temperature_change)
        self.bath_sg = ToggleTextEditWithTitle(self, "Bath SG")
        self.bath_sg.set_text_width_max(70)
        self.bath_sg.emit_text_change.connect(self.bath_sg_change)
        
        self.setMaximumHeight(250)
        self.setMaximumWidth(250)
        self.layout.addWidget(title_label)
        self.layout.addWidget(self.bath_temperature)
        self.layout.addWidget(self.bath_sg)

        self.setLayout(self.layout)
