import time
import re

from PySide6.QtCore import QThread, pyqtSignal

from serial.tools import list_ports

from com_bridge import ComBridge

class PortWatcher(QThread):

    com_bridge: ComBridge
    
    def __init__(self, main_com: ComBridge):
        super().__init__()
        self.com_bridge = main_com
        self._ports = []

    def get_ports(self):
        ports = []
        for port, desc, hwid in sorted(list_ports.comports()):
            ports.append(port)

        filtered_ports = self.filter_ports(ports)
        if(len(filtered_ports) != len(self._ports)):
          # publish event
            self.com_bridge.ports_updated.emit(filtered_ports)
        self._ports = filtered_ports
        return self._ports

    def run(self):
        print("Port watcher running")
        while True:
            self.get_ports()
            
            time.sleep(0.7)

    def filter_ports(self, ports):
        blacklist = [
            'Bluetooth',
            'Powerbeats',
            'JBLFlip',
            "ACM"
        ]

        blacklistExp = re.compile(
            '|'.join([re.escape(word) for word in blacklist]))
        filtered_ports = []
        for port in ports:
            if not blacklistExp.search(port):
                filtered_ports.append(port)

        return filtered_ports