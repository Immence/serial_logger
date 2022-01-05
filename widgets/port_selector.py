from PySide6 import QtCore, QtWidgets

from util.port_scanner import PortScanner


placeholder_text = "No ports found.."

class PortSelector(QtWidgets.QComboBox):

    port_selected = QtCore.Signal(str)
    port_disconnected = QtCore.Signal()
    
    __port_watcher: PortScanner
    __ports = QtCore.QStringListModel([])
    __active_port: str = None

    def __init__(self):
        QtWidgets.QComboBox.__init__(self)

        self.setMaximumWidth(200)
        self.setPlaceholderText(placeholder_text)
        self.setModel(self.__ports)
        self.activated.connect(self.set_current_port)
        self.__port_watcher = PortScanner()
        self.__port_watcher.ports_updated.connect(self.on_port_list_change)
        self.__port_watcher.start()
        

    def on_port_list_change(self, ports):
        self.__ports.setStringList(ports)

        self.setCurrentText(self.__active_port)
        
        if len(ports) == 0:
            self.setCurrentIndex(-1)
            self.clear()
            self.set_current_port()
            return

        elif len(ports) == 1:
            self.set_current_port()
            return

        if self.__active_port not in ports:
            self.port_disconnected.emit()
    

    def set_current_port(self):
        if self.__active_port is None and self.currentText() == "":
            return

        elif self.currentText() == "":
            self.port_disconnected.emit()
            return

        self.__active_port = self.currentText()
        self.port_selected.emit(self.__active_port)

    def on_port_disconnected(self):
        self.__active_port = None
        self.set_current_port()