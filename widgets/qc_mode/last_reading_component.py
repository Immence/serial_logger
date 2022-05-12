from components.data_containers.device_reading import DeviceReading
from components.reading_component import ReadingComponent
from PySide6 import QtWidgets


class SingleReadingComponent(QtWidgets.QWidget):
    
    reading: ReadingComponent

    def __init__(self, title = "SINGLE READING - Title not set"):
        QtWidgets.QWidget.__init__(self)
        self.reading = ReadingComponent(None, None, None, None)
        self.reading_layout = QtWidgets.QVBoxLayout()
        self.title = QtWidgets.QLabel(title)
        self.reading_layout.addWidget(self.title)
        self.reading_layout.addWidget(self.reading)
        self.setLayout(self.reading_layout)

    def reset_reading(self):
        self.layout().removeWidget(self.reading)
        self.reading.setParent(None)
        self.reading = ReadingComponent(None, None, None, None)
        self.layout().addWidget(self.reading)
    def update_reading(self, reading: DeviceReading):
        self.layout().removeWidget(self.reading)
        self.reading.setParent(None)
        self.reading = ReadingComponent(reading.frequency, reading.temperature, reading.compensated, reading.sg)
        self.layout().addWidget(self.reading)
