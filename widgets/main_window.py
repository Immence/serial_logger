from PySide6 import QtWidgets

from widgets.serial_monitor import SerialMonitor

from constants import WIN_HEIGHT, WIN_WIDTH

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        
        self.monitor = SerialMonitor()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.monitor)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.resize(WIN_WIDTH, WIN_HEIGHT)