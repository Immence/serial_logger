from handlers.settings_file_handler import SettingsFileHandler
from PySide6 import QtGui
from PySide6.QtCore import Qt

ICON_RESOURCES_PATH = SettingsFileHandler().get_icon_resources_path()

class Icons:
    TEST_ICON_PATH = f"{ICON_RESOURCES_PATH}icons8-e-96.png"
    LINE_GRAPH_ICON_PATH = f"{ICON_RESOURCES_PATH}line-graph-icon.png"
    SCATTER_PLOT_ICON_PATH = f"{ICON_RESOURCES_PATH}scatter-plot-icon.png"
    SUCCESS_ICON_PATH = f"{ICON_RESOURCES_PATH}correct.png"
    FAIL_ICON_PATH = f"{ICON_RESOURCES_PATH}remove.png"

    @staticmethod
    def test_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.TEST_ICON_PATH)
    
    @staticmethod
    def line_graph_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.LINE_GRAPH_ICON_PATH)

    @staticmethod
    def scatter_plot_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.SCATTER_PLOT_ICON_PATH)
    
    @staticmethod
    def success_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.SUCCESS_ICON_PATH)
        
    @staticmethod
    def fail_icon() -> QtGui.QIcon:
        return QtGui.QIcon(Icons.FAIL_ICON_PATH)

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
