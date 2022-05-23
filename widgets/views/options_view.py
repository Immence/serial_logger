import util.middlewares as Middlewares
from components.text_widgets import ToggleTextEditWithTitle
from PySide6 import QtCore, QtWidgets


class OptionsLayout(QtWidgets.QFrame):

    bath_temperature : ToggleTextEditWithTitle
    bath_sg : ToggleTextEditWithTitle    

    bath_temperature_change = QtCore.Signal(str)
    bath_sg_change = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        self.layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel("Optional settings")
        self.bath_temperature = ToggleTextEditWithTitle(self, "Bath temperature")
        self.bath_temperature.set_text_width_max(70)
        self.bath_temperature.emit_text_change.connect(self.bath_temperature_change)
        self.bath_sg = ToggleTextEditWithTitle(self, "Bath SG")
        self.bath_sg.set_text_width_max(70)
        self.bath_sg.emit_text_change.connect(self.bath_sg_change)
        
        self.setMaximumHeight(250)
        self.setMaximumWidth(250)
        self.layout.addWidget(title_label)
        self.layout.addWidget(self.bath_temperature)
        self.layout.addWidget(self.bath_sg)

        self.setLayout(self.layout)

class QcOptionsLayout(QtWidgets.QFrame):

    bath_temperature : ToggleTextEditWithTitle
    bath_sg : ToggleTextEditWithTitle    
    reading_amount : ToggleTextEditWithTitle
    pass_threshold : ToggleTextEditWithTitle

    force_start : QtWidgets.QPushButton
    bath_temperature_change = QtCore.Signal(str)
    bath_sg_change = QtCore.Signal(str)
    reading_amount_change = QtCore.Signal(str)
    pass_threshold_change = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        self.layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel("QC settings")

        self.bath_temperature = ToggleTextEditWithTitle(self, "Bath temperature", Middlewares.replace_comma)
        self.bath_temperature.emit_text_change.connect(self.bath_temperature_change)
        self.bath_sg = ToggleTextEditWithTitle(self, "Bath SG", Middlewares.replace_comma)
        self.bath_sg.emit_text_change.connect(self.bath_sg_change)
        self.reading_amount = ToggleTextEditWithTitle(self, "Reading amount")
        self.reading_amount.emit_text_change.connect(self.reading_amount_change)
        self.pass_threshold = ToggleTextEditWithTitle(self, "Pass threshold", Middlewares.replace_comma)
        self.pass_threshold.emit_text_change.connect(self.pass_threshold_change)
        self.force_start = QtWidgets.QPushButton("Force start")
        
        self.setMaximumWidth(250)
        self.layout.addWidget(title_label)
        self.layout.addWidget(self.bath_temperature)
        self.layout.addWidget(self.bath_sg)
        self.layout.addWidget(self.reading_amount)
        self.layout.addWidget(self.pass_threshold)
        self.layout.addStretch()
        self.layout.addWidget(self.force_start)

        self.setLayout(self.layout)

    def set_default_values(self):
        self.reading_amount.set_default_text("5")
        self.pass_threshold.set_default_text("0.001")

