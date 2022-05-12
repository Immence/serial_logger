from typing import Callable
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from bridges.program_state_bridge import ProgramStateBridge
from files.res.icons import Icons

class TopToolBar(QtWidgets.QToolBar):

    _PSB : ProgramStateBridge

    def __init__(self, parent, PSB : ProgramStateBridge, new_mode_action : Callable):
        QtWidgets.QToolBar.__init__(self, parent)
        self._PSB = PSB
        self._create_actions(new_mode_action)
        self.addAction(self.select_new_mode_action)
        # self.addAction(self.reset_action)
        # self.addAction(self.add_bath_measurement_action)
        # self.addAction(self.export_data_action)
        # self.addSeparator()
        self.setMovable(False)

    def _create_actions(self, new_mode_action : Callable):
        pass
        # self.add_bath_measurement_action = QtGui.QAction(self)
        # self.add_bath_measurement_action.triggered.connect(self._PSB.update_bath_state)
        # self.add_bath_measurement_action.setText("New bath measurement")

        # self.export_data_action = QtGui.QAction(self)
        # self.export_data_action.triggered.connect(self._PSB.export_data)
        # self.export_data_action.setText("Export data to ZIP")    
        
        self.select_new_mode_action = QtGui.QAction(self)
        self.select_new_mode_action.triggered.connect(new_mode_action)
        self.select_new_mode_action.setText("Select new mode")  

    def raise_error(self):
        exception = Exception()
        exception.message = "Testing testing 1-2-3"
        self._PSB.raise_error.emit(exception)
