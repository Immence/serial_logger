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

    def __init__(self):
        super().__init__()

    def handle_response(self, text) -> None:
        log_writer.write_log_line(text)

        if text.startswith("#"):
            parsed_text = self.interpret_response(text)
            csv_writer.write_csv_line(parsed_text)

    @staticmethod
    def interpret_response(text: str) -> dict:
        parsed_text = {
            "unix": int(time.time()), 
            "gmt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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

        return parsed_text
    