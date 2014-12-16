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
from Orange.widgets import widget, settings, gui
import Orange.data

from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.PlotData1D import PlotData1D

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
        return self._plotsList()[index]

class PlotViewer1D(widget.OWWidget):
    name = "Plot Viewer 2D"
    description = "Can plot 2D data"
    icon = "icons/screen.svg"

    want_main_area=False
    want_control_area=False

    inputs = [("Crystal diffraction", DiffractionResult, "onDiffractionResult")]
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        # GUI
#        box = gui.widgetBox(self.controlArea, "Plots")
#        self.infoa = gui.widgetLabel(box, '')
#        self.resize(100,50)



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
        self.vbox_plots.addWidget(self.table)
        self.vbox_plots.addWidget(self.btn_screenshot)

        self.vbox_graph.addWidget(self.toolbar)
        self.vbox_graph.addWidget(self.canvas)
        
        self.hbox_plots_graph.addLayout(self.vbox_plots)
        self.hbox_plots_graph.addLayout(self.vbox_graph)
        
        self.layout().addLayout(self.hbox_plots_graph)
        
    def setPlots(self, plots):
        self.model_plots = PlotSetModel(plots)
        self.combobox.setModel(self.model_plots)
        
    def onDiffractionResult(self, diffraction_results):
        #plots = diffraction_results.asPlotData1D()
        plot_generator = diffraction_results.plotGenerator()
        plots = plot_generator.plots()

        self.setPlots(plots)
        self.table.setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.setVisible(True)
        
    def plots_combobox_index_changed(self, index):
        plot = self.combobox.model().plotByIndex(index)
        plot_info = plot.plotInfo()

        self.model_plot_info = PlotInfoModel(plot_info)
        self.table.setModel(self.model_plot_info)
        
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

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
            
                 
    def set_data(self, dataset):
        if dataset is not None:
 #           self.infoa.setText('%d instances in input data set' % len(dataset))
            ind = 1
            #self.send("Sampled Data", sample)
        else:
 #           self.infoa.setText('No data on input yet, waiting to get something.')
            self.send("Sampled Data", None)

if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = PlotViewer1D()
    ow.show()
    appl.exec_()
