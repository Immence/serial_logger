from dataclasses import asdict

from bridges.program_state_bridge import ProgramStateBridge
from components.data_containers.bath_reading import BathReading
from components.data_containers.device_reading import DeviceReading
from handlers.settings_file_handler import SettingsFileHandler
from PySide6 import QtCore

import util.validators as Validators
from util.csv_writer import write_csv_line
from util.exceptions import InvalidFileNameException, InvalidQrCodeException
from util.log_writer import write_log_line


class Logger(QtCore.QObject):
    qr_code: str = None
    target_dir : str
    file_name : str = None
    log_file_name : str = None
    latest_bath_reading : BathReading = BathReading("", "")
    _PSB : ProgramStateBridge

    def __init__(self, PSB : ProgramStateBridge):
        QtCore.QObject.__init__(self)

        self.target_dir = SettingsFileHandler().get_default_output_path()
        self._PSB = PSB
        self._PSB.device_disconnected.connect(self.handle_device_disconnect)
        self._PSB.qr_code_set.connect(self.set_qr_code)
        self._PSB.file_name_set.connect(self.set_file_name)
        self._PSB.bath_temperature_set.connect(self.handle_bath_reading_temp_update)
        self._PSB.bath_sg_set.connect(self.handle_bath_reading_sg_update)

    def set_qr_code(self, qr_code : str):
        if qr_code == "Not set":
            return

        qr_code = qr_code.upper()

        if not Validators.validate_qr_code(qr_code):
            self._PSB.raise_error.emit(InvalidQrCodeException())
            return

        self.qr_code = qr_code

    def set_file_name(self, file_name : str):
        if not file_name.endswith(".csv"):
            self._PSB.raise_error.emit(InvalidFileNameException())
            return

        self.file_name = f"{self.target_dir}/{file_name}"
        self.log_file_name = self.file_name.replace(".csv", ".txt")

    def handle_device_disconnect(self):
        self.qr_code = None
    
    def handle_bath_reading_temp_update(self, temperature : str):
        self.latest_bath_reading = BathReading(temperature, self.latest_bath_reading.sg)

    def handle_bath_reading_sg_update(self, sg : str):
        self.latest_bath_reading = BathReading(self.latest_bath_reading.temperature, sg)

    def log_communication(self, text : str):
        try:
            if not self.log_file_name:
                write_log_line(text)
            else:
                write_log_line(text, self.log_file_name)
        except Exception as e:
            e.message = "Something went wrong when writing to the log file."
            self._PSB.raise_error.emit(e)

    def write_to_csv(self, reading : DeviceReading):
        try:
            write_csv_line(self.file_name, {"qr_code" : self.qr_code, **asdict(reading), **self.latest_bath_reading.to_dict()})
        except Exception as e:
            print(f"Exception type: {type(e)}\nException message: {e.args[0]}")
            e.message = "Something went wrong when writing to the CSV file. Make sure it is not in use by another program."
            self._PSB.raise_error.emit(e)


