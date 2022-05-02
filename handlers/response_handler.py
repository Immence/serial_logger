from PySide6 import QtCore

from datetime import datetime
import time
from bridges.program_state_bridge import ProgramStateBridge
from util import csv_writer
from util import log_writer

unit_dict = {           # Fuck it, I might handle unit stuff at a later point if it's necessary.
    "c": "Celsius",
    "f": "Fahrenheit",
}

start_triggers = ["rst", "POWERON_RESET"]
ready_triggers = ["Command Mode running"]
disconnect_triggers = ["Brownout"]
fail_triggers = ["Sleep"]

class ResponseHandler(QtCore.QObject):
    _PSB : ProgramStateBridge
    qr_code = ""
    
    # Serial connection status signals
    serial_connected = QtCore.Signal()
    serial_disconnected = QtCore.Signal()
    
    # Device connection signals
    device_connected = QtCore.Signal()
    device_disconnected = QtCore.Signal()
    
    def __init__(self, PSB : ProgramStateBridge):
        super().__init__()
        self._PSB = PSB

    def handle_response(self, text) -> None:
        log_writer.write_log_line(text)
         # Device has been connected and turned on
        if text.startswith("rst"):
            if "POWERON_RESET" in text:
                self._PSB.serial_connected.emit()
        
        # Device reports that command mode is ready
        elif text.startswith(ready_triggers[0]):
            self._PSB.device_ready.emit()
            
        # Device has been turned off or disconnected
        elif text.startswith(disconnect_triggers[0]):
            self._PSB.device_disconnected.emit()

        elif text.startswith("#"):
            parsed_text = self.interpret_response(self.qr_code, text)
            if "frequency" and "temperature" in parsed_text:
                self._PSB.reading_received.emit(parsed_text)
            csv_writer.write_csv_line(parsed_text)

    def set_qr_code(self, qr_code: str) -> None:
        self.qr_code = qr_code
        self.handle_response(f"//////////////////////////////////\nQR-code has been set to {self.qr_code}")
        print(f"QR-code has been set to {self.qr_code}")

    @staticmethod
    def interpret_response(qr_code: str, text: str) -> dict:
        parsed_text = {
            "qr_code": qr_code,
            }

        word_list = text.strip("# ").split()
        headers = []
        values= []
        for word in word_list:
            if word.endswith(":"):
                headers.append(word.strip(":").lower())
            elif word[len(word)-1].isnumeric():
                values.append(word)

        for i in range (0,len(headers)):
            parsed_text[headers[i]] = values[i]

        parsed_text["gmt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        unix = int(time.time())
        parsed_text["unix"] = unix

        return parsed_text
    