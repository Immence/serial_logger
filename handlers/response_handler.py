from PySide6 import QtCore

from datetime import datetime
import time
from bridges.program_state_bridge import ProgramStateBridge
from util import log_writer
from util.exceptions import CommunicationFailedException
from components.data_containers.device_reading import DeviceReading

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
    
    # Serial connection status signals
    serial_connected = QtCore.Signal()
    serial_disconnected = QtCore.Signal()
    
    # Device connection signals
    device_connected = QtCore.Signal()
    device_disconnected = QtCore.Signal()
    
    def __init__(self, PSB : ProgramStateBridge):
        super().__init__()
        self._PSB = PSB

    def handle_response(self, text: str) -> None:

        # Device has been connected and turned on
        if text.startswith("rst"):
            if "POWERON_RESET" in text:
                self._PSB.serial_connected.emit()
        
        elif text == "Could not find command":
            self._PSB.raise_error.emit(CommunicationFailedException())
            return
        # Device reports that command mode is ready
        elif text.startswith(ready_triggers[0]):
            print("DEVICE READY, RESPONSE HANDLER")
            self._PSB.device_ready.emit()
            
        # Device has been turned off or disconnected
        elif text.startswith(disconnect_triggers[0]):
            self._PSB.device_disconnected.emit()
        
        elif text.startswith("#"):
            parsed_text = ResponseHandler.__interpret_response(text)
            if type(parsed_text) is DeviceReading:
                self._PSB.reading_received.emit(parsed_text)
            else:
                if "qrcode" in parsed_text:
                    self._PSB.qr_code_received.emit(parsed_text["qrcode"])   
                self._PSB.serial_received.emit(parsed_text)

    @staticmethod
    def __interpret_response(text: str) -> dict:
        parsed_text = {
            }
        
        word_list = text.strip("# ").split()
        headers = []
        values= []
        if len(word_list) > 2:
            if "Frequency:" and "Temperature:" in word_list:
                for word in word_list:
                    if word.endswith(":"):
                        headers.append(word.strip(":").lower())
                    elif word[len(word)-1].isnumeric():
                        values.append(word)
                zip_iterator = zip(headers, values)
                return DeviceReading(**dict(zip_iterator))

            elif "frequency" in word_list:
                headers.append("low")
                values.append(word_list[4])
                
            elif "Temp" in word_list:
                if "B:" in word_list:
                    headers.append("temp_b")
                elif "C:" in word_list:
                    headers.append("temp_c")
                elif "D:" in word_list:
                    headers.append("temp_d")
                elif "E:" in word_list:
                    headers.append("temp_e")
                values.append(word_list[2])
            
            elif "Low" in word_list:
                if "frequency:" in word_list:
                    headers.append("low_liquid_frequency")
                    values.append(word_list[3])
            elif "High" in word_list:
                if "frequency:" in word_list:
                    headers.append("high_liquid_frequency")
                    values.append(word_list[3])
            
            elif "variant:" in word_list:
                headers.append("device_variant")
                values.append(word_list[2])

            elif "Fork" in word_list:
                if "A:" in word_list:
                    headers.append("constant_a")
                    values.append(word_list[2])
                elif "B:" in word_list:
                    headers.append("constant_b")
                    values.append(word_list[2])

        else:
            for word in word_list:
                if word.endswith(":"):
                    headers.append(word.strip(":").lower())
                else: 
                    values.append(word)

        for i in range (0,len(headers)):
            parsed_text[headers[i]] = values[i]

        parsed_text["gmt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        unix = int(time.time())
        parsed_text["unix"] = unix

        return parsed_text