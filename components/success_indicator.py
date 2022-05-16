from files.res.icons import Icons
from PySide6 import QtCore, QtGui, QtWidgets

from components.gif_component import GifComponent


class SuccessIndicator(QtWidgets.QFrame):
    
    indicator : QtWidgets.QLabel
    in_progress_gif : GifComponent

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)

        if parent:
            self.setMaximumWidth(parent.width()/2)

        self.layout = QtWidgets.QVBoxLayout()
        self.indicator = QtWidgets.QLabel(self)
        self.in_progress_gif = GifComponent(self)
        self.in_progress_gif.setMaximumWidth(self.maximumWidth()/2)
        self.in_progress_gif.set_gif_path("cool_loading_1.gif")
        self.in_progress_gif.hide()
        self.layout.addWidget(self.indicator)
        self.layout.addWidget(self.in_progress_gif)
        self.setLayout(self.layout)
        self.handle_in_progress()

    def handle_success(self):
        self.indicator.setPixmap(QtGui.QPixmap(Icons.SUCCESS_ICON_PATH).scaledToWidth(self.width()))
        self.handle_not_in_progress()
        
    def handle_fail(self):
        self.indicator.setPixmap(QtGui.QPixmap(Icons.FAIL_ICON_PATH).scaledToWidth(self.width()))
        self.handle_not_in_progress()

    def handle_in_progress(self):
        self.indicator.hide()
        self.in_progress_gif.show()

    def handle_not_in_progress(self):
        self.indicator.show()
        self.in_progress_gif.hide()
