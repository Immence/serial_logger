from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from res.icons import Icons

class ToolBar(QtWidgets.QToolBar):

    _serial_monitor_action: QtGui.QAction

    def __init__(self, parent, serial_monitor_action):
        QtWidgets.QToolBar.__init__(self, parent)
        self._create_actions(serial_monitor_action)
        self.addAction(self._serial_monitor_action)
        self.setMovable(False)

    def _create_actions(self, serial_monitor_action):
        self._serial_monitor_action = QtGui.QAction(self)
        self._serial_monitor_action.setText("&Serial Monitor")
        self._serial_monitor_action.setIcon(Icons.test_icon())
        self._serial_monitor_action.triggered.connect(serial_monitor_action)

    