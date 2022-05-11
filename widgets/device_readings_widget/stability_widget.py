from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from files.res.font_styles import Fonts

class StatusFrame(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        
        ### Frame
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.setFixedWidth(200)
        ### Labels
        average_descriptor_label = QtWidgets.QLabel("Avg.")
        deviance_descriptor_label = QtWidgets.QLabel("Dev.")
        self.average_label = QtWidgets.QLabel("")
        self.average_label.setFont(Fonts.title())
        self.deviance_label = QtWidgets.QLabel("")
        self.deviance_label.setFont(Fonts.title())
        
        ### Layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(average_descriptor_label, 0, 0, Qt.AlignLeft)
        layout.addWidget(self.average_label, 0, 1)
        layout.addWidget(deviance_descriptor_label, 1, 0, Qt.AlignLeft)
        layout.addWidget(self.deviance_label, 1, 1)
        self.setLayout(layout)
    
    def set_average(self, average: str):
        self.average_label.setText(average)

    def set_deviance(self, deviance: str):
        self.deviance_label.setText(f"± {deviance}")

    def clear_data(self):
        self.average_label.setText("")
        self.deviance_label.setText("")


class StabilityComponent(QtWidgets.QFrame):

    def __init__(self, title : str, subtitle : str = " last 10 "):
        QtWidgets.QFrame.__init__(self)
        
        self.setMaximumHeight(150)
        ### Labels
        self.title = QtWidgets.QLabel(title)
        self.subtitle = QtWidgets.QLabel(subtitle)
        self.temp_status = StatusFrame()
        
        ### Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.title, Qt.AlignHCenter)
        layout.addWidget(self.subtitle, Qt.AlignHCenter)
        layout.addWidget(self.temp_status)
        
        self.setLayout(layout)

    def update_status(self, average:str, deviance:str):
        self.temp_status.set_average(average)
        self.temp_status.set_deviance(deviance)

    def clear_data(self):
        self.temp_status.clear_data()