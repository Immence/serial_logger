from PySide6 import QtWidgets, QtGui

from PySide6.QtCore import Qt
from widgets.port_selector import PortSelector

from widgets.serial_monitor import SerialMonitor
from handlers.file_handler import FileHandler

from util.serial_thread import SerialThread

import util.log_writer as logger

from constants import WIN_HEIGHT, WIN_WIDTH, BAUD_RATE

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.port_selector = PortSelector()
        self.dock_widget = QtWidgets.QDockWidget("Serial Port")
        self.dock_widget.setWidget(self.port_selector)

        self.dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        #Menu
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_widget)

        #Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.button = QtWidgets.QPushButton("Click me!")
        
        self.monitor = SerialMonitor()
        self.file_handler = FileHandler()
        
        self.serial_thread = SerialThread(BAUD_RATE)
        self.port_selector.port_selected.connect(self.serial_thread.set_port)
        self.serial_thread.response_emitter.connect(self.monitor.append_text)
        self.serial_thread.response_emitter.connect(logger.write_log)

        # layout = QtWidgets.QVBoxLayout(self)
        # layout.addWidget(self.monitor)
        # layout.addWidget(self.button)
        # self.setLayout(layout)
        self.setCentralWidget(self.monitor)
        self.resize(WIN_WIDTH, WIN_HEIGHT)