from PySide6 import QtWidgets, QtCore, QtGui

GIF_RESOURCES_PATH = "files/res"
class GifComponent(QtWidgets.QLabel):
    
    __gif_path : str
    def __init__(self, parent = None):
        QtWidgets.QLabel.__init__(self, parent)

        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Type.Show:
            self.__on_start()

        elif event.type() == QtCore.QEvent.Type.Hide:
            self.__on_stop()

        return False

    def __on_start(self):
        if self.movie():
            state : QtGui.QMovie.MovieState
            state = self.movie().state()
            if state == QtGui.QMovie.Running:
                return
            else:
                self.movie().start()
        return

    def __on_stop(self):
        if self.movie():
            state : QtGui.QMovie.MovieState
            state = self.movie().state()
            if state == QtGui.QMovie.NotRunning:
                return
            else:
                self.movie().stop()
        return

    def set_gif_path(self, path : str):
        self.__gif_path = path
        self.set_movie()

    def get_gif_path(self) -> str:
        return self.__gif_path

    def set_movie(self):
        movie = QtGui.QMovie(f"{GIF_RESOURCES_PATH}/{self.get_gif_path()}")
        self.setMovie(movie)
        

    
