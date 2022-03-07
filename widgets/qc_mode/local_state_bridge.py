from PySide6 import QtCore, QtWidgets

class LocalStateBridge(QtWidgets.QWidget):
    """ Handles the mode-specific signals"""
    qr_code_set = QtCore.Signal(str)

    target_sg_set = QtCore.Signal(str)

    pass_threshold_set = QtCore.Signal(str)

    reading_amount_set = QtCore.Signal(str)

    start_reading = QtCore.Signal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.target_sg_set.connect(self.debug)
        self.pass_threshold_set.connect(self.debug)

    def debug(self, signal_str = "WOW"):
        sender_index = self.senderSignalIndex()
        print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {signal_str}")
        

        