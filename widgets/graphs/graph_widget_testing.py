import sys

from PySide6 import QtCore, QtGui, QtWidgets

from datetime import datetime
import pyqtgraph as pg

from random import randint

class GraphWidget(QtWidgets.QWidget):
    
    frequencies: list[float]
    temperatures: list[float]
    time: list[float]

    max_reading_length : int

    def __init__(self,):
        QtWidgets.QWidget.__init__(self)
        self.graphWidget = pg.PlotWidget()
        self.max_reading_length = 100
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphWidget)
        
        # self.frequencies = [1, 2, 3]
        # self.temperatures = []
        # self.time = [1, 2, 3]

        self.frequencies = list()
        self.temperatures = list()
        self.time = list()
        self.graphWidget.setBackground('w')

        # self.graphWidget.setLabel("left", "Frequency")
        # self.graphWidget.setLabel("right", "Temperature")
        # self.graphWidget.addLegend()

        pen = pg.mkPen(color=(255, 0, 0))
        pen_2 = pg.mkPen(color=(0, 255, 0))
        self.data_line = self.graphWidget.plot(self.time, self.frequencies, pen=pen)
        # self.data_line_2 = self.graphWidget.plot(self.time, self.temperatures, pen=pen_2)
        self.setLayout(layout)



    def add_reading(self, reading : dict):
        if len(self.frequencies) > self.max_reading_length:
            self.frequencies = self.frequencies[1:]
            self.temperatures = self.temperatures[1:]
            self.time = self.time[1:]
        self.frequencies.append(float(reading["frequency"]))
        self.temperatures.append(float(reading["temperature"]))
        self.time.append(len(self.frequencies))
        self.data_line.setData(self.time, self.frequencies)

    def clear_readings(self):
        self.frequencies.clear()
        self.temperatures.clear()

    def toggleGraphWindow(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
            