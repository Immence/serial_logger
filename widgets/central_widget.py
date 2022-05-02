from PySide6 import QtWidgets, QtCore, QtGui
from bridges.program_state_bridge import ProgramStateBridge

from widgets.readings_widget.readings_widget import ReadingsWidget

class CentralWidget(QtWidgets.QWidget):
    _PSB : ProgramStateBridge
    
    readings_widget : ReadingsWidget
    in_progress_indicator : QtWidgets.QLabel

    loading_gif : str

    def __init__(self, PSB : ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)

        self._PSB = PSB 
        self._PSB.device_disconnected.connect(self.handle_device_disconnected)
        self.loading_gif = "cool_loading_1.gif"

        self.readings_widget = ReadingsWidget()
        self._PSB.reading_received.connect(self.readings_widget.add_reading)
        self._PSB.clear_reading_list.connect(self.readings_widget.clear_readings)
        
        self._PSB.start_reading.connect(self.handle_start_reading)
        self._PSB.stop_reading.connect(self.handle_stop_reading)
        self.in_progress_indicator = QtWidgets.QLabel()
        movie = QtGui.QMovie(f"res/{self.loading_gif}")
        self.in_progress_indicator.setMovie(movie)


        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.readings_widget, alignment = QtCore.Qt.AlignLeft)
        layout.addWidget(self.in_progress_indicator, 1, QtCore.Qt.AlignHCenter)
        self.setLayout(layout)
    
    def handle_device_disconnected(self):
        self.readings_widget.clear_readings()

    def handle_start_reading(self):
        print("Start reading!")
        self.in_progress_indicator.movie().start()
        self.in_progress_indicator.show()

    def handle_stop_reading(self):
        print("Stop reading!")
        self.in_progress_indicator.movie().stop()
        self.in_progress_indicator.hide()
