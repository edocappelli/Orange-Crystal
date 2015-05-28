"""
Class to plot arbitrary matrix given as numpy array.
"""

from orangecontrib.crystal.plotting import PlotGenerator, PlotData1D, PlotGeneratorSetting


class NumpyPlotGenerator(PlotGenerator):
    def __init__(self, numpy_array, column_names):
        #super(NumpyPlotGenerator, self).__init__()
        self._column_names = column_names
        PlotGenerator.__init__(self)

        if len(numpy_array.shape) != 2:
            raise Exception("Only matrices are supported (2D numpy array).")

        if numpy_array.shape[1] != len(column_names):
            raise Exception("Number of columns unequals the number of given column names.")

        self._array = numpy_array

    def _defaultSettings(self):
        default_settings = list()

        default_settings.append(PlotGeneratorSetting("Axis X", "Axis X", self._column_names, self._column_names[0]))
        default_settings.append(PlotGeneratorSetting("Axis Y", "Axis Y", self._column_names, self._column_names[-1]))

        return default_settings

    def _plots(self):
        column_name_x = self._settingByName("Axis X").value()
        index_x = self._column_names.index(column_name_x)

        column_name_y = self._settingByName("Axis Y").value()
        index_y = self._column_names.index(column_name_y)

        plot = PlotData1D("%s %s" % (column_name_x, column_name_y),
                          column_name_x,
                          column_name_y)
        plot.setX(self._array[:,index_x])
        plot.setY(self._array[:,index_y])

        return [plot]