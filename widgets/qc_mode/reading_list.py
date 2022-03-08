from PySide6 import QtWidgets
from typing import List

from components.reading_component import ReadingComponent

class ReadingList(QtWidgets.QWidget):
    
    readings: List[ReadingComponent]

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.readings = []
        self.list_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.list_layout)

    def reset_readings(self):
        self.readings.clear()
        for i in reversed(range(self.list_layout.count())): 
            self.list_layout.itemAt(i).widget().setParent(None)

    def add_reading(self, reading: dict):
        self.readings.append(ReadingComponent(reading["frequency"], reading["temperature"], reading["compensated"], reading["sg"], len(self.readings)+1))
        self.list_layout.addWidget(self.readings[len(self.readings)-1])
        