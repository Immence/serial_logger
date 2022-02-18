from PySide6 import QtWidgets

class TextContainerReadOnly(QtWidgets.QTextEdit):
    def __init__(self):
        QtWidgets.QTextEdit.__init__(self)
        self.setReadOnly(True)