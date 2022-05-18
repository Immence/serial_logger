from PySide6 import QtCore, QtGui, QtWidgets


class StartStopButton(QtWidgets.QPushButton):


    __ready : bool = False
    __in_progress : bool = False
    __finished : bool = False

    values_changed = QtCore .Signal()

    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setFont(QtGui.QFont("Helvetica", pointSize=28, weight = QtGui.QFont.Bold))
        self.setMaximumHeight(200)
        self.update_button()
        self.values_changed.connect(self.update_button)
        
    def update_button(self):
        if not self.__ready:
            self.set_start_style()
            self.setDisabled(True)
            self.__in_progress = False
            self.setText("START")
            return

        else:
            self.setDisabled(False)

        if self.__ready and not self.__in_progress:
            self.set_start_style()
            if self.__ready and self.__finished:
                self.setText("RESTART")
            else:
                self.setText("START")
        else:
            self.set_stop_style()
            self.setText("STOP")

    def set_start_style(self):
        self.setStyleSheet("""
            StartStopButton
                {
                    background-color: #2ABf9E;
    
                    padding: 10px;
                }
                """)
    
    def set_stop_style(self):
         self.setStyleSheet("""
            StartStopButton
                { 
                    background-color: #c95b4b;
                    padding: 10px;
                }
                """)

    def get_in_progress(self) -> bool:
        return self.__in_progress

    def set_in_progress(self, in_progress : bool):
        self.__in_progress = in_progress
        self.values_changed.emit()

    def set_ready(self, ready : bool):
        self.__ready = ready
        self.values_changed.emit()

    def get_ready(self) -> bool:
        return self.__ready

    def set_finished(self, finished : bool):
        self.__finished = finished
        self.values_changed.emit()

    def get_finished(self) -> bool:
        return self.__finished
