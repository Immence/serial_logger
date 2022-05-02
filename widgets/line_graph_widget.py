import sys

from PySide6 import QtCore, QtGui, QtWidgets

from datetime import datetime
import pyqtgraph as pg

from random import randint

class LineGraphWidget(QtWidgets.QWidget):
    
    frequencies: list[float]
    temperatures: list[float]
    time: list[float]

    max_reading_length : int

    pw : pg.PlotWidget
    yax_1 : pg.PlotDataItem
    yax_2 : pg.PlotCurveItem

    def __init__(self,):
        QtWidgets.QWidget.__init__(self)

        self.pw = pg.PlotWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.pw)

        # Init lists and stuff
        self.frequencies = list()
        self.temperatures = list()
        self.max_reading_length = 100

        ### Multiple axes example:
        # https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/examples/MultiplePlotAxes.py
    
        self.p1 = self.pw.plotItem
        
        # Style left axis
        self.p1.getAxis("left").setGrid(255)
        self.p1.getAxis("left").setLabel("Frequency (Hz)", color="blue")

        ## Create a new viewbox and link the right axis to its coordinate system
        self.p2 = pg.ViewBox()
        self.p1.showAxis("right")
        self.p1.scene().addItem(self.p2)
        self.p1.getAxis("right").linkToView(self.p2)
        self.p2.setXLink(self.p1)
        self.p1.getAxis("right").setLabel("Temperature (\N{DEGREE SIGN}C)", color="red")
    
        self.pw.setBackground("#e8cca264")
        self.p1.vb.sigResized.connect(self.updateViews)

        self.yax_1 = self.p1.plot(self.frequencies, pen=pg.mkPen("blue", width=2))
        self.yax_2 = pg.PlotCurveItem(self.temperatures, pen=pg.mkPen('red', width=2))

        self.p2.addItem(self.yax_2)
        
        self.p1.vb.setLimits(xMin=0, xMax=100, yMin=1200, yMax=1700, minYRange=1, minXRange=100)
        
        self.p2.setLimits(yMin=0, yMax=30, minYRange=1)
        ###
        
        # Set layout
        self.setLayout(layout)

    ## Handle view resizing 
    def updateViews(self):
        ## view has resized; update auxiliary views to match
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
        
        ## need to re-update linked axes since this was called
        ## incorrectly while views had different shapes.
        ## (probably this should be handled in ViewBox.resizeEvent)
        self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)


    def add_reading(self, reading : dict = None):
        if len(self.frequencies) > self.max_reading_length:
            self.frequencies = self.frequencies[1:]
            self.temperatures = self.temperatures[1:]
        self.frequencies.append(float(reading["frequency"]))
        self.temperatures.append(float(reading["temperature"]))
        self.yax_1.setData(self.frequencies)
        self.yax_2.setData(self.temperatures)

    def clear_data(self):
        self.frequencies.clear()
        self.temperatures.clear()
        self.yax_1.clear()
        self.yax_2.clear()

    def toggleGraphWindow(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
            