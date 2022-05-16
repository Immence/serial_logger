from files.res.font_styles import Fonts
from PySide6 import QtGui, QtWidgets

from components.data_containers.device_reading import QcDeviceReading


class QcReadingComponent(QtWidgets.QWidget):
    
    reading : QcDeviceReading
    freq_label : QtWidgets.QLabel
    temp_label : QtWidgets.QLabel
    sg_label : QtWidgets.QLabel
    deviance_label : QtWidgets.QLabel

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.freq_label = QtWidgets.QLabel(self, objectName="title")
        self.temp_label = QtWidgets.QLabel(self, objectName="title")
        self.sg_label = QtWidgets.QLabel(self, objectName="title")
        self.deviance_label = QtWidgets.QLabel(self, objectName="title")
        
        self.layout = QtWidgets.QVBoxLayout()
        
        title_layout = QtWidgets.QHBoxLayout()
        value_layout = QtWidgets.QHBoxLayout()
        frequency_unit = QtWidgets.QLabel("Hz", objectName="body")
        temperature_unit = QtWidgets.QLabel(u"\N{DEGREE SIGN}C", objectName="body")
        gravity_unit = QtWidgets.QLabel("SG", objectName="body")
        deviance_unit = QtWidgets.QLabel("Deviance SG", objectName="body")   

        title_layout.addWidget(frequency_unit, 1)
        title_layout.addWidget(temperature_unit, 1)
        title_layout.addWidget(gravity_unit, 1)
        title_layout.addWidget(deviance_unit)

        value_layout.addWidget(self.freq_label,1)
        value_layout.addWidget(self.temp_label,1)
        value_layout.addWidget(self.sg_label, 1)
        value_layout.addWidget(self.deviance_label)
        self.layout.addLayout(title_layout, 1)
        self.layout.addLayout(value_layout, 1)
        self.setLayout(self.layout)

    def clear(self):
        self.reading = None
        self.freq_label.clear()
        self.temp_label.clear()
        self.sg_label.clear()
        self.deviance_label.clear()
        
    def set_data(self, reading : QcDeviceReading):
        self.reading = reading
        self.freq_label.setText(reading.frequency)
        self.temp_label.setText(reading.temperature)
        self.sg_label.setText(reading.sg)
        self.deviance_label.setText("{:e}".format(reading.deviance()))
    

    

