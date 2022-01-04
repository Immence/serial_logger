import time, serial

from PySide6 import QtCore

from queue import Queue

from constants import SER_TIMEOUT

class SerialThread(QtCore.QThread):

    port_name: str
    baud_rate: int

    running: bool

    text_queue: Queue

    serial_connection: serial.Serial

    buf: bytearray

    def __init__(self, port_name:str, baud_rate: int):
        QtCore.QThread.__init__(self)
        self.port_name, self.baud_rate = port_name, baud_rate
        self.running = True
        self.text_queue = Queue()
        self.buf = bytearray()


    def run(self):
        print(f"Opening {self.port_name} at {self.baud_rate} baud")
        
        try:
            self.serial_connection = serial.Serial(self.port_name, self.baud_rate, timeout=SER_TIMEOUT)
            time.sleep(SER_TIMEOUT*1.2)
            self.serial_connection.flushInput()
            print("Connection opened successfully")
        
        except Exception as e:
            print(e)
            self.serial_connection = None

        if self.serial_connection is None:
            print("Failed to open the port")
            self.running = False

        while self.running:
            line = self.read_line()
            if line:
                line = line.decode("ascii", "ignore").strip("\r\n")
                print(line)

        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None

    def read_line(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.serial_connection.in_waiting))
            data = self.serial_connection.read(i)
            if (data == b""):
                return None
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)