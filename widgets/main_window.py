from PySide6 import QtWidgets, QtGui

from PySide6.QtCore import Qt
from bridges.program_state_bridge import ProgramStateBridge
from widgets.line_graph_widget import LineGraphWidget
from widgets.scatter_graph_widget import ScatterGraphWidget
from widgets.port_selector import PortSelector

from widgets.serial_monitor import SerialMonitor
from widgets.button_menu import CommandButtonGroup

from util.serial_thread import SerialThread

from handlers.response_handler import ResponseHandler
from widgets.toolbars.top_toolbar import TopToolBar
from widgets.toolbars.bottom_toolbar import BottomToolBar

from widgets.gearhead_widget import GearheadWidget

from global_values import WIN_HEIGHT, WIN_WIDTH, BAUD_RATE
from widgets.views.text_variable_view import TextVariableView
from components.custom_dock_widget import CustomDockWidget

class MainWindow(QtWidgets.QMainWindow):

    PSB : ProgramStateBridge

    serial_monitor_dock_widget : CustomDockWidget
    line_graph_dock_widget : CustomDockWidget
    text_variable_dock_widget : CustomDockWidget
    serial_monitor_dock_widget : CustomDockWidget

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.PSB = ProgramStateBridge()

        self.init_dock_widgets()
      
        #Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        
        self.response_handler = ResponseHandler(self.PSB)

        self.PSB.device_disconnected.connect(self.handle_device_disconnected)
        
        self.serial_thread = SerialThread(BAUD_RATE)
        self.serial_thread.response_emitter.connect(self.serial_monitor.append_text)
        self.PSB.reading_received.connect(self.line_graph_widget.add_reading)
        self.PSB.reading_received.connect(self.scatter_plot_widget.add_reading)
        self.port_selector.port_selected.connect(self.serial_thread.set_port)
        self.serial_thread.response_emitter.connect(self.response_handler.handle_response)

        ### Add dock widgets
        self.addDockWidget(Qt.TopDockWidgetArea, self.port_selector_dock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.command_button_dock_widget)
        if self.serial_monitor_dock_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.serial_monitor_dock_widget)
        if self.line_graph_dock_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.line_graph_dock_widget)
        if self.scatter_plot_dock_widget:
            self.addDockWidget(Qt.BottomDockWidgetArea, self.scatter_plot_dock_widget)
        if self.text_variable_dock_widget:
            self.addDockWidget(Qt.LeftDockWidgetArea, self.text_variable_dock_widget)
        
        ### Set layout
        self.central_widget = GearheadWidget(self.PSB)
        self.setCentralWidget(self.central_widget)
        self.__create_toolbars()
        self.resize(WIN_WIDTH, WIN_HEIGHT)
    
    def __create_toolbars(self):
        top_toolbar = TopToolBar(self, self.PSB)
        bottom_toolbar = BottomToolBar(self, self.serial_monitor_dock_widget.toggle_window, self.line_graph_dock_widget.toggle_window, self.scatter_plot_dock_widget.toggle_window)
        self.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)
        self.addToolBar(Qt.TopToolBarArea, top_toolbar)

    def exit_program(self):
        self.port_selector.stop()
        self.serial_thread.stop()
        self.close()

    def handle_device_disconnected(self):
        print("HANDLE DEVICE DISCONNECTED")
        self.line_graph_widget.clear_data()
        self.scatter_plot_widget.clear_data()
        self.command_buttons.stop_readings()

    def init_dock_widgets(self):
        ### Dock widgets
        # Port selector widget
        self.port_selector = PortSelector()
        self.port_selector_dock_widget = CustomDockWidget(self.port_selector, self, title="Port selector")

        # Command button widget
        self.command_buttons = CommandButtonGroup(self.PSB)
        self.command_button_dock_widget = CustomDockWidget(self.command_buttons, self, title="Commands")

        # Text set widget
        self.text_variable_view = TextVariableView(self)
        self.text_variable_dock_widget = CustomDockWidget(self.text_variable_view, self)

        # Serial monitor widget
        self.serial_monitor = SerialMonitor()
        self.serial_monitor_dock_widget = CustomDockWidget(self.serial_monitor, self, windowed=True, title="Serial monitor")

        ## Graph widgets
        self.line_graph_widget = LineGraphWidget()
        self.line_graph_dock_widget = CustomDockWidget(self.line_graph_widget, self, windowed=True, title="Line graph, last 100 readings")

        self.scatter_plot_widget = ScatterGraphWidget()
        self.scatter_plot_dock_widget = CustomDockWidget(self.scatter_plot_widget, self, windowed=True, title="Scatter plot, last 10 readings")

