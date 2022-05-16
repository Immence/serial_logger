from components.data_containers.device_reading import QcDeviceReading
from components.reading_component import QcReadingComponent
from PySide6 import QtCore, QtWidgets


class WorstReadingComponent(QtWidgets.QWidget):
    
    reading: QcReadingComponent

    def __init__(self, title = "SINGLE READING - Title not set"):
        QtWidgets.QWidget.__init__(self)
        self.reading = QcReadingComponent(self)
        self.layout = QtWidgets.QVBoxLayout()
        component_title = QtWidgets.QLabel(title)
        component_title.setObjectName("title")
        self.titles_layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(component_title, alignment = QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.reading, 1, alignment=QtCore.Qt.AlignVCenter)
        self.setLayout(self.layout)

    def reset_reading(self):
        self.reading.clear()
        
    def update_reading(self, reading: QcDeviceReading):
        self.reading.set_data(reading)
