from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from enum import Enum, unique

@unique
class Status(Enum):
    DISCONNECTED = 1
    WAITING = 2
    CONNECTED = 3


class ConnectionIndicator(QtWidgets.QWidget):
    __color: Qt.GlobalColor
    __state: bool
    __pixmap: QtGui.QPixmap

    __rad_x = 100
    __rad_y = 100

    status = Status.DISCONNECTED
    painter: QtGui.QPainter

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        painter = QtGui.QPainter()
        __state = False
        __color = Qt.red

    def status_change(self, status: Status):
        pass

    def _draw(self):
        # https://stackoverflow.com/questions/24943711/qt-drawing-icons-using-color-and-alpha-map
        color: Qt.GlobalColor

        color = Qt.red
        pixmap = QtGui.QPixmap("res/icons8-e-96.png")

        test = QtGui.QPainter(pixmap)
        test.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)

        test.setBrush(color)
        test.setPen(color)

        test.drawRect(pixmap.rect())

        # Here is our new colored icon!
        self.icon = QtGui.QIcon(pixmap)


