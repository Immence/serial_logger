from PySide6.QtCore import QObject, Signal

class ProgramStateBridge(QObject):
    """Handles the general program-wide signals"""
    # Serial connection status signals
    serial_connected = Signal()
    serial_disconnected = Signal()
    
    # Device connection signals
    device_connected = Signal()
    device_disconnected = Signal()

    # Command mode signal
    device_ready = Signal()

    # Reading signal
    start_reading = Signal()
    stop_reading = Signal()

    serial_received = Signal(dict)

    reading_received = Signal(dict)

    clear_reading_list = Signal()

    write_to_csv = Signal(dict)


    raise_error = Signal(Exception)
    emit_error = Signal(Exception)

    # All interrupt signals
    request_interrupt = Signal()
    user_request_interrupt = Signal()
    notify_interrupted = Signal()
    allow_continue = Signal()

    qr_code_received = Signal(str)
    qr_code_set = Signal(str)
    file_name_set = Signal(str)

    # Top bar signals
    update_bath_state = Signal()
    export_data = Signal()
    select_new_mode = Signal()
    reset_readings = Signal()

    # Other global signals
    success_dialog = Signal(str)
    start_calibration_readings = Signal()
    start_stabilization_readings = Signal() 

    def __init__(self):
        QObject.__init__(self)
        self.serial_received.connect(self.debug)
        self.device_disconnected.connect(self.debug)
        self.serial_connected.connect(self.debug)
        self.serial_disconnected.connect(self.debug)
        self.device_ready.connect(self.debug)
        self.device_connected.connect(self.debug)
        self.raise_error.connect(self.debug_error_signal)
        self.allow_continue.connect(self.debug)
        self.update_bath_state.connect(self.debug)
        self.success_dialog.connect(self.debug)
        self.start_reading.connect(self.debug)
        self.stop_reading.connect(self.debug)
        self.qr_code_set.connect(self.debug)
        self.file_name_set.connect(self.debug)
        
        #interceptor
        self.raise_error.connect(self.intercept_error_signal)

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

    def intercept_error_signal(self, error : Exception):
        if not hasattr(error, "message"):
            error.message = error.args[0]

        self.emit_error.emit(error)