"""
Manages a set of plots.
"""

class PlotManager(object):
    def __init__(self):
        self.setPlotGenerator(None)
        self.setCurrentPlot(None)
        self._kept_plots=[]
        self._plot_event_handler = []

    def setPlotGenerator(self, plot_generator):
        self._plot_generator = plot_generator

    def _plotGenerator(self):
        return self._plot_generator

    def settings(self):
        return self._plotGenerator().settings()

    def setSetting(self, setting_name, value):
        self._plotGenerator().setSetting(setting_name,
                                          value)

    def plots(self):
        return self._plot_generator.plots()

    def setCurrentPlot(self, plot):
        self._current_plot = plot

    def currentPlot(self):
        return self._current_plot

    def plotByData(self, data):
        return None

    def keepPlot(self, plot):
        self._kept_plots.append(plot)

    def keptPlots(self):
        return self._kept_plots

    def releasePlot(self, plot):
        self._kept_plots.remove(plot)

    def raisePlotEvent(self, plot, event):
        # TODO not nice
        for handled_plot, handler in self._plot_event_handler:
            if handled_plot==plot:
                handler(event)

    def listenPlotEvent(self, plot, handler):
        # TODO not nice
        self._plot_event_handler.append((plot, handler))

    def forgetPlotEvent(self, plot):
        # TODO not nice
        pos = 0
        for index, plot_and_handler in enumerate(self._plot_event_handler):
            if plot_and_handler[0]==plot:
                pos = index
                break

        del self._plot_event_handler[pos]
