from PySide6 import QtWidgets, QtGui

from res.font_styles import Fonts


class ReadingComponent(QtWidgets.QWidget):
    
    freq: float
    temp: float
    freq_comp: float
    sg: float

    def __init__(self, freq, temp, freq_comp, sg, index = 0):
        QtWidgets.QWidget.__init__(self)

        self.freq = freq
        self.temp = temp
        self.freq_comp = freq_comp
        self.sg = sg
        
        self.setMaximumHeight(100)
        self.setMaximumWidth(400)
        layout = QtWidgets.QGridLayout()
        
        layout.setSpacing(0)
        
        index_label = QtWidgets.QLabel(str(index+1))
        frequency = QtWidgets.QLabel("Hz")
        temperature = QtWidgets.QLabel(u"\N{DEGREE SIGN}C")
        gravity = QtWidgets.QLabel("SG")

        freq_value = QtWidgets.QLabel(self.freq)
        temperature_value = QtWidgets.QLabel(self.temp)
        gravity_value = QtWidgets.QLabel(self.sg)
        
        layout.addWidget(index_label, 0, 0, 2, 1)
        layout.addWidget(frequency, 0, 1)
        layout.addWidget(temperature, 0, 2)
        layout.addWidget(gravity, 0, 3)
        layout.addWidget(freq_value, 1, 1)
        layout.addWidget(temperature_value, 1, 2)
        layout.addWidget(gravity_value, 1, 3)
        self.setLayout(layout)

    

    

