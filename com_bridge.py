from PySide6.QtCore import pyqtSignal, QObject

class ComBridge(QObject):

    ports_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()