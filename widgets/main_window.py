from PySide6 import QtWidgets, QtGui

from PySide6.QtCore import Qt
from widgets.port_selector import PortSelector
from widgets.qc_mode.qc_mode_main_widget import QcModeMainWidget

from widgets.serial_monitor import SerialMonitor
from widgets.input_widget import InputWidget
from widgets.button_menu import CommandButtonGroup
from widgets.toolbar import ToolBar
from util.serial_thread import SerialThread

from handlers.response_handler import ResponseHandler
from bridges.program_state_bridge import ProgramStateBridge

from modes.mode_enum import Mode

from global_values import WIN_HEIGHT, WIN_WIDTH, BAUD_RATE


class MainWindow(QtWidgets.QMainWindow):
    PSB : ProgramStateBridge
    mode: Mode
    top_dock_widget: QtWidgets.QDockWidget = None
    right_dock_widget: QtWidgets.QDockWidget = None
    central_widget: QtWidgets.QDockWidget = None
    bottom_widget: QtWidgets.QDockWidget = None


    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.PSB = ProgramStateBridge()
        self.port_selector = PortSelector()
        self.bottom_widget = QtWidgets.QDockWidget("Serial Port")
        self.bottom_widget.setWidget(self.port_selector)
        self.bottom_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        
        self.monitor = SerialMonitor()
        self.serial_widget = QtWidgets.QDockWidget()
        self.serial_widget.setWidget(self.monitor)
        self.serial_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.serial_widget.resize(1000, 600)
        self.serial_widget.setHidden(True)
        
        #Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.button = QtWidgets.QPushButton("Click me!")

        self.response_handler = ResponseHandler(self.PSB)
        self.PSB.qr_code_set.connect(self.response_handler.set_qr_code)

        self.serial_thread = SerialThread(BAUD_RATE)
        self.port_selector.port_selected.connect(self.serial_thread.set_port)
        self.serial_thread.response_emitter.connect(self.monitor.append_text)
        self.serial_thread.response_emitter.connect(self.response_handler.handle_response)

        self.mode = Mode.QC

        if self.mode == Mode.QC:
            self.init_qc_mode()

        elif self.mode == Mode.OTHER:
            self.init_other_mode()

        #Dock widgets
        if self.bottom_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_widget)
        if self.serial_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.serial_widget)
        if self.top_dock_widget:
            self.addDockWidget(Qt.TopDockWidgetArea, self.top_dock_widget)
        if self.right_dock_widget:
            self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock_widget)
        
        self.setCentralWidget(self.central_widget)
        self._create_toolbars()
        self.resize(WIN_WIDTH, WIN_HEIGHT)

    def _create_toolbars(self):
        top_toolbar = ToolBar(self, self.toggle_serial_monitor)
        self.addToolBar(Qt.BottomToolBarArea, top_toolbar)

    def init_qc_mode(self):
        self.central_widget = QcModeMainWidget(self.PSB)
        #Top dock widget
        top_widget = self.central_widget.get_top_dock_widget()
        self.top_dock_widget = QtWidgets.QDockWidget("Calibration QC Options")
        self.top_dock_widget.setWidget(top_widget)
        self.top_dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

    def init_other_mode(self):
        #Top dock widget
        self.input_field = InputWidget()
        self.input_field.emit_input.connect(self.PSB.qr_code_set)
        self.top_dock_widget = QtWidgets.QDockWidget("QR-Code")
        self.top_dock_widget.setWidget(self.input_field)
        self.top_dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        #Right dock widget
        self.command_buttons = CommandButtonGroup()
        self.right_dock_widget = QtWidgets.QDockWidget("Commands")
        self.right_dock_widget.setWidget(self.command_buttons)
        self.right_dock_widget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        

    def toggle_serial_monitor(self):
        if self.serial_widget.isHidden():
            if not self.serial_widget.isFloating():
                self.serial_widget.setFloating(True)
            self.serial_widget.show()
        else:
            self.serial_widget.hide()