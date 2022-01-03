from queue import Queue
from PySide6.QtCore import pyqtSignal, QObject
import re

from com_bridge import ComBridge

class ResponseInterpreter(QObject):
    """Receives all output from fork and parses it correctly"""
    qrcode_received = pyqtSignal(str)
    hardware_id_received = pyqtSignal(str)
    device_variant_received = pyqtSignal(str)
    fork_constant_a_received = pyqtSignal(str)
    fork_constant_b_received = pyqtSignal(str)
    temp_constant_b_received = pyqtSignal(str)
    temp_constant_c_received = pyqtSignal(str)
    temp_constant_d_received = pyqtSignal(str)
    temp_constant_e_received = pyqtSignal(str)
    calibration_temperature_received = pyqtSignal(str)
    sg_received = pyqtSignal(str)
    low_liquid_freq_received = pyqtSignal(str)
    high_liquid_freq_received = pyqtSignal(str)
    low_liquid_sg_received = pyqtSignal(str)
    high_liquid_sg_received = pyqtSignal(str)
    temperature_received = pyqtSignal(str)
    reference_sg_received = pyqtSignal(float)
    reference_temp_received = pyqtSignal(float)
    is_reference_fork_received = pyqtSignal(int)
    reading_received = pyqtSignal(dict)

    com_bridge: ComBridge

    finished = pyqtSignal()

    _input_buffer_empty: bool

    def __init__(self, response_queue: Queue, com_bridge: ComBridge):
        super().__init__()
        self.response_queue = response_queue
        self.com_bridge = com_bridge
        self._input_buffer_empty = True

    def run(self):
        while True:
            
            if not self.response_queue.empty():
                if self._input_buffer_empty:
                    self._input_buffer_empty = False
                    self.com_bridge.input_buffer_empty.emit(False)

                response = self.response_queue.get()

                # Set indicator to green
                # "ets" seems random, but it's in the first line a device prints when turned on

                if "ets" in response or response == "Command Mode running":
                    self.com_bridge.device_connected.emit(True)
                    self.com_bridge.device_ready.emit(True)
                        
                elif response == "Command Mode running":
                    self.com_bridge.device_ready.emit(True)
                
                # Set indicator to red
                elif response == "Brownout detector was triggered":
                    self.com_bridge.device_connected.emit(False)
                    self.com_bridge.device_ready.emit(False)


                elif response.startswith("#"):
                    if "QRCode" in response:
                        self.__emit_qr_code(response)
                    elif "HardwareID" in response:
                        self.__emit_hardware_id(response)
                    elif "Device variant" in response:
                        self.__emit_device_variant(response)
                    elif "Fork" in response:
                        self.__emit_fork_constant(response)
                    elif "Temp" in response:
                        self.__emit_temp_constants(response)
                    elif "Calitemp" in response:
                        self.__emit_calibration_temperature(response)
                    elif "Temperature" in response:
                        self.__emit_liquid_temperature(response)
                    elif "Specific Gravity" in response:
                        self.__emit_specific_gravity(response)
                    elif "Low liquid frequency" in response:
                        self.__emit_low_liquid_freq(response)
                    elif "High liquid frequency" in response:
                        self.__emit_high_liquid_freq(response)
                    elif "Low and High liquid frequencies" in response:
                        self.__emit_low_and_high_liquid_freq(response)
                    elif "Low" in response:
                        self.__emit_low_liquid_sg(response)
                    elif "High" in response:
                        self.__emit_high_liquid_sg(response)
                    elif "reference_sg" in response:
                        self.__emit_reference_sg(response)
                    elif "reference_temp" in response:
                        self.__emit_reference_temp(response)
                    elif "is_reference_fork" in response:
                        self.__emit_reference_fork(response)
                    elif "Frequency" in response and "Temperature" in response and "SG" in response:
                        self.__emit_reading(response)
                    else:
                        print(f"Error interpreting response: {self.__get_value(response)}")
                        print(response)
            else:
                if not self._input_buffer_empty:
                    self._input_buffer_empty = True
                    self.com_bridge.input_buffer_empty.emit(True)


    @staticmethod
    def __get_value(response: str) -> str:
        index = response.find(":")
        res_value = response[index + 2:]
        return res_value

    def __emit_reading(self, response: str):
        split_str = re.split(": | ", response)
        reading = {
            "freq": float(split_str[1]),
            "temp": float(split_str[3])
        }
        
        self.reading_received.emit(reading)
        
    def __emit_reference_fork(self, response: str):
       # print(f"Emitting is_reference_fork: {response}")
        #print(int(self.__getValue(response)))
        self.is_reference_fork_received.emit(int(self.__get_value(response)))

    def __emit_reference_temp(self, response: str):
        #print("Emitting reference temp")
        self.reference_temp_received.emit(float(self.__get_value(response)))

    def __emit_reference_sg(self, response: str):
        #print("Emitting reference sg")
        self.reference_sg_received.emit(float(self.__get_value(response)))

    def __emit_qr_code(self, response: str):
        self.qrcode_received.emit(self.__get_value(response))

    def __emit_hardware_id(self, response: str):
        self.hardware_id_received.emit(self.__get_value(response))

    def __emit_device_variant(self, response: str):
        self.device_variant_received.emit(self.__get_value(response))

    def __emit_fork_constant(self, response: str):
        if "A" in response:
            self.fork_constant_a_received.emit(self.__get_value(response))
        elif "B" in response:
            self.fork_constant_b_received.emit(self.__get_value(response))
        else:
            pass

    def __emit_temp_constants(self, response: str):
        # print(f"Emitting {self.__get_value(response)}")
        # print(f"As float: {float(self.__get_value(response))}")
        if "B" in response:
            self.temp_constant_b_received.emit(self.__get_value(response))
        elif "C" in response:
            self.temp_constant_c_received.emit(self.__get_value(response))
        elif "D" in response:
            self.temp_constant_d_received.emit(self.__get_value(response))
        elif "E" in response:
            self.temp_constant_e_received.emit(self.__get_value(response))
        else:
            pass

    def __emit_calibration_temperature(self, response: str):
        self.calibration_temperature_received.emit(self.__get_value(response))

    def __emit_liquid_temperature(self, response: str):
        self.temperature_received.emit(self.__get_value(response))

    def __emit_specific_gravity(self, response: str):
        self.sg_received.emit(self.__get_value(response))

    def __emit_low_liquid_freq(self, response: str):
        self.low_liquid_freq_received.emit(self.__get_value(response))
            
    def __emit_high_liquid_freq(self, response: str):
        self.high_liquid_freq_received.emit(self.__get_value(response))

    def __emit_low_liquid_sg(self, response: str):
        self.low_liquid_sg_received.emit(self.__get_value(response))

    def __emit_high_liquid_sg(self, response: str):
        self.high_liquid_sg_received.emit(self.__get_value(response))

    def __emit_low_and_high_liquid_freq(self, response: str):
        print(response)
        print(list(response))
        self.low_and_high_liquid_freq_received.emit(list(self.__get_value(response)))
