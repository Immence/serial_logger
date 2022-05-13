from PySide6 import QtCore, QtGui, QtWidgets


class StartStopButton(QtWidgets.QPushButton):


    __ready : bool = True
    __in_progress : bool = False

    ready_change = QtCore.Signal(str)
    in_progress_change = QtCore.Signal(bool)

    values_changed = QtCore .Signal()
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setFont(QtGui.QFont("Helvetica", pointSize=28, weight = QtGui.QFont.Bold))
        self.setMaximumHeight(200)
        self.setObjectName("massive-button")
        self.update_button()
        self.clicked.connect(lambda : self.set_in_progress(not self.get_in_progress()))
        self.in_progress_change.connect(lambda : print("In progress change"))
        
    def update_button(self):
        if not self.__ready:
            self.setDisabled(True)
            self.set_in_progress(False)

        else:
            self.setDisabled(False)

        if self.__ready and not self.__in_progress:
            self.setStyleSheet("""
            StartStopButton
                {
                    background-color: #2ABf9E;
    
                    padding: 10px;
                }
                """)  
            self.setText("START")

        else:
            self.setStyleSheet("""
            StartStopButton
                { 
                    background-color: #c95b4b;
                    padding: 10px;
                }
                """)
            self.setText("STOP")

    def get_in_progress(self) -> bool:
        return self.__in_progress
    def set_in_progress(self, in_progress : bool):
        self.update_button()
        self.__in_progress = in_progress
        self.in_progress_change.emit(self.__in_progress)
    def set_ready(self, ready : bool):
        self.update_button()
        self.__ready = ready
        self.ready_change.emit(str(self.__ready))
    def get_ready(self) -> bool:
        return self.__ready

    ready = QtCore.Property(bool, get_ready, set_ready, notify=ready_change)
    in_progress = QtCore.Property(bool, get_in_progress, set_in_progress, notify=in_progress_change)
