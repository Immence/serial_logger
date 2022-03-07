from PySide6 import QtWidgets, QtCore

from res.font_styles import Fonts

class InputWithTitle(QtWidgets.QFrame):

    title: QtWidgets.QLabel
    input_field: QtWidgets.QLineEdit
    submit_button: QtWidgets.QPushButton

    emit_input = QtCore.Signal(str)

    def __init__(self, title= "Title not set", text="Not set"):
        QtWidgets.QFrame.__init__(self)
        
        # Child widgets
        self.title = QtWidgets.QLabel(title)
        self.title.setFont(Fonts.body())
        self.input_field = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_click)
        # QFrame properties
        self.setMaximumHeight(120)
        self.setMaximumWidth(200)
        self.input_field.setMaximumWidth(100)
        self.submit_button.setMaximumWidth(100)
    
        # Main Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def on_click(self):
        self.emit_input.emit(self.input_field.text())

