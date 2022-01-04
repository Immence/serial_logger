import sys, time, serial

from PySide6 import QtCore, QtGui, QtWidgets

from queue import Queue

WIN_WIDTH, WIN_HEIGHT = 684, 400
SER_TIMEOUT = 0.1
RETURN_CHAR = "\n"
PASTE_CHAR = "\x16"
BAUD_RATE = 115200
PORT_NAME = "/dev/ttyUSB0"

def str_bytes(s):
    return s.encode("latin-1")

def bytes_str(d):
    return d if type(d) is str else "".join([chr(b) for b in d])

def display(s):
    pass

class MyTextBox(QtWidgets.QTextEdit):
    def __init__(self):
        QtWidgets.QTextEdit.__init__(self)
        
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        return super().keyPressEvent(e)

        
class MyWidget(QtWidgets.QWidget):
    
    text_update = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.text_box = MyTextBox()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_box.setFont(font)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.text_update.connect(self.append_text)
        sys.stdout = self

        self.serial_thread = SerialThread(PORT_NAME, BAUD_RATE)
        self.serial_thread.start()

    def write(self, text):
        self.text_update.emit(text)

    def flush(self):
        pass

    def append_text(self, text):
        curr = self.text_box.textCursor()
        curr.movePosition(QtGui.QTextCursor.End)
        s = str(text)
        while s:
            head, sep, s = s.partition("\n")
            curr.insertText(head)
            if sep:
                curr.insertBlock()
        self.text_box.setTextCursor(curr)
    
    def keypress_handler(self, event):
        k = event.key()
        s = RETURN_CHAR if k == QtCore.Qt.Key_Return else event.text()
        if len(s)>0 and s[0] == PASTE_CHAR:
            cb = QtWidgets.QApplication.clipboard()
            self.serial_thread.ser_out(cb.text())
        else:
            self.serial_thread.ser_out(s)

    def closeEvent(self, event):
        self.serial_thread.running = False
        self.serial_thread.wait()

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

    def ser_out(self, s):
        self.text_queue.put(s)
    
    def ser_in(self, s):
        display(s)

    def run(self):
        print(f"Opening {self.port_name} at {self.baud_rate} baud")
        
        try:
            print("Trying to open the connection..")
            self.serial_connection = serial.Serial(self.port_name, self.baud_rate, timeout=SER_TIMEOUT)
            time.sleep(SER_TIMEOUT*1.2)
            self.serial_connection.flushInput()
            print("Opening connection is done")
        
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    opt = err = None

    w = MyWidget()
    w.setWindowTitle("PLAATO Serial Logger")
    w.show()
    sys.exit(app.exec())
# class MainWindow(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         self.button = QtWidgets.QPushButton("Click me!")
#         self.text = QtWidgets.QLabel("Hello World",
#                                         alignment=QtCore.Qt.AlignCenter)

#         self.layout = QtWidgets.QVBoxLayout(self)
#         self.layout.addWidget(self.text)
#         self.layout.addWidget(self.button)
    
# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])

#     widget = MainWindow()
#     widget.resize(800, 600)
#     widget.show()

#     sys.exit(app.exec())