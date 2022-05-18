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

    def handle_result(self, success : bool):
        if success:
            self.indicator.setPixmap(QtGui.QPixmap(Icons.SUCCESS_ICON_PATH).scaledToWidth(self.width()))
            return

        self.indicator.setPixmap(QtGui.QPixmap(Icons.FAIL_ICON_PATH).scaledToWidth(self.width()))
        
    def handle_progress_change(self, progress : bool):
        if progress:
            self.indicator.hide()
            self.in_progress_gif.show()
            return

        self.in_progress_gif.hide()

    def handle_ready_change(self, ready : bool):
        if not ready:
            self.indicator.hide()
            self.in_progress_gif.hide()

    def handle_finish_change(self, finished : bool):
        if not finished:
            self.indicator.hide()
            return
        
        self.indicator.show()

