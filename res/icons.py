from PySide6 import QtGui
from PySide6.QtCore import Qt

class Icons:
    TEST_ICON_PATH = "res/icons8-e-96.png"

    @staticmethod
    def test_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.TEST_ICON_PATH)
    
    @staticmethod
    def connection_indicator(color: Qt.GlobalColor) -> QtGui.QIcon:
        pixmap = QtGui.QPixmap(Icons.TEST_ICON_PATH)
        painter = QtGui.QPainter(pixmap)

        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)

        painter.setBrush(color)
        painter.setPen(color)

        painter.drawRect(pixmap.rect())

        painter.end()
        
        return QtGui.QIcon(pixmap)
