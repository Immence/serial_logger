from PySide6 import QtWidgets

from files.res.font_styles import Fonts

class FieldWithTitle(QtWidgets.QFrame):

    title: QtWidgets.QLabel
    text: QtWidgets.QLabel

    def __init__(self, title= "Title not set", text="Not set"):
        QtWidgets.QFrame.__init__(self)
        
        self.title = QtWidgets.QLabel(title)
        self.title.setFont(Fonts.body())
        self.text = QtWidgets.QLabel(text)
        self.text.setFont(Fonts.title())

        self.setMaximumHeight(70)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def set_text(self, text: any) -> None:
        self.text.setText(str(text))

