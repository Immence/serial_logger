from PySide6.QtCore import QObject, Signal

class VariableCommunicationBridge(QObject):
    """Handles the variables set in the program"""
    qr_code_set = Signal(str)
    file_name_set = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        self.qr_code_set.connect(self.debug)
        self.file_name_set.connect(self.debug)


    def debug(self, signal_str = "GLOBAL WOWEEEEEE"):
        sender_index = self.senderSignalIndex()
        print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {signal_str}")
    
    def debug_error_signal(self, error : Exception):
        sender_index = self.senderSignalIndex()
        try:
            print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {error.message}")
        except:
            print("Caught error without a message set!")
            print(f"{self.metaObject().method(sender_index).name()} --#-- Signal: {error.args[0]}")
