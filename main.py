import sys

from PySide6 import QtWidgets
from widgets.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    opt = err = None

    w = MainWindow()
    w.setWindowTitle("PLAATO Serial Logger")
    w.show()
    sys.exit(app.exec())
