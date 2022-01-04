import sys

from PySide6 import QtWidgets
from widgets.main_window import MainWindow


def str_bytes(s):
    return s.encode("latin-1")

def bytes_str(d):
    return d if type(d) is str else "".join([chr(b) for b in d])

def display(s):
    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    opt = err = None

    w = MainWindow()
    w.setWindowTitle("PLAATO Serial Logger")
    w.show()
    sys.exit(app.exec())
