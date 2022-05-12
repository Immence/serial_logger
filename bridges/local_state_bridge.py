from PySide6 import QtCore

class LocalStateBridge(QtCore.QObject):

    bath_temperature_set = QtCore.Signal(str)
    bath_sg_set = QtCore.Signal(str)


    def __init__(self):
        QtCore.QObject.__init__(self)

        self.bath_temperature_set.connect(self.debug)
        self.bath_sg_set.connect(self.debug)


    def debug(self, signal_str = "LOCAL WOWEEEEEE"):
        sender_index = self.senderSignalIndex()
        print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {signal_str}")
    
    def debug_error_signal(self, error : Exception):
        sender_index = self.senderSignalIndex()
        try:
            print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {error.message}")
        except:
            print("Caught error without a message set!")
            print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {error.args[0]}")