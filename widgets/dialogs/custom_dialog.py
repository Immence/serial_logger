from PySide6 import QtWidgets, QtCore, QtGui

        
class CustomErrorDialog(QtWidgets.QDialog):

    button_box : QtWidgets.QDialogButtonBox

    def __init__(self, error : Exception, parent = None):
        super().__init__(parent)

        self.setParent(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.setMaximumHeight(50)

        self.layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Something just ain't right!")
        title.setMaximumHeight(40)
        title.setObjectName("title")
        if not hasattr(error, "message"):
            error.message = error.args[0]
        message = QtWidgets.QLabel(error.message)
        message.setWordWrap(True)
        message.setObjectName("body")

        self.layout.addWidget(title, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addWidget(message, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.button_box, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.setLayout(self.layout)

class SuccessDialog(QtWidgets.QDialog):
    button_box : QtWidgets.QDialogButtonBox

    def __init__(self, message : str, parent = None):
        super().__init__(parent)

        self.setParent(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        buttons = QtWidgets.QDialogButtonBox.Ok
        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.setMaximumHeight(50)

        self.layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("All good!")
        title.setMaximumHeight(40)
        title.setObjectName("title")
        message = QtWidgets.QLabel(message)
        message.setWordWrap(True)
        message.setObjectName("body")

        self.layout.addWidget(title, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addWidget(message, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.button_box, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.setLayout(self.layout)

class StationPickerDialog(QtWidgets.QDialog):
    button_box : QtWidgets.QDialogButtonBox

    station_picked = None

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setParent(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.ApplicationModal)
        self.station_1_button = QtWidgets.QPushButton("Station 1")
        self.station_2_button = QtWidgets.QPushButton("Station 2")

        self.station_1_button.clicked.connect(self.accept)
        self.station_2_button.clicked.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Select your station")
        title.setMaximumHeight(40)
        title.setObjectName("title")

        self.layout.addWidget(title, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addWidget(self.station_1_button, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.station_2_button, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)
    
class CustomImageDialog(QtWidgets.QDialog):

    button_box : QtWidgets.QDialogButtonBox

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setParent(parent)
        self.setMinimumSize(600, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        accept_button = QtWidgets.QPushButton("I feel better now, thank you")
        accept_button.clicked.connect(self.accept)
        self.central_widget = QtWidgets.QLabel()
        self.movie = QtGui.QMovie(f"res/hugs-cute.gif")
        self.central_widget.setMovie(self.movie)
        self.movie.start()

        self.layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("You're gonna be fine!")
        title.setObjectName("title")
        self.layout.addWidget(title, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addWidget(self.central_widget, alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(accept_button, alignment = QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)