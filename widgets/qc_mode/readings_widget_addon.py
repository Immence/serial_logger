from PySide6 import QtWidgets, QtCore
from typing import List
from bridges.local_state_bridge import LocalStateBridge
from components.data_containers.device_reading import DeviceReading

from widgets.qc_mode.reading_list_addon import QcReadingList
from widgets.device_readings_widget.stability_widget import StabilityComponent
import numpy as np
from widgets.device_readings_widget.reading_list import ReadingList

class DeviceReadingsWidget(QtWidgets.QWidget):
    
    readings: List[DeviceReading]
    temperature_stability_widget : StabilityComponent
    frequency_stability_widget : StabilityComponent

    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        
        self.readings = []
        self.temperature_stability_widget = StabilityComponent("Temperature")
        self.frequency_stability_widget = StabilityComponent("Frequency")
        stability_layout = QtWidgets.QHBoxLayout()
        self.layout = QtWidgets.QVBoxLayout()
        self.reading_list = ReadingList()
        stability_layout.addWidget(self.temperature_stability_widget, alignment = QtCore.Qt.AlignLeft)
        stability_layout.addWidget(self.frequency_stability_widget, alignment = QtCore.Qt.AlignRight)
        self.layout.addLayout(stability_layout)

    def start(self):
        self.layout.addWidget(self.reading_list)
        self.setLayout(self.layout)

    def clear_readings(self):
        self.readings.clear()
        self.reading_list.clear_data()
        self.temperature_stability_widget.clear_data()
        self.frequency_stability_widget.clear_data()


    def add_reading(self, reading: DeviceReading):
        self.readings.append(reading)
        if len(self.readings) > 10:
            self.readings.pop(0)
        self.update_temp_stats()
        self.update_freq_stats()
        self.reading_list.update_data(self.readings)

    def update_temp_stats(self):
        temperatures = [ float(reading.temperature) for reading in self.readings ]
        temp_avg = np.round(np.average(temperatures), 2)
        temp_std = np.round(np.std(temperatures), 2)
        self.temperature_stability_widget.update_status(str(temp_avg), str(temp_std))

    def update_freq_stats(self):
        frequencies = [ float(reading.frequency) for reading in self.readings ]
        freq_avg = np.round(np.average(frequencies), 2)
        freq_std = np.round(np.std(frequencies), 2)
        self.frequency_stability_widget.update_status(str(freq_avg), str(freq_std))

class QcReadingsWidget(DeviceReadingsWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.reading_list = QcReadingList()
        self.setMaximumWidth(400)
        self.start()

    def add_reading(self, reading : DeviceReading):
        print("Overridden add_reading function")
        super().add_reading(reading)