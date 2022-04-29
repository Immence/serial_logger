from PySide6 import QtWidgets, QtCore
from bridges.program_state_bridge import ProgramStateBridge

from widgets.readings_widget.readings_widget import ReadingsWidget

class CentralWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    
    readings_widget : ReadingsWidget
    
    def __init__(self, PSB : ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        self._PSB = PSB 

        self.readings_widget = ReadingsWidget()
        self._PSB.reading_received.connect(self.readings_widget.add_reading)
        self._PSB.clear_reading_list.connect(self.readings_widget.clear_readings)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.readings_widget)
        self.setLayout(layout)
