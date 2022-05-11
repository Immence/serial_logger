from PySide6 import QtCore, QtWidgets
from typing import List
from components.data_containers.bath_reading import BathReading

class ReadingListObjectWidget(QtWidgets.QFrame):

    _freq_label : QtWidgets.QLabel
    _temp_label : QtWidgets.QLabel
    _index_label : QtWidgets.QLabel

    _freq_unit_label : QtWidgets.QLabel
    _temp_unit_label : QtWidgets.QLabel

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.text_layout = QtWidgets.QVBoxLayout()
        self.widget_layout = QtWidgets.QHBoxLayout()
        # Upper layout items
        upper_layout = QtWidgets.QHBoxLayout()
        self._freq_label = QtWidgets.QLabel()
        self._freq_unit_label = QtWidgets.QLabel("SG")
        upper_layout.addWidget(self._freq_label, 1, QtCore.Qt.AlignHCenter)
        upper_layout.addWidget(self._freq_unit_label)
        # Lower layout items
        lower_layout = QtWidgets.QHBoxLayout()
        self._temp_label = QtWidgets.QLabel()
        self._temp_unit_label = QtWidgets.QLabel(u"\N{DEGREE SIGN}C")
        lower_layout.addWidget(self._temp_label, 1, QtCore.Qt.AlignHCenter)
        lower_layout.addWidget(self._temp_unit_label)
        #Final layout creation
        self._index_label = QtWidgets.QLabel()
        self.text_layout.addLayout(upper_layout)
        self.text_layout.addLayout(lower_layout)
        self.widget_layout.addWidget(self._index_label, 0)
        self.widget_layout.addLayout(self.text_layout, 1)
        self.setLayout(self.widget_layout)

    def setIndexLabel(self, index):
        if index == 10:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self._index_label.setText(str(index))
    def setFreqLabel(self, freq):
        self._freq_label.setText(str(freq))
    def setTempLabel(self, temp):
        self._temp_label.setText(str(temp))


class ReadingListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)
        self.model().rowsInserted.connect(
            self.handleRowsInserted, QtCore.Qt.QueuedConnection)

    def handleRowsInserted(self, parent, first, last):
        for index in range(first, last + 1):
            item = self.item(index)
            if item is not None and self.itemWidget(item) is None:
                item_data = item.data(QtCore.Qt.UserRole)
                widget = ReadingListObjectWidget()
                widget.setIndexLabel(item_data["index"])
                widget.setFreqLabel(item_data["sg"])
                widget.setTempLabel(item_data["temperature"])
                item.setSizeHint(widget.sizeHint())
                self.setItemWidget(item, widget)



#https://pythonshowcase.com/question/dropped-customised-qwidget-item-disappears-in-the-qlistwidget-after-internal-drag-drop-pyside-pyqt
class ReadingList(QtWidgets.QWidget):  
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.reading_list_widget = ReadingListWidget(self)

        layout.addWidget(self.reading_list_widget)

    def update_data(self, readings: List[BathReading]):
        self.reading_list_widget.clear()
        for index, reading in enumerate(reversed(readings)):
            list_widget_item = QtWidgets.QListWidgetItem(self.reading_list_widget)
            # store the data needed to create/re-create the custom widget
            list_widget_item.setData(QtCore.Qt.UserRole, {"index": len(readings)-index, "sg": reading.sg, "temperature": reading.temperature})
            self.reading_list_widget.addItem(list_widget_item)
    
    def clear_data(self):
        self.reading_list_widget.clear()

