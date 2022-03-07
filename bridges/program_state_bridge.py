from PySide6 import QtCore, QtWidgets

class ProgramStateBridge(QtWidgets.QWidget):
    """Handles the general program-wide signals"""
    #Disconnect signal
    disconnect = QtCore.Signal()
    #Connect signal
    connected = QtCore.Signal()
    #Active signal
    connection_ready = QtCore.Signal()

    qr_code_set = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.qr_code_set.connect(self.debug)

    def debug(self, str = "WOW"):
        print(str)

        