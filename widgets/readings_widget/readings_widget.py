from PySide6 import QtWidgets
from typing import List
from components.data_containers.reading import Reading

from widgets.readings_widget.reading_list import ReadingList
from widgets.readings_widget.stability_widget import StabilityComponent
import numpy as np
from widgets.readings_widget.reading_list import ReadingList

class ReadingsWidget(QtWidgets.QWidget):
    
    readings: List[Reading]
    temperature_stability_widget : StabilityComponent
    frequency_stability_widget : StabilityComponent

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.readings = []
        self.temperature_stability_widget = StabilityComponent("Temperature")
        self.frequency_stability_widget = StabilityComponent("Frequency")
        stability_layout = QtWidgets.QHBoxLayout()
        layout = QtWidgets.QVBoxLayout()
        self.reading_list = ReadingList()
        self.reading_list.setMaximumWidth(400)
        self.setMaximumWidth(400)
        stability_layout.addWidget(self.temperature_stability_widget)
        stability_layout.addWidget(self.frequency_stability_widget)
        layout.addLayout(stability_layout)
        layout.addWidget(self.reading_list)
        self.setLayout(layout)

    def clear_readings(self):
        self.readings.clear()
        self.reading_list.clear_data()
        self.temperature_stability_widget.clear_data()
        self.frequency_stability_widget.clear_data()


    def add_reading(self, reading: Reading):
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