from PySide6.QtGui import QFont

class Fonts():

    default_font = "Helvetica"

    @staticmethod
    def title() -> QFont:
        return QFont(Fonts.default_font, pointSize=14, weight=QFont.Bold)

    @staticmethod
    def body() -> QFont:
        return QFont(Fonts.default_font, pointSize=12)
