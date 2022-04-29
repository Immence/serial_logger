from PySide6 import QtCore, QtWidgets, QtGui
from util.port_scanner import PortScanner

placeholder_text = "No ports found.."

class PortSelector(QtWidgets.QComboBox):

    port_selected = QtCore.Signal(str)
    port_disconnected = QtCore.Signal()

    __connected: bool
    
    __port_scanner: PortScanner
    __ports = QtCore.QStringListModel([])
    __active_port: str = None

    def __init__(self):
        QtWidgets.QComboBox.__init__(self)

        self.setMaximumWidth(200)
        self.setPlaceholderText(placeholder_text)
        self.setModel(self.__ports)
        # self.activated.connect(self.set_current_port)
        self.__port_scanner = PortScanner()
        self.__port_scanner.ports_updated.connect(self.on_port_list_change)
        self.__port_scanner.start()
        self.currentTextChanged.connect(self.set_current_port)
        
    def on_port_list_change(self, ports):
        self.__ports.setStringList(ports)

    def set_current_port(self, port : str):
        if self.__active_port is None and port == "":
            return

        if port == "":
            self.port_disconnected.emit()
            return

        self.__active_port = self.currentText()
        self.port_selected.emit(self.__active_port)

    def on_port_disconnected(self):
        self.__active_port = None
        self.set_current_port()
    
    def stop(self):
        self.__port_scanner.stop()
