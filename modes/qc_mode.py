from PySide6 import QtCore, QtGui, QtWidgets

from components.my_text_box import TextContainerReadOnly

class QcMode(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        self.text_box = TextContainerReadOnly()
        layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)
