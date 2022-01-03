import threading
from PySide6.QtCore import QObject, pyqtSignal, pyqtSlot
import time

class StreamReceiver(QObject):
    stream_receiver_signal = pyqtSignal(str)

    def __init__(self, queue, *args,**kwargs):
        QObject.__init__(self, *args,**kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.stream_receiver_signal.emit(text) 