from PySide6 import QtWidgets

class CustomDockWidget(QtWidgets.QDockWidget):
    
    windowed : bool = False

    def __init__(self, widget : QtWidgets.QWidget, parent=None, **kwargs):
        QtWidgets.QDockWidget.__init__(self, parent)

        self.setWidget(widget)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        
        for key, value in kwargs.items():
            if key == "windowed" and value == True:
                self.resize(1000, 600)
                self.setHidden(True)
                self.windowed = True
            elif key == "title":
                self.setWindowTitle(value)

    def toggle_window(self):
        if not self.windowed:
            return
        
        if self.isHidden():
            if not self.isFloating():
                self.setFloating(True)
            self.show()
        else:
            self.hide()