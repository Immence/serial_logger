from bridges.program_state_bridge import ProgramStateBridge
from global_values import COMMAND_QUEUE
from PySide6 import QtWidgets
from util.commands import Commands


class CommandButton(QtWidgets.QPushButton):

    def __init__(self, name, fun):
        QtWidgets.QPushButton.__init__(self, name)
        self.setObjectName("standard-button")
        self.fun = fun
        self.clicked.connect(self.on_click)
        self.setDisabled(True)

    def on_click(self):
        self.blockSignals(True)
        COMMAND_QUEUE.put(self.fun())
        self.blockSignals(False)

class CommandButtonGroup(QtWidgets.QWidget):

    get_qr_code: CommandButton
    get_freq_run: CommandButton
    get_freq_stop: CommandButton

    def __init__(self, PSB : ProgramStateBridge):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)
        self.get_qr_code = CommandButton("Get QR code", Commands.get_qr_code)
        self.get_freq_run = CommandButton("Start reading", Commands.get_freq_run)
        self.get_freq_run.clicked.connect(lambda : PSB.start_reading.emit())
        self.get_freq_stop = CommandButton("Stop reading", Commands.get_freq_stop)
        self.get_freq_stop.clicked.connect(lambda : PSB.stop_reading.emit())

        # Connection status
        PSB.device_ready.connect(self.handle_device_ready)
        PSB.device_disconnected.connect(self.handle_device_disconnected)

        # Layout
        layout.addWidget(self.get_qr_code)
        layout.addWidget(self.get_freq_run)
        layout.addWidget(self.get_freq_stop)
        self.setLayout(layout)

    def handle_device_ready(self):
        self.get_qr_code.setDisabled(False)
        self.get_freq_run.setDisabled(False)
        self.get_freq_stop.setDisabled(False)

    def handle_device_disconnected(self):
        self.get_qr_code.setDisabled(True)
        self.get_freq_run.setDisabled(True)
        self.get_freq_stop.setDisabled(True)

    def stop_readings(self):
        self.get_freq_stop.click()
