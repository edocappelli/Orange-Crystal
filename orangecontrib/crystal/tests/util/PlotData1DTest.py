"""
Unittest for PlotData1D class.
"""
import unittest

from collections import OrderedDict

from orangecontrib.crystal.util.PlotData1D import PlotData1D, Autoscale

def plotData1D():
    plot_data_1d = PlotData1D("Title",
                              "x axis",
                              "y axis")
    return plot_data_1d


class PlotData1DTest(unittest.TestCase):
    def testConstructor(self):
        plot_data_1d = plotData1D()
        self.assertIsInstance(plot_data_1d,
                              PlotData1D)
        self.assertEqual(plot_data_1d.title(), "Title")
        self.assertEqual(plot_data_1d.titleXAxis(), "x axis")
        self.assertEqual(plot_data_1d.titleYAxis(), "y axis")

        self.assertIs(plot_data_1d.xMax(),Autoscale)
        self.assertIs(plot_data_1d.xMin(),Autoscale)
        self.assertIs(plot_data_1d.yMax(),Autoscale)
        self.assertIs(plot_data_1d.yMin(),Autoscale)

        self.assertEqual(plot_data_1d.x(),[])
        self.assertEqual(plot_data_1d.y(),[])

        self.assertEqual(plot_data_1d._plot_info,
                         OrderedDict())

    def testSetTitle(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setTitle("a title")
        self.assertEqual(plot_data_1d.title(),
                         "a title")

    def testSetTitleXAxis(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setTitleXAxis("a x title")
        self.assertEqual(plot_data_1d.titleXAxis(),
                         "a x title")

    def testSetTitleYAxis(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setTitleYAxis("a y title")
        self.assertEqual(plot_data_1d.titleYAxis(),
                         "a y title")

    def testSetXMin(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setXMin(-1.1)
        self.assertAlmostEqual(plot_data_1d.xMin(),
                               -1.1)

    def testSetXMax(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setXMax(1.4)
        self.assertAlmostEqual(plot_data_1d.xMax(),
                               1.4)

    def testSetYMin(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setYMin(-2.1)
        self.assertAlmostEqual(plot_data_1d.yMin(),
                               -2.1)

    def testSetYMax(self):
        plot_data_1d = plotData1D()
        plot_data_1d.setYMax(2.4)
        self.assertAlmostEqual(plot_data_1d.yMax(),
                               2.4)

    def testSetX(self):
        plot_data_1d = plotData1D()
        x_data = [0.1, 0.2, 0.3]
        plot_data_1d.setX(x_data)
        self.assertEqual(plot_data_1d.x(), x_data)

    def testSetY(self):
        plot_data_1d = plotData1D()
        y_data = [0.1, 0.2, 0.3]
        plot_data_1d.setY(y_data)
        self.assertEqual(plot_data_1d.y(), y_data)

    def testAddXYPoint(self):
        plot_data_1d = plotData1D()

        plot_data_1d.addXYPoint(0.0,1.0)
        self.assertEqual(plot_data_1d.x(), [0.0])
        self.assertEqual(plot_data_1d.y(), [1.0])

    def testPlotInfo(self):
        plot_data_1d = PlotData1D("Title",
                                  "x axis",
                                  "y axis")

        plot_data_1d.addPlotInfo("a title", "a info")
        self.assertIn("a title", plot_data_1d.plotInfo())
        self.assertEqual(plot_data_1d.plotInfo()["a title"],
                         "a info")