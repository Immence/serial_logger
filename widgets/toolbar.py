from PySide6 import QtWidgets, QtGui

from res.icons import Icons

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        QtWidgets.QToolBar.__init__(self, parent)
        self._create_actions(parent)
        self.addAction(self.newAction)
        self.addAction(self.otherAction)

    def _create_actions(self, parent):
        self.newAction = QtGui.QAction(self)
        self.newAction.setText("&Serial Monitor")
        self.newAction.setIcon(Icons.test_icon())
        print(parent)

        self.otherAction = QtGui.QAction(self)
        self.otherAction.setText("&Other action")
        self.otherAction.setIcon(Icons.test_icon())


    