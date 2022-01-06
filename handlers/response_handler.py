from PySide6 import QtCore

from datetime import datetime
import time
from util import csv_writer
from util import log_writer

unit_dict = {           # Fuck it, I might handle unit stuff at a later point if it's necessary.
    "c": "Celsius",
    "f": "Fahrenheit",
}


class ResponseHandler(QtCore.QObject):
    qr_code = ""
    
    def __init__(self):
        super().__init__()

    def handle_response(self, text) -> None:
        log_writer.write_log_line(text)

        if text.startswith("#"):
            parsed_text = self.interpret_response(self.qr_code, text)
            csv_writer.write_csv_line(parsed_text)

    def set_qr_code(self, qr_code: str) -> None:
        self.qr_code = qr_code
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
                headers.append(word.strip(":"))
            elif word[len(word)-1].isnumeric():
                values.append(word)

        for i in range (0,len(headers)):
            parsed_text[headers[i]] = values[i]

        parsed_text["gmt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        unix = int(time.time())
        parsed_text["unix"] = unix

        return parsed_text
    