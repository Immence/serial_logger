from PySide6 import QtWidgets, QtGui
from files.res.icons import Icons

class BottomToolBar(QtWidgets.QToolBar):

    _serial_monitor_action: QtGui.QAction

    def __init__(self, parent, serial_monitor_action, line_graph_widget_action, scatter_graph_widget_action):
        QtWidgets.QToolBar.__init__(self, parent)
        self._create_actions(serial_monitor_action, line_graph_widget_action, scatter_graph_widget_action)
        self.addAction(self._serial_monitor_action)
        self.addAction(self._line_graph_widget_action)
        self.addAction(self._scatter_graph_widget_action)
        self.setMovable(False)

    def _create_actions(self, serial_monitor_action, line_graph_widget_action, scatter_graph_widget_action):
        self._serial_monitor_action = QtGui.QAction(self)
        self._serial_monitor_action.setText("&Serial Monitor (F1)")
        self._serial_monitor_action.setIcon(Icons.test_icon())
        self._serial_monitor_action.triggered.connect(serial_monitor_action)
        self._serial_monitor_action.setShortcut("F1")

        self._line_graph_widget_action = QtGui.QAction(self)
        self._line_graph_widget_action.setText("&Line Graph widget (F2)")
        self._line_graph_widget_action.setIcon(Icons.line_graph_icon())
        self._line_graph_widget_action.triggered.connect(line_graph_widget_action)
        self._line_graph_widget_action.setShortcut("F2")
        
        self._scatter_graph_widget_action = QtGui.QAction(self)
        self._scatter_graph_widget_action.setText("&Scatter plot widget (F3)")
        self._scatter_graph_widget_action.setIcon(Icons.scatter_plot_icon())
        self._scatter_graph_widget_action.triggered.connect(scatter_graph_widget_action)    
        self._scatter_graph_widget_action.setShortcut("F3")