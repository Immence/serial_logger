import time, serial

from PySide6 import QtCore

from queue import Queue

from global_values import SER_TIMEOUT, COMMAND_QUEUE

class SerialThread(QtCore.QThread):

    port_name: str = None
    baud_rate: int

    running: bool

    text_queue: Queue

    serial_connection: serial.Serial = None

    buf: bytearray

    response_emitter = QtCore.Signal(str)
    serial_connected = QtCore.Signal()
    serial_disconnected = QtCore.Signal()

    __abort: bool = False
    __condition: QtCore.QWaitCondition
    __mutex: QtCore.QMutex
    
    def __init__(self, baud_rate: int):
        QtCore.QThread.__init__(self)
        self.__mutex = QtCore.QMutex()
        self.__condition = QtCore.QWaitCondition()
        
        self.baud_rate = baud_rate
        self.running = True
        self.text_queue = Queue()
        self.buf = bytearray()


    def set_port(self, port_name):
        if port_name == "":
            self.stop()
            self.port_name = None
            return

        if self.port_name != None:
            self.stop()
            
        self.port_name = port_name
        self.__abort = False
        self.start()
        
    def run(self):
        print(f"Opening {self.port_name} at {self.baud_rate} baud")
        
        try:
            self.serial_connection = serial.Serial(self.port_name, self.baud_rate, timeout=SER_TIMEOUT)
            time.sleep(SER_TIMEOUT*1.2)
            self.serial_connection.flushInput()
            print("SERIAL CONNECTION", self.serial_connection)
            print("Connection opened successfully")
        
        except Exception as e:
            print(e)
            self.serial_connection = None

        if self.serial_connection is None:
            print("Failed to open the port")
            self.__abort = True

        else:
            self.serial_connected.emit()

        while True:
            if self.__abort:
                return
            try:
                if not COMMAND_QUEUE.empty():
                    output = COMMAND_QUEUE.get()
                    print(output)
                    bytes_command = bytes(output, "ascii")
                    self.serial_connection.write(bytes_command)

                line = self.read_line()
                
                if line:
                    line = line.decode("ascii", "ignore").strip("\r\n")
                    self.response_emitter.emit(line)

            except Exception as e:
                self.serial_disconnected.emit()
                self.__abort = True


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

    def stop(self):
        self.__mutex.lock()
        self.__abort = True
        self.__condition.wakeOne()
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        self.__mutex.unlock()
        self.wait(2000)
        self.exit()