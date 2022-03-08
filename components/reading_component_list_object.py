from PySide6 import QtWidgets, QtGui

from res.font_styles import Fonts


class ReadingListItem(QtWidgets.QListWidgetItem):
    
    freq: float
    temp: float
    freq_comp: float
    sg: float
    index: int

    def __init__(self, freq, temp, freq_comp, sg, index = 0):
        QtWidgets.QListWidgetItem.__init__(self)
        self.freq = freq
        self.temp = temp
        self.sg = sg
        self.index = index
        self.set_text()
    
    def set_text(self):
        representation_str = f"{self.index + 1} - {self.freq} Hz - {self.temp} C - {self.sg} SG"
        self.setText(representation_str)
    

