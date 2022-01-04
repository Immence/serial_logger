from PySide6 import QtGui, QtWidgets

class MyTextBox(QtWidgets.QTextEdit):
    def __init__(self):
        QtWidgets.QTextEdit.__init__(self)
        
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        return super().keyPressEvent(e)
