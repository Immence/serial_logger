import sys, os

from PySide6 import QtWidgets
from widgets.main_window import MainWindow

from global_values import OUTPUT_FOLDER

def create_directory():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER, exist_ok = True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    opt = err = None

    create_directory()

    w = MainWindow()
    w.setWindowTitle("PLAATO Serial Logger")
    w.show()
    with open("res/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    r = app.exec()
    w.exit_program()
    sys.exit(r)
