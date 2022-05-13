from dataclasses import asdict
from typing import List, overload

from components.data_containers.device_reading import DeviceReading
from PySide6 import QtCore, QtWidgets


class QcReadingListObjectWidget(QtWidgets.QFrame):

    _index_label : QtWidgets.QLabel
    _sg_label : QtWidgets.QLabel
    _sg_diff_label : QtWidgets.QLabel
    _freq_label : QtWidgets.QLabel
    _temp_label : QtWidgets.QLabel

    _sg_unit = "SG"
    _freq_unit = "Hz"
    _temp_unit = u"\N{DEGREE SIGN}C"

    outside_threshold : bool = False

    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.text_layout = QtWidgets.QVBoxLayout()
        self.sg_layout = QtWidgets.QVBoxLayout()
        self.reading_stats_layout = QtWidgets.QVBoxLayout()
        self.widget_layout = QtWidgets.QHBoxLayout()
        # SG layout items
        self._sg_label = QtWidgets.QLabel()
        self._sg_diff_label = QtWidgets.QLabel()
        self.sg_layout.addWidget(self._sg_label, alignment=QtCore.Qt.AlignLeft)
        self.sg_layout.addWidget(self._sg_diff_label)

        # Reading stats layout
        self._freq_label = QtWidgets.QLabel()
        self._temp_label = QtWidgets.QLabel()
        self.reading_stats_layout.addWidget(self._freq_label, alignment = QtCore.Qt.AlignRight)
        self.reading_stats_layout.addWidget(self._temp_label, alignment = QtCore.Qt.AlignRight)

        #Final layout creation
        self._index_label = QtWidgets.QLabel()
        self.widget_layout.addWidget(self._index_label, 1)
        self.widget_layout.addLayout(self.sg_layout, 1)
        self.widget_layout.addLayout(self.reading_stats_layout)
        self.setLayout(self.widget_layout)

    def set_data(self, data):
        self.set_index_label(data["index"])
        self.set_sg_label(data["sg"])
        self.set_freq_label(data["frequency"])
        self.set_temp_label(data["temperature"])

        if "sg_diff" and "pass_threshold" in data:
            self.set_sg_diff_label(data["sg_diff"], data["pass_threshold"])
            self.check_outside_threshold(data["sg_diff"], data["pass_threshold"])
        elif "sg_diff" in data:
            self.set_sg_diff_label(data["sg_diff"])
        else:
            self.set_sg_diff_label(None)

    def set_index_label(self, index):
        if index == 10:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        else:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self._index_label.setText(str(index))

    def set_sg_label(self, sg):
        self._sg_label.setText(f"{str(sg)} {self._sg_unit}")
    def set_freq_label(self, freq):
        self._freq_label.setText(f"{str(freq)} {self._freq_unit}")
    def set_temp_label(self, temp):
        self._temp_label.setText(f"{str(temp)}  {self._temp_unit}")
    def set_sg_diff_label(self, sg_diff):
        if sg_diff is None:
            self._sg_diff_label.setText("diff: Not set")
        else:
            self._sg_diff_label.setText(f"diff: {str(sg_diff)} {self._freq_unit}")
    
    def check_outside_threshold(self, sg_diff : str, pass_threshold : str):
        self._sg_diff_label.setText(f"diff: {str(sg_diff)} {self._freq_unit}")
        sg_diff = float(sg_diff)
        pass_threshold = float(pass_threshold)

        if abs(sg_diff) > pass_threshold:
            self.outside_threshold = True


class ReadingListWidget(QtWidgets.QListWidget):
    list_item_type : object

    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)
        self.model().rowsInserted.connect(
            self.handleRowsInserted, QtCore.Qt.QueuedConnection)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def handleRowsInserted(self, parent, first, last):
        for index in range(first, last + 1):
            item = self.item(index)
            if item is not None and self.itemWidget(item) is None:
                widget = self.list_item_type()
                widget.set_data(item.data(QtCore.Qt.UserRole))
                item.setSizeHint(widget.sizeHint())
                self.setItemWidget(item, widget)

    def set_list_item_type(self, list_item_type : object):
        self.list_item_type = list_item_type



#https://pythonshowcase.com/question/dropped-customised-qwidget-item-disappears-in-the-qlistwidget-after-internal-drag-drop-pyside-pyqt
class QcReadingList(QtWidgets.QWidget):  
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.reading_list_widget = ReadingListWidget(self)
        self.reading_list_widget.set_list_item_type(QcReadingListObjectWidget)
        layout.addWidget(self.reading_list_widget)

    def update_data(self, readings: List[DeviceReading], **kwargs):
        self.reading_list_widget.clear()
        for index, reading in enumerate(reversed(readings)):
            list_widget_item = QtWidgets.QListWidgetItem(self.reading_list_widget)
                
            # store the data needed to create/re-create the custom widget
            list_widget_item.setData(QtCore.Qt.UserRole, {"index": len(readings)-index, **asdict(reading), **kwargs})
            self.reading_list_widget.addItem(list_widget_item)
    
    def clear_data(self):
        self.reading_list_widget.clear()
    
    def set_list_item_type(self, list_item_type : object):
        self.reading_list_widget.set_list_item_type(list_item_type)

