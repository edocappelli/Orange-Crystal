"""
<name>Plot Viewer 2D</name>
<description>Can plot 2d data</description>
<icon>icons/screen.svg</icon>
<priority>2</priority>
"""
import sys
from PyQt4 import *
from PyQt4.Qt import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

import Orange
from Orange.widgets import widget, gui

from orangecontrib.crystal.util.PlotGenerator import PlotGenerator
from orangecontrib.crystal.util.PlotManager import PlotManager


class PlotInfoModel(QAbstractTableModel):
    def __init__(self, data_dict):
        super(PlotInfoModel, self).__init__()
        self._data_dict = data_dict
        
    def _plotsList(self):
        return self._data_dict
        
    def rowCount(self, index=QModelIndex()):
        return len(self._plotsList())

    def columnCount(self, index=QModelIndex()):
        return 2
    
    def headerData(self, column_offset, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation==Qt.Horizontal:
                if column_offset==0:
                    return "Name"
                if column_offset==1:
                    return "Value"
                
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() \
           or \
           not(0<=index.row()<=len(self._plotsList())):
            print(index.row())
            return QVariant()
        
        if role != Qt.DisplayRole:
            return None
        
        if index.column()==0:
            keys = list(self._plotsList().keys())
            item = keys[int(index.row())]
        elif index.column()==1:
            values = list(self._plotsList().values())
            item = values[int(index.row())]
        else:
            return None
        
        return item

class PlotSetModel(QAbstractTableModel):
    def __init__(self, plots_list):
        super(PlotSetModel, self).__init__()
        self._plots_list = plots_list
        
    def _plotsList(self):
        return self._plots_list
        
    def rowCount(self, index=QModelIndex()):
        return len(self._plotsList())

    def columnCount(self, index=QModelIndex()):
        return 1
    
    def headerData(self, column_offset, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation==Qt.Horizontal:
                if column_offset==0:
                    return "Name"
                
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() \
           or \
           not(0<=index.row()<=len(self._plotsList())):
            print(index.row())
            return QVariant()
        
        if role != Qt.DisplayRole:
            return None
        
        if index.column()==0:
            item = self._plotsList()[int(index.row())]
            item = item.title()
        else:
            return None
        
        return item    
    
    def plotByIndex(self, index):
        plot_list = self._plotsList()

        if index >= len(plot_list) or index < 0:
            return None

        return plot_list[index]

class PlotViewer1D(widget.OWWidget):
    name = "Plot Viewer 1D"
    description = "Can plot 1D data"
    icon = "icons/screen.svg"

    want_main_area=False
    want_control_area=False

    inputs = [("Plots", PlotGenerator, "onPlotGenerator")]
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.combobox = QComboBox()
        self.connect(self.combobox, 
                     SIGNAL("currentIndexChanged(int)"), 
                     self.plots_combobox_index_changed)
        
        self.btn_screenshot = QPushButton("Make screenshot")
        self.connect(self.btn_screenshot, 
                     SIGNAL("pressed(void)"), 
                     self.btn_screenshot_clicked)


        self.hbox_plots_graph = QHBoxLayout()
        self.vbox_plots = QVBoxLayout()        
        self.vbox_plot_settings = QVBoxLayout()
        self.vbox_graph = QVBoxLayout()
        
        self.table = QTableView()


        self.setMinimumHeight(600)
#        self.table.setMinimumWidth(200)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.vbox_plots.addWidget(self.combobox)
        self.vbox_plots.addLayout(self.vbox_plot_settings)
        self.vbox_plots.addWidget(self.table)
        self.vbox_plots.addWidget(self.btn_screenshot)

        self.vbox_graph.addWidget(self.toolbar)
        self.vbox_graph.addWidget(self.canvas)
        
        self.hbox_plots_graph.addLayout(self.vbox_plots)
        self.hbox_plots_graph.addLayout(self.vbox_graph)
        
        self.layout().addLayout(self.hbox_plots_graph)

        self._settings_widgets = []
        self._setPlotManager(PlotManager())

    def _setPlotManager(self, plot_manager):
        self._plot_manager = plot_manager

    def _plotManager(self):
        return self._plot_manager

    def setPlots(self, plots):
        self.model_plots = PlotSetModel(plots)
        self.combobox.setModel(self.model_plots)

    def _updatePlots(self):
        plots = self._plotManager().plots()
        self.setPlots(plots)
        self.table.setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.setVisible(True)

    def _checkBoxStateChanged(self, name, value):
        bool_value = bool(value)
        self._plotManager().setSetting(name, bool_value)
        self._updatePlots()

    def _comboBoxStateChanged(self, name, value):
        str_value = str(value)
        self._plotManager().setSetting(name, str_value)
        self._updatePlots()

    def _widgetFromPlotManagerSetting(self, setting):
        if setting.type() is bool:
            widget = QCheckBox(setting.description(), self)
            widget.setChecked(setting.value())
            handler = lambda x: self._checkBoxStateChanged(setting.name(), x)
            widget.stateChanged.connect(handler)
        elif type(setting.type()) is list:
            widget = QComboBox(self)
            widget.addItems(setting.type())
            handler = lambda x: self._comboBoxStateChanged(setting.name(), x)
            widget.currentIndexChanged[str].connect(handler)
        else:
            raise NotImplemented("PlotManagerSetting type %s not implemented" % str(type(setting.type())))

        return widget

    def _updateSettingsWidgets(self):

        for widget in self._settings_widgets:
            self.vbox_plot_settings.removeWidget(widget)
            widget.deleteLater()

        self._settings_widgets = []

        for setting in self._plotManager().settings():
            widget = self._widgetFromPlotManagerSetting(setting)
            self.vbox_plot_settings.addWidget(widget)
            self._settings_widgets.append(widget)

    def onPlotGenerator(self, plot_generator):
        self._plotManager().setPlotGenerator(plot_generator)
        self._updateSettingsWidgets()
        self._updatePlots()

    def plots_combobox_index_changed(self, index):

        plot = self.combobox.model().plotByIndex(index)

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        if plot is None:
            ax.plot([],[], '*-')
            ax.set_title("")
            ax.set_xlabel("")
            ax.set_ylabel("")
        else:

            plot_info = plot.plotInfo()

            self.model_plot_info = PlotInfoModel(plot_info)
            self.table.setModel(self.model_plot_info)

            # plot data
            ax.plot(plot.x(), plot.y(), '*-')
            ax.set_title(plot.title())
            ax.set_xlabel(plot.titleXAxis())
            ax.set_ylabel(plot.titleYAxis())

        # refresh canvas
        self.canvas.draw()

    def btn_screenshot_clicked(self):
        for i in range(self.combobox.count()):
            self.combobox.setCurrentIndex(i)
            QApplication.processEvents()
            p = QPixmap.grabWindow(self.winId())
            QApplication.processEvents()
            
            plot = self.combobox.model().plotByIndex(i)
            
            plot_info = plot.plotInfo()
            
            type = "phase" if "Phase" in plot.title() else "refl"
            pol = "S" if "S" in plot.title() else "P"
#            type = plot.title().replace(" - ","_").replace(" ","_")

            crystal = plot_info["Crystal Name"] 
            thickness = plot_info["Thickness"].replace(" ","") 
            geometry = plot_info["Geometry Type"].replace(" ","")
            asymmetry = plot_info["Asymmetry Angle"]            
            
            filename = "%s_%s_%s_%s_%s_%s" % (type, 
                                              pol,
                                              crystal,
                                              thickness,
                                              geometry,
                                              asymmetry)
            
            p.save(filename, 'png')
            
if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = PlotViewer1D()
    ow.show()
    appl.exec_()
