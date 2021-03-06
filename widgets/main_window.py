import util.log_writer as LogWriter
from bridges.program_state_bridge import ProgramStateBridge
from components.custom_dock_widget import CustomDockWidget
from components.data_containers.device_reading import DeviceReading
from global_values import BAUD_RATE, COMMAND_QUEUE, WIN_HEIGHT, WIN_WIDTH
from handlers.response_handler import ResponseHandler
from handlers.settings_file_handler import SettingsFileHandler
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from util.commands import Commands
from util.serial_thread import SerialThread

from widgets.command_button_menu import CommandButtonGroup
from widgets.dialogs.custom_dialog import CustomErrorDialog
from widgets.dialogs.mode_picker_dialog import ModePickerDialog
from widgets.gearhead_mode.gearhead_widget import GearheadWidget
from widgets.graphs.line_graph_widget import LineGraphWidget
from widgets.graphs.scatter_graph_widget import ScatterGraphWidget
from widgets.port_selector import PortSelector
from widgets.qc_mode.qc_mode_main_widget import QcModeMainWidget
from widgets.serial_monitor import SerialMonitor
from widgets.toolbars.bottom_toolbar import BottomToolBar
from widgets.toolbars.top_toolbar import TopToolBar
from widgets.views.text_variable_view import TextVariableView


class MainWindow(QtWidgets.QMainWindow):

    PSB : ProgramStateBridge

    port_selector : PortSelector
    serial_thread : SerialThread
    response_handler : ResponseHandler
    serial_monitor : SerialMonitor

    port_selector_dock_widget : CustomDockWidget
    serial_monitor_dock_widget : CustomDockWidget
    line_graph_dock_widget : CustomDockWidget
    text_variable_dock_widget : CustomDockWidget
    serial_monitor_dock_widget : CustomDockWidget

    central_widget : QtWidgets.QWidget = None
    current_mode : str

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.current_mode = SettingsFileHandler().get_program_mode()
        self.PSB = ProgramStateBridge()
        self.PSB.emit_error.connect(self.raise_error_dialog)

        self.response_handler = ResponseHandler(self.PSB)
      
        #Exit QAction
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.triggered.connect(self.exit_program)
        

        # Init connection events
        self.PSB.device_disconnected.connect(self.handle_device_disconnected)
        self.PSB.device_ready.connect(self.handle_device_ready)

        # Init serial thread  
        self.serial_thread = SerialThread(BAUD_RATE)
        self.serial_thread.response_emitter.connect(self.response_handler.handle_response)
        
        
        # Serial monitor widget needs to be connected to receive text for the entire run of the program
        self.serial_monitor = SerialMonitor()
        self.serial_monitor.text_update.connect(LogWriter.write_log_line)
        self.serial_thread.response_emitter.connect(self.serial_monitor.write)
        
        self.port_selector = PortSelector()

        self.init_dock_widgets()
        self.add_dock_widgets()

        ### Set layout
        self.run_selected_mode()
        self.__create_toolbars()
        self.resize(WIN_WIDTH, WIN_HEIGHT)

    
    def run_selected_mode(self):
        print("Running selected mode")
        if self.current_mode == "gearhead":
            print("Running gearhead")
            self.central_widget = GearheadWidget(self.PSB)
        elif self.current_mode == "qc":
            print("Running QC")
            self.central_widget = QcModeMainWidget(self.PSB)
        SettingsFileHandler().set_mode(self.current_mode)
        self.setCentralWidget(self.central_widget)

    def __create_toolbars(self):
        top_toolbar = TopToolBar(self, self.PSB, self.raise_mode_select_dialog)
        bottom_toolbar = BottomToolBar(self, self.serial_monitor_dock_widget.toggle_window, self.line_graph_dock_widget.toggle_window, self.scatter_plot_dock_widget.toggle_window)
        
        self.addToolBar(Qt.TopToolBarArea, top_toolbar)
        self.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)

    def exit_program(self):
        self.port_selector.stop()
        self.serial_thread.stop()
        self.close()

    def handle_device_ready(self):
        # Waiting half a second before sending command because the device appears to have issues reading commands at startup
        QtCore.QTimer.singleShot(500, lambda :  COMMAND_QUEUE.put(Commands.get_qr_code()))
        
    def handle_device_disconnected(self):
        pass

    def init_dock_widgets(self):
        ### Dock widgets
        # Port selector widget
        self.port_selector.port_selected.connect(self.serial_thread.set_port)
        self.port_selector_dock_widget = CustomDockWidget(self.port_selector, self, title="Port selector")

        # Command button widget
        command_buttons = CommandButtonGroup(self.PSB)
        self.PSB.device_disconnected.connect(command_buttons.stop_readings)
        self.command_button_dock_widget = CustomDockWidget(command_buttons, self, title="Commands")

        # Text set widget
        text_variable_view = TextVariableView(self)
        text_variable_view.connect_signals(self.PSB)
        self.text_variable_dock_widget = CustomDockWidget(text_variable_view, self)

        # Serial monitor widget
        self.serial_monitor_dock_widget = CustomDockWidget(self.serial_monitor, self, windowed=True, title="Serial monitor")

        ## Graph widgets
        line_graph_widget = LineGraphWidget()
        self.PSB.reset_readings.connect(line_graph_widget.clear_data)
        self.PSB.device_disconnected.connect(line_graph_widget.clear_data)
        self.PSB.reading_received.connect(line_graph_widget.add_reading)
        self.line_graph_dock_widget = CustomDockWidget(line_graph_widget, self, windowed=True, title="Line graph, last 100 readings")

        scatter_plot_widget = ScatterGraphWidget()
        self.PSB.reset_readings.connect(scatter_plot_widget.clear_data)
        self.PSB.device_disconnected.connect(scatter_plot_widget.clear_data)
        self.PSB.reading_received.connect(scatter_plot_widget.add_reading)
        self.scatter_plot_dock_widget = CustomDockWidget(scatter_plot_widget, self, windowed=True, title="Scatter plot, last 10 readings")

    def add_dock_widgets(self):
        ### Add initialized dock widgets
        #Top
        self.addDockWidget(Qt.TopDockWidgetArea, self.port_selector_dock_widget)
        #Left
        self.addDockWidget(Qt.LeftDockWidgetArea, self.text_variable_dock_widget)
        #Right
        self.addDockWidget(Qt.RightDockWidgetArea, self.command_button_dock_widget)
        #Bottom
        self.addDockWidget(Qt.BottomDockWidgetArea, self.serial_monitor_dock_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.line_graph_dock_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.scatter_plot_dock_widget)

    def raise_mode_select_dialog(self):
        dlg = ModePickerDialog(self)

        if dlg.exec_():
            print("Success")
            if dlg.selected_mode == self.current_mode:
                return
            else:
                self.current_mode = dlg.selected_mode
                self.run_selected_mode()
        else:
            print("Cancel")

    def raise_error_dialog(self, exception: Exception):
        dlg = CustomErrorDialog(exception, self)
        
        if dlg.exec_():
            print("Success")
        else:
            print("Cancel")
