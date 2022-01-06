from PySide6 import QtWidgets

from util.commands import Commands
from global_values import COMMAND_QUEUE

class CommandButton(QtWidgets.QPushButton):

    def __init__(self, name, fun):
        QtWidgets.QPushButton.__init__(self, name)
        self.fun = fun
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.blockSignals(True)
        COMMAND_QUEUE.put(self.fun())
        self.blockSignals(False)

class CommandButtonGroup(QtWidgets.QWidget):

    get_freq_run: CommandButton
    get_freq_stop: CommandButton

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)
        self.get_freq_run = CommandButton("Start reading", Commands.get_freq_run)
        self.get_freq_stop = CommandButton("Stop reading", Commands.get_freq_stop)

        layout.addWidget(self.get_freq_run)
        layout.addWidget(self.get_freq_stop)
        self.setLayout(layout)
