from PySide6 import QtWidgets, QtGui

from res.icons import Icons

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent, action1):
        QtWidgets.QToolBar.__init__(self, parent)
        self._create_actions(action1)
        self.addAction(self.newAction)
        self.addAction(self.otherAction)
        self.setMovable(False)

    def _create_actions(self, action1):
        self.newAction = QtGui.QAction(self)
        self.newAction.setText("&Serial Monitor")
        self.newAction.setIcon(Icons.test_icon())
        self.newAction.triggered.connect(action1)
        self.otherAction = QtGui.QAction(self)
        self.otherAction.setText("&Other action")
        self.otherAction.setIcon(Icons.test_icon())


    