from PySide6 import QtWidgets, QtCore, QtGui
from bridges.program_state_bridge import ProgramStateBridge
from widgets.views.options_view import OptionsLayout

from widgets.views.text_variable_view import TextVariableView

from widgets.device_readings_widget.readings_widget import DeviceReadingsWidget
from widgets.bath_readings_widget.bath_readings_widget import BathReadingsWidget
from components.gif_component import GifComponent

class GearheadWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    
    device_readings_widget : DeviceReadingsWidget
    in_progress_indicator : QtWidgets.QLabel
    options_view : OptionsLayout

    test : TextVariableView

    loading_gif_path : str

    def __init__(self, PSB : ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        self.setContentsMargins(0, 10, 0, 0)
        self._PSB = PSB 
        self._PSB.device_disconnected.connect(self.handle_device_disconnected)
        self.loading_gif_path = "cool_loading_1.gif"
        
        device_readings_layout = QtWidgets.QVBoxLayout()
        self.device_readings_widget = DeviceReadingsWidget()
        device_readings_title_bar = QtWidgets.QHBoxLayout()
        device_readings_title = QtWidgets.QLabel("Device readings")
        device_readings_reset_button = QtWidgets.QToolButton(self)
        device_readings_reset_button.clicked.connect(PSB.reset_readings)
        device_readings_reset_button.setText("Reset")
        device_readings_reset_button.setIcon(QtGui.QIcon.fromTheme("edit-undo"))
    
        device_readings_title_bar.addWidget(device_readings_title,alignment= QtCore.Qt.AlignHCenter)
        device_readings_title_bar.addWidget(device_readings_reset_button, alignment=QtCore.Qt.AlignRight)
        device_readings_layout.addLayout(device_readings_title_bar)
        device_readings_layout.addWidget(self.device_readings_widget)

        self._PSB.reading_received.connect(self.device_readings_widget.add_reading)
        self._PSB.reset_readings.connect(self.device_readings_widget.clear_readings)
        
        self.options_view = OptionsLayout(self)

        self._PSB.start_reading.connect(self.handle_start_reading)
        self._PSB.stop_reading.connect(self.handle_stop_reading)

        self.in_progress_indicator = GifComponent()
        self.in_progress_indicator.set_gif_path(self.loading_gif_path)
        self.in_progress_indicator.hide()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.options_view, alignment = QtCore.Qt.AlignTop)
        layout.addWidget(self.in_progress_indicator, 1, QtCore.Qt.AlignHCenter)
        layout.addStretch()
        layout.addLayout(device_readings_layout, 1)
        self.setLayout(layout)
    
    def handle_device_disconnected(self):
        self.device_readings_widget.clear_readings()
        self.handle_stop_reading()

    def handle_start_reading(self):
        print("Start reading!")
        self.in_progress_indicator.show()

    def handle_stop_reading(self):
        print("Stop reading!")
        self.in_progress_indicator.hide()
