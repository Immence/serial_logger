from PySide6 import QtWidgets, QtCore

from files.res.icons import Icons

class InputWithConfirmation(QtWidgets.QWidget):
    text_field : QtWidgets.QLineEdit
    button_box : QtWidgets.QDialogButtonBox

    emit_input = QtCore.Signal(str)
    emit_hidden = QtCore.Signal()

    def __init__(self, parent : QtWidgets.QWidget = None):
        QtWidgets.QWidget.__init__(self, parent)
        
        # Signal creation stuff

        # Self size stuff
        self.setMaximumHeight(parent.maximumHeight())

        self.installEventFilter(self)

        # Text field stuff
        self.text_field = QtWidgets.QLineEdit()

        # Button stuff
        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.button_box.setMaximumWidth(150)

        # Signal connection stuff
        # Layout stuff
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.text_field, 1)
        self.layout.addWidget(self.button_box, 1)
        self.setLayout(self.layout)
        

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Type.Show:
            self.__connect_signals()

        elif event.type() == QtCore.QEvent.Type.Hide:
            self.text_field.clear()
            self.emit_hidden.emit()
            self.__disconnect_signals()

        return False
    
    def __connect_signals(self):
        pass

    def __disconnect_signals(self):
        pass

    def accept(self):
        self.emit_input.emit(self.text_field.text())
        self.hide()

    def reject(self):
        self.hide()

    def set_text_field_width(self, width : int):
        self.text_field.setMaximumWidth(width)

class ToggleTextEdit(QtWidgets.QWidget):
    __current_text_view : QtWidgets.QLineEdit
    __invisible_padding_box : QtWidgets.QWidget
    __edit_text_view : InputWithConfirmation
    emit_text_change = QtCore.Signal(str)
    
    text_width_max : int = 200
    padding_box_width : int = 150
    
    edit_mode : bool = False

    __toggle_button : QtWidgets.QToolButton
    
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.__toggle_button = QtWidgets.QToolButton(self)
        self.__toggle_button.setIcon(Icons.test_icon())
        self.__toggle_button.clicked.connect(self.handle_toggle_click)
        self.__toggle_button.setMaximumWidth(40)
        self.__toggle_button.setIconSize(QtCore.QSize(20, 20))

        self.__current_text_view = QtWidgets.QLineEdit(self)
        self.__current_text_view.setReadOnly(True)
        self.__current_text_view.setMaximumWidth(self.text_width_max)
        self.set_default_text()
        self.__current_text_view.setObjectName("display-text-view")

        self.__invisible_padding_box = QtWidgets.QWidget(self)
        self.__invisible_padding_box.setMaximumWidth(150)

        self.__edit_text_view = InputWithConfirmation(self)
        self.__edit_text_view.hide()
        self.__edit_text_view.set_text_field_width(self.text_width_max)

        # Connect signals
        self.__edit_text_view.emit_input.connect(self.__handle_text_change)
        self.__edit_text_view.emit_hidden.connect(self.handle_toggle_click)

        # Self display size stuff
        self.setMaximumWidth(self.__toggle_button.width()+self.text_width_max+self.padding_box_width)
        

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.__toggle_button, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.__edit_text_view, 1)
        self.layout.addWidget(self.__current_text_view, 1)
        self.layout.addWidget(self.__invisible_padding_box, 1)
        self.setLayout(self.layout)

    def get_text(self) -> str:
        return self.__current_text_view.text()

    def set_default_text(self, default : str = "Not set") -> None:
        self.__default_text = default
        self.__current_text_view.setText(self.__default_text)
        self.emit_text_change.emit(self.get_text())
    
    def get_default_text(self) -> str:
        return self.__default_text
    
    def __handle_text_change(self, text : str) -> None:
        if text == "":
            return
        self.__current_text_view.setText(text)
        self.emit_text_change.emit(self.get_text())

    def clear(self) -> None:
        self.__current_text_view.clear()
        self.__current_text_view.setText(self.set_default_text())     

    def handle_toggle_click(self) -> None:
        self.edit_mode = not self.edit_mode
        self.__current_text_view.setHidden(self.edit_mode)
        self.__invisible_padding_box.setHidden(self.edit_mode)
        self.__toggle_button.setDisabled(self.edit_mode)
        self.__edit_text_view.setVisible(self.edit_mode)

    def set_text(self, text : str) -> None:
        self.__handle_text_change(text)

    def get_text(self) -> str:
        return self.__current_text_view.text()

class ToggleTextEditWithTitle(QtWidgets.QFrame):

    title : QtWidgets.QLabel
    text_edit : ToggleTextEdit

    emit_text_change = QtCore.Signal(str)

    def __init__(self, parent=None, title: str = "Title not set"):        
        QtWidgets.QFrame.__init__(self, parent)

        self.title = QtWidgets.QLabel(self)
        self.title.setText(title)
        self.text_edit = ToggleTextEdit(self)
        self.text_edit.emit_text_change.connect(self.emit_text_change)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
    
    def set_title(self, title : str) -> None:
        self.title.setText(title)

    def clear(self) -> None:
        self.text_edit.clear()

    def get_title(self) -> str:
        return self.title.text()

    def set_default_text(self, text : str):
        self.text_edit.set_default_text(text)
    
    def set_text(self, text : str):
        self.text_edit.set_text(text)