from PySide6 import QtWidgets, QtCore
from util.validators import Validators

class InputField(QtWidgets.QLineEdit):

    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)

class InputButton(QtWidgets.QPushButton):

    def __init__(self, title):
        QtWidgets.QPushButton.__init__(self, title)

class InputWidget(QtWidgets.QWidget):

    input_field: InputField
    input_button: InputButton

    emit_input = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout(self)
        self.input_field = InputField()
        self.input_button = InputButton("Submit")
        self.input_button.clicked.connect(self.on_click)
        layout.addWidget(self.input_field)
        layout.addWidget(self.input_button)
        self.setLayout(layout)

    
    def on_click(self):
        if Validators.validate_qr_code(self.input_field.text()):
            self.emit_input.emit(self.input_field.text())

        else:
            print(f"ERROR - INVALID QR-CODE: {self.input_field.text()}")

    

    