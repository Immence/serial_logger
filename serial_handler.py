import serial
import threading
import time
from response_interpreter import ResponseInterpreter

from queue import Queue

from PySide6.QtCore import pyqtSignal, QThread

class SerialHandler(threading.Thread):

    response_signal = pyqtSignal(str)
    interpreter: ResponseInterpreter
    interpreter_thread: QThread

    def __init__(self, command_queue: Queue, response_queue: Queue, baud: int, port: str):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.baud = baud
        self.port = port
        self.command_queue = command_queue
        self.response_queue = response_queue
        self.running = False
        self.connection = serial.Serial()
        self.interpreter_thread = QThread()
        self.buf = bytearray()

    def run(self):
        self.__connect()

        while self.running:
            if self.connection.is_open:
                if self.command_queue.empty() == False:
                    output = self.command_queue.get()
                    bytes_command = bytes(output, "ascii")
                    self.connection.write(bytes_command)
                
                line = self.readline()
                if line:
                    line = line.decode("ascii", "ignore").strip("\r\n")
                    self.response_queue.put(line)

        self.connection.close()
        for x in range(6):
            time.sleep(0.33)
            print(".", end='')

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.connection.in_waiting))
            data = self.connection.read(i)
            if (data == b""):
                return None
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

    def close(self):
        print("terminating serial connection")
        self.running = False
    
    def change_port(self, port: str):
        print("Changing port")
        self.port = port
                
    def __connect(self):
        print(f"Connecting serial on port: {self.port} BAUD: {self.baud}")
        try:
            self.connection.port = self.port
            self.connection.baudrate = self.baud
            self.connection.timeout = 1
            self.connection.open()
            time.sleep(2)
            if self.connection.is_open:
                print("Serial connection ready")
                self.running = True
                
        except Exception as exception:
            print(f"Serial connection failed. Exception: {exception}")
            time.sleep(5)     


