from collections import OrderedDict
import copy

class Autoscale(object):
    pass

class PlotData2D():
    def __init__(self, title, title_x_axis, title_y_axis):
        self.setTitle(title)
        self.setTitleXAxis(title_x_axis)
        self.setTitleYAxis(title_y_axis)

        self.setXMax(Autoscale)
        self.setXMin(Autoscale)
        self.setYMax(Autoscale)
        self.setYMin(Autoscale)
        
        self.setX(None)
        self.setY(None)

        self._plot_info = OrderedDict()

    def setTitle(self, title):
        self._title = title

    def title(self):
        return self._title

    def setTitleXAxis(self, title_x_axis):
        self._title_x_axis = title_x_axis

    def titleXAxis(self):
        return self._title_x_axis

    def setTitleYAxis(self, title_y_axis):
        self._title_y_axis = title_y_axis

    def titleYAxis(self):
        return self._title_y_axis

    def setXMin(self, x_min):
        self.x_min = x_min

    def xMin(self):
        return self.x_min

    def setXMax(self, x_max):
        self.x_max = x_max

    def xMax(self):
        return self.x_max

    def setYMin(self, y_min):
        self.y_min = y_min

    def yMin(self):
        return self.y_min

    def setYMax(self, y_max):
        self.y_min = y_max

    def yMax(self):
        return self.y_max

    def setX(self, x):
        self._x = x

    def x(self):
        return self._x

    def setY(self, y):
        self._y = y

    def y(self):
        return self._y

    def addXY(self, x_point ,y_point):
        self._x.append(x_point)
        self._y.append(y_point)
        
    def addPlotInfo(self, name, info):
        self._plot_info[name] = info
        
    def plotInfo(self):
        return copy.deepcopy(self._plot_info)