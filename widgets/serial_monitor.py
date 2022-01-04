import sys

from PySide6 import QtCore, QtGui, QtWidgets

from util.serial_thread import SerialThread
from components.my_text_box import MyTextBox
from constants import PORT_NAME, BAUD_RATE, RETURN_CHAR, PASTE_CHAR
class SerialMonitor(QtWidgets.QWidget):
    
    text_update = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.text_box = MyTextBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_box.setFont(font)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self.text_update.connect(self.append_text)
        sys.stdout = self

        self.serial_thread = SerialThread(PORT_NAME, BAUD_RATE)
        self.serial_thread.start()

    def write(self, text):
        self.text_update.emit(text)

    def flush(self):
        pass

    def append_text(self, text):
        curr = self.text_box.textCursor()
        curr.movePosition(QtGui.QTextCursor.End)
        s = str(text)
        while s:
            head, sep, s = s.partition("\n")
            curr.insertText(head)
            if sep:
                curr.insertBlock()
        self.text_box.setTextCursor(curr)
    
    def keypress_handler(self, event):
        k = event.key()
        s = RETURN_CHAR if k == QtCore.Qt.Key_Return else event.text()
        if len(s)>0 and s[0] == PASTE_CHAR:
            cb = QtWidgets.QApplication.clipboard()
            self.serial_thread.ser_out(cb.text())
        else:
            self.serial_thread.ser_out(s)

    def closeEvent(self, event):
        self.serial_thread.running = False
        self.serial_thread.wait()
