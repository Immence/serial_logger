from typing import List

from components.data_containers.device_reading import DeviceReading
from PySide6 import QtCore, QtWidgets


class ReadingListObjectWidget(QtWidgets.QFrame):

    _index_label : QtWidgets.QLabel
    _sg_label : QtWidgets.QLabel
    _freq_label : QtWidgets.QLabel
    _temp_label : QtWidgets.QLabel

    _sg_unit = "SG"
    _freq_unit = "Hz"
    _temp_unit = u"\N{DEGREE SIGN}C"

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.text_layout = QtWidgets.QVBoxLayout()
        self.sg_layout = QtWidgets.QVBoxLayout()
        self.widget_layout = QtWidgets.QHBoxLayout()
        # SG layout items
        self._sg_label = QtWidgets.QLabel()
        self.sg_layout.addWidget(self._sg_label)
        # Upper layout items
        upper_layout = QtWidgets.QHBoxLayout()
        self._freq_label = QtWidgets.QLabel()
        upper_layout.addWidget(self._freq_label, 1, QtCore.Qt.AlignRight)
        # Lower layout items
        lower_layout = QtWidgets.QHBoxLayout()
        self._temp_label = QtWidgets.QLabel()
        lower_layout.addWidget(self._temp_label, 1, QtCore.Qt.AlignRight)
        #Final layout creation
        self._index_label = QtWidgets.QLabel()
        self.text_layout.addLayout(upper_layout)
        self.text_layout.addLayout(lower_layout)
        self.widget_layout.addWidget(self._index_label, 0)
        self.widget_layout.addLayout(self.sg_layout, 1)
        self.widget_layout.addLayout(self.text_layout, 1)
        self.setLayout(self.widget_layout)

    def setIndexLabel(self, index):
        if index == 10:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        else:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self._index_label.setText(str(index))
    
    def setSgLabel(self, sg):
        self._sg_label.setText(f"{str(sg)} {self._sg_unit}")
    def setFreqLabel(self, freq):
        self._freq_label.setText(f"{str(freq)} {self._freq_unit}")
    def setTempLabel(self, temp):
        self._temp_label.setText(f"{str(temp)}  {self._temp_unit}")


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
                widget.setSgLabel(item_data["sg"])
                widget.setFreqLabel(item_data["frequency"])
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

    def update_data(self, readings: List[DeviceReading]):
        self.reading_list_widget.clear()
        for index, reading in enumerate(reversed(readings)):
            list_widget_item = QtWidgets.QListWidgetItem(self.reading_list_widget)
            # store the data needed to create/re-create the custom widget
            list_widget_item.setData(QtCore.Qt.UserRole, {"index": len(readings)-index, **reading.to_dict()})
            self.reading_list_widget.addItem(list_widget_item)
    
    def clear_data(self):
        self.reading_list_widget.clear()

