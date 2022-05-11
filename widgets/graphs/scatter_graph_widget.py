from PySide6 import QtWidgets

import pyqtgraph as pg
import numpy as np

from components.data_containers.device_reading import DeviceReading

class ScatterGraphWidget(QtWidgets.QWidget):
    
    frequencies: list[float]
    spots : list[dict]

    max_reading_length : int

    pw : pg.PlotWidget
    yax_1 : pg.PlotDataItem

    def __init__(self,):
        QtWidgets.QWidget.__init__(self)

        self.pw = pg.plot()
        self.max_reading_length = 10
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.pw)

        # Init lists and stuff
        self.frequencies = list()
        self.spots = list()

    
        self.scatter = pg.ScatterPlotItem(size = 10, brush = pg.mkBrush(255, 255, 255))
        self.average_line = pg.InfiniteLine(0, 0, pen=pg.mkPen("red", width=3))

        self.pw.addItem(self.scatter)
        self.pw.addItem(self.average_line)
        self.scatter.getViewBox().setMouseEnabled(False, False)
        # Set layout
        self.setLayout(layout)


    def add_reading(self, reading : DeviceReading = None):
        if len(self.frequencies) > self.max_reading_length:
            self.frequencies = self.frequencies[1:]
            self.spots = self.spots[1:]
        self.frequencies.append(float(reading.frequency))
        if len(self.spots) == 0:
            self.spots.append({"pos": (0, float(reading.frequency))})
        else:
            self.spots.append({"pos": (self.spots[-1]["pos"][0]+1, float(reading.frequency))})
        self.scatter.setData(self.spots)
        self.average_line.setPos(np.average(self.frequencies))

    def clear_data(self):
        self.frequencies.clear()
        self.scatter.clear()
        self.spots.clear()
        self.average_line.setPos(0)

    def toggleGraphWindow(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
            