from PySide6 import QtCore, QtWidgets

from util.port_scanner import PortScanner


placeholder_text = "No ports found.."

class PortSelector(QtWidgets.QComboBox):

    port_watcher: PortScanner
    
    ports = QtCore.QStringListModel([])
    activated_index  = -1

    def __init__(self):
        QtWidgets.QComboBox.__init__(self)

        self.setMaximumWidth(200)
        self.setPlaceholderText(placeholder_text)
        self.setModel(self.ports)
        #self.activated.connect(self.set_current_port)
        
        self.port_watcher = PortScanner()
        self.port_watcher.ports_updated.connect(self.on_port_list_change)
        self.port_watcher.start()
        

    def on_port_list_change(self, ports):
        if len(ports) == 0:
            self.setCurrentIndex(-1)
            self.clear()
            return

        self.ports.setStringList(ports)

    def set_current_port(self, index):
        self.activated_index = index
        self.setCurrentIndex(self.activated_index)