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

        self.add_reading(
            {
                "Frequency": "1357.28577",
                "Temperature": "21.93",
                "Compensated": "1600.6000",
                "SG": "1.07897",
            })
        self.add_reading(
            {
                "Frequency": "1357.28577",
                "Temperature": "21.93",
                "Compensated": "1600.6000",
                "SG": "1.07897",
            })
        self.add_reading(
            {
                "Frequency": "1357.28577",
                "Temperature": "21.93",
                "Compensated": "1600.6000",
                "SG": "1.07897",
            })
        self.add_reading(
            {
                "Frequency": "1357.28577",
                "Temperature": "21.93",
                "Compensated": "1600.6000",
                "SG": "1.07897",
            })
        self.add_reading(
            {
                "Frequency": "1357.28577",
                "Temperature": "21.93",
                "Compensated": "1600.6000",
                "SG": "1.07897",
            })

    def reset_list(self):
        self.readings.clear()

    def add_reading(self, reading: dict):
        self.readings.append(ReadingComponent(reading["Frequency"], reading["Temperature"], reading["Compensated"], reading["SG"], len(self.readings)))
        self.list_layout.addWidget(self.readings[len(self.readings)-1])