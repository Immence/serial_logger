import sys

from PySide6 import QtCore, QtGui, QtWidgets

from components.my_text_box import TextContainerReadOnly
from global_values import RETURN_CHAR, PASTE_CHAR, TEXT_SIZE

class SerialMonitor(QtWidgets.QWidget):
    
    text_update = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.text_box = TextContainerReadOnly()
        font = QtGui.QFont()
        font.setPointSize(TEXT_SIZE)
        self.text_box.setFont(font)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self.text_update.connect(self.append_text)
        sys.stdout = self


    def write(self, text):
        self.text_update.emit(text)

    def flush(self):
        pass
    
    def append_global(self, text):
        self.append_text("GLOBAL SIGNAL" + text)
    def append_text(self, text):
        curr = self.text_box.textCursor()
        curr.movePosition(QtGui.QTextCursor.End)
        s = str(text) + "\n"
        while s:
            head, sep, s = s.partition("\n")
            curr.insertText(head)
            if sep:
                curr.insertBlock()
        self.text_box.setTextCursor(curr)

    def toggleSerialMonitor(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
            
    def closeEvent(self, event):
        self.serial_thread.running = False
        self.serial_thread.wait()
