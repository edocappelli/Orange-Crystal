from collections import OrderedDict
import copy

class Autoscale(object):
    pass

class PlotData1D():
    """
    Represents a 1D plot. The graph data together with related information.
    """
    def __init__(self, title, title_x_axis, title_y_axis):
        """
        Constructor.
        :param title: Plot title.
        :param title_x_axis: X axis' title.
        :param title_y_axis: Y axis' title.
        """

        # Set titles.
        self.setTitle(title)
        self.setTitleXAxis(title_x_axis)
        self.setTitleYAxis(title_y_axis)

        # Set X and Y ranges to default (autoscaling).
        self.setXMax(Autoscale)
        self.setXMin(Autoscale)
        self.setYMax(Autoscale)
        self.setYMin(Autoscale)

        # Initialize X and Y data.
        self.setX([])
        self.setY([])

        # Initialize plot information to empty ordered dictionary.
        self._plot_info = OrderedDict()

    def setTitle(self, title):
        """
        Sets the plot's title.
        :param title: Plot's title.
        """
        self._title = title

    def title(self):
        """
        Returns the plot's title.
        :return: Title of the plot.
        """
        return self._title

    def setTitleXAxis(self, title_x_axis):
        """
        Sets the x axis title.
        :param title_x_axis: X axis title.
        """
        self._title_x_axis = title_x_axis

    def titleXAxis(self):
        """
        Returns the x axis title.
        :return: X axis title.
        """
        return self._title_x_axis

    def setTitleYAxis(self, title_y_axis):
        """
        Sets the y axis title.
        :param title_y_axis:  Y axis title.
        """
        self._title_y_axis = title_y_axis

    def titleYAxis(self):
        """
        Returns the y axis title.
        :return: Y axis title.
        """
        return self._title_y_axis

    def setXMin(self, x_min):
        """
        Sets x range minimum.
        :param x_min: X range minimum.
        """
        self.x_min = x_min

    def xMin(self):
        """
        Returns x range minimum.
        :return: X range minimum.
        """
        return self.x_min

    def setXMax(self, x_max):
        """
        Sets X range maximum.
        :param x_max: X range maximum.
        """
        self.x_max = x_max

    def xMax(self):
        """
        Returns X range maximum.
        :return: X range maximum.
        """
        return self.x_max

    def setYMin(self, y_min):
        """
        Sets Y range minimum.
        :param y_min: Y range minimum.
        """
        self.y_min = y_min

    def yMin(self):
        """
        Returns Y range minimum.
        :return: Y range minimum.
        """
        return self.y_min

    def setYMax(self, y_max):
        """
        Sets Y range maximum.
        :param y_max: Y range maximum.
        """
        self.y_max = y_max

    def yMax(self):
        """
        Returns Y range maximum.
        :return: Y range maximum.
        """
        return self.y_max

    def setX(self, x):
        """
        Sets X data.
        :param x: X data.
        """
        self._x = x

    def x(self):
        """
        Returns X data.
        :return: X data.
        """
        return self._x

    def setY(self, y):
        """
        Sets Y data.
        :param y: Y data.
        """
        self._y = y

    def y(self):
        """
        Returns Y data.
        :return: Y data.
        """
        return self._y

    def addXYPoint(self, x_point, y_point):
        """
        Adds an x-y point.
        :param x_point: x coordinate.
        :param y_point: y coordinate.
        """
        self._x.append(x_point)
        self._y.append(y_point)
        
    def addPlotInfo(self, name, info):
        """
        Adds a plot info.
        :param name: Name of the info.
        :param info: The info.
        """
        self._plot_info[name] = info
        
    def plotInfo(self):
        """
        Returns the plot info copy.
        :return: The plot info.
        """
        return copy.deepcopy(self._plot_info)