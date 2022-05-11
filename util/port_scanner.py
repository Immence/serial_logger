import time
import re

from PySide6 import QtCore

from serial.tools import list_ports

class PortScanner(QtCore.QThread):

    ports_updated = QtCore.Signal(list)
    __abort: bool = False
    __condition: QtCore.QWaitCondition
    __mutex: QtCore.QMutex

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__mutex = QtCore.QMutex()
        self.__condition = QtCore.QWaitCondition()

        self.__ports = []

    def get_ports(self):
        ports = []
        for port, desc, hwid in sorted(list_ports.comports()):
            ports.append(port)
        filtered_ports = self.filter_ports(ports)
        if len(filtered_ports) != len(self.__ports):
            # Publish port change
            self.ports_updated.emit(filtered_ports)
        
        self.__ports = filtered_ports
        return self.__ports

    def run(self):
        print("Port watcher running")
        while True:
            if self.__abort:
                return
            self.get_ports()

            time.sleep(0.7)

    def filter_ports(self, ports):
        blacklist = [
            "Bluetooth",
            "Powerbeats",
            "JBLFlip",
            "ACM"
        ]

        blacklistExp = re.compile(
            "|".join([re.escape(word) for word in blacklist])
        )
        filtered_ports = []
        for port in ports:
            if not blacklistExp.search(port):
                filtered_ports.append(port)

        return filtered_ports
    
    def stop(self):
        self.__mutex.lock()
        self.__abort = True
        self.__condition.wakeOne()
        self.__mutex.unlock()
        self.wait(2000)
        self.exit()
