from PySide6 import QtWidgets, QtGui

from PySide6.QtCore import Qt
from bridges.program_state_bridge import ProgramStateBridge
from widgets.port_selector import PortSelector

from widgets.serial_monitor import SerialMonitor
from widgets.input_widget import InputWidget
from widgets.button_menu import CommandButtonGroup

from util.serial_thread import SerialThread

from handlers.response_handler import ResponseHandler
from widgets.toolbars.top_toolbar import TopToolBar
from widgets.toolbars.bottom_toolbar import BottomToolBar

from widgets.central_widget import CentralWidget

from global_values import WIN_HEIGHT, WIN_WIDTH, BAUD_RATE

class MainWindow(QtWidgets.QMainWindow):

    PSB : ProgramStateBridge

    serial_monitor_dock_widget : QtWidgets.QDockWidget
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.PSB = ProgramStateBridge()
        self.port_selector = PortSelector()
        self.dock_widget = QtWidgets.QDockWidget("Serial Port")
        self.dock_widget.setWidget(self.port_selector)
        self.dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        
        self.input_field = InputWidget()
        self.input_widget = QtWidgets.QDockWidget("QR-Code")
        self.input_widget.setWidget(self.input_field)
        self.input_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        self.command_buttons = CommandButtonGroup()
        self.command_widget = QtWidgets.QDockWidget("Commands")
        self.command_widget.setWidget(self.command_buttons)
        self.command_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        #Serial monitor stuff
        monitor = SerialMonitor()
        self.serial_monitor_dock_widget = QtWidgets.QDockWidget()
        self.serial_monitor_dock_widget.setWidget(monitor)
        self.serial_monitor_dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.serial_monitor_dock_widget.resize(1000, 600)
        self.serial_monitor_dock_widget.setHidden(True)
        #Menu
        self.addDockWidget(Qt.TopDockWidgetArea, self.input_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.command_widget)
        #Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.button = QtWidgets.QPushButton("Click me!")
        
        self.response_handler = ResponseHandler(self.PSB)
        self.input_field.emit_input.connect(self.response_handler.set_qr_code)
        
        self.serial_thread = SerialThread(BAUD_RATE)
        self.serial_thread.response_emitter.connect(monitor.append_text)
        self.port_selector.port_selected.connect(self.serial_thread.set_port)
        self.serial_thread.response_emitter.connect(self.response_handler.handle_response)

        # layout = QtWidgets.QVBoxLayout(self)
        # layout.addWidget(self.monitor)
        # layout.addWidget(self.button)
        # self.setLayout(layout)
        if self.serial_monitor_dock_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.serial_monitor_dock_widget)
        
        self.central_widget = CentralWidget(self.PSB)
        self.setCentralWidget(self.central_widget)
        self.__create_toolbars()
        self.resize(WIN_WIDTH, WIN_HEIGHT)
    
    def __create_toolbars(self):
        top_toolbar = TopToolBar(self, self.PSB)
        bottom_toolbar = BottomToolBar(self, self.toggle_serial_monitor)
        self.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
        self.addToolBar(Qt.TopToolBarArea, top_toolbar)

    def exit_program(self):
        self.port_selector.stop()
        self.serial_thread.stop()
        self.close()

    def toggle_serial_monitor(self):
        if self.serial_monitor_dock_widget.isHidden():
            if not self.serial_monitor_dock_widget.isFloating():
                self.serial_monitor_dock_widget.setFloating(True)
            self.serial_monitor_dock_widget.show()
        else:
            self.serial_monitor_dock_widget.hide()
