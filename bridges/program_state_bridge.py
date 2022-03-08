from PySide6 import QtCore, QtWidgets

class ProgramStateBridge(QtWidgets.QWidget):
    """Handles the general program-wide signals"""
    #Disconnect signal
    disconnected = QtCore.Signal()
    #Connect signal
    connected = QtCore.Signal()
    #Active signal
    connection_ready = QtCore.Signal()

    qr_code_set = QtCore.Signal(str)

    reading_received = QtCore.Signal(dict)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.qr_code_set.connect(self.debug)
        self.disconnected.connect(self.debug)
        self.connected.connect(self.debug)
        self.connection_ready.connect(self.debug)
        self.reading_received.connect(self.debug)

    def debug(self, signal_str = "GLOBAL WOWEEEEEE"):
        sender_index = self.senderSignalIndex()
        print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {signal_str}")
        