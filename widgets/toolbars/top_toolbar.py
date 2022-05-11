from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from bridges.program_state_bridge import ProgramStateBridge
from files.res.icons import Icons

class TopToolBar(QtWidgets.QToolBar):

    _PSB : ProgramStateBridge

    def __init__(self, parent, PSB : ProgramStateBridge):
        QtWidgets.QToolBar.__init__(self, parent)
        self._PSB = PSB
        self._create_actions()
        # self.addAction(self.reset_action)
        # self.addAction(self.add_bath_measurement_action)
        # self.addAction(self.export_data_action)
        # self.addSeparator()
        # self.addAction(self.select_new_station_action)
        self.setMovable(False)

    def _create_actions(self):
        pass
        # self.add_bath_measurement_action = QtGui.QAction(self)
        # self.add_bath_measurement_action.triggered.connect(self._PSB.update_bath_state)
        # self.add_bath_measurement_action.setText("New bath measurement")

        # self.export_data_action = QtGui.QAction(self)
        # self.export_data_action.triggered.connect(self._PSB.export_data)
        # self.export_data_action.setText("Export data to ZIP")    
        
        # self.select_new_station_action = QtGui.QAction(self)
        # self.select_new_station_action.triggered.connect(self._PSB.select_new_mode)
        # self.select_new_station_action.setText("Select new station")  

    def raise_error(self):
        exception = Exception()
        exception.message = "Testing testing 1-2-3"
        self._PSB.raise_error.emit(exception)
    
    def handle_interrupt(self):
        self.reset_action.setDisabled()
    