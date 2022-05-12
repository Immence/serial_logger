from PySide6 import QtCore, QtWidgets

class LocalStateBridge(QtWidgets.QWidget):
    """ Handles the mode-specific signals"""
    qr_code_set = QtCore.Signal(str)

    target_sg_set = QtCore.Signal(str)

    pass_threshold_set = QtCore.Signal(str)

    reading_amount_set = QtCore.Signal(str)

    start_reading = QtCore.Signal()

    program_ready = QtCore.Signal(bool)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.qr_code_set.connect(self.debug)
        self.target_sg_set.connect(self.debug)
        self.pass_threshold_set.connect(self.debug)
        self.reading_amount_set.connect(self.debug)
        self.start_reading.connect(self.debug)
        self.program_ready.connect(self.debug)


    def debug(self, signal_str = "LOCAL WOWEEEEEE"):
        sender_index = self.senderSignalIndex()
        print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {signal_str}")
        

        