from PySide6 import QtCore, QtWidgets

class LocalStateBridge(QtWidgets.QWidget):
    """ Handles the mode-specific signals"""
    qr_code_set = QtCore.Signal(str)

    target_sg_set = QtCore.Signal(str)

    pass_threshold_set = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

    def debug(self, str = "WOW"):
        print(str)

        