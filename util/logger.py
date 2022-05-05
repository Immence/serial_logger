from PySide6 import QtCore

from bridges.program_state_bridge import ProgramStateBridge
from util.csv_writer import write_csv_line

from util.exceptions import InvalidFileNameException, InvalidQrCodeException

from util.validators import Validators

class Logger(QtCore.QObject):
    qr_code: str = None
    file_name : str = None
    _PSB : ProgramStateBridge

    def __init__(self, PSB : ProgramStateBridge):
        QtCore.QObject.__init__(self)

        self._PSB = PSB
        self._PSB.reading_received.connect(self.handle_reading_received)
        self._PSB.device_disconnected.connect(self.handle_device_disconnect)
        self._PSB.qr_code_set.connect(self.set_qr_code)
        self._PSB.file_name_set.connect(self.set_file_name)

    def set_qr_code(self, qr_code : str):
        qr_code = qr_code.upper()

        if not Validators.validate_qr_code(qr_code):
            self._PSB.raise_error.emit(InvalidQrCodeException)
            return

        self.qr_code = qr_code

    def set_file_name(self, file_name : str):
        if not file_name.endswith(".csv"):
            self._PSB.raise_error.emit(InvalidFileNameException())
            return

        self.file_name = file_name

    def handle_device_disconnect(self):
        self.qr_code = None

    def handle_reading_received(self, reading_dict):
        try:
            write_csv_line({"qr_code" : self.qr_code, **reading_dict})
        except Exception as e:
            e.message = "Something went wrong when writing to the CSV file. Make sure it is not in use by another program."
            self._PSB.raise_error.emit(e)


