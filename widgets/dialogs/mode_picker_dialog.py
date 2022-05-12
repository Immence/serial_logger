from PySide6 import QtWidgets, QtCore, QtGui

        
class ModePickerDialog(QtWidgets.QDialog):

    gearhead_mode : QtWidgets.QPushButton
    qc_mode : QtWidgets.QPushButton
    cancel : QtWidgets.QPushButton

    selected_mode : str

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setParent(parent)
        self.setMinimumSize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        #Title
        title = QtWidgets.QLabel("Select a new mode")
        title.setMaximumHeight(40)
        title.setObjectName("title")
        
        #Buttons
        buttonLayout = QtWidgets.QGridLayout()
        self.gearhead_mode = QtWidgets.QPushButton("GEARHEAD MODE")
        self.gearhead_mode.clicked.connect(lambda : self.set_mode("gearhead"))
        self.qc_mode = QtWidgets.QPushButton("QC MODE")
        self.qc_mode.clicked.connect(lambda : self.set_mode("qc"))
        self.cancel = QtWidgets.QPushButton("CANCEL")
        self.cancel.clicked.connect(self.reject)

        buttonLayout.addWidget(self.gearhead_mode)
        buttonLayout.addWidget(self.qc_mode)
        buttonLayout.addWidget(self.cancel)
        
        #Main layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(title, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)

    def set_mode(self, mode : str):
        self.selected_mode = mode
        self.accept()