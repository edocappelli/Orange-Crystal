import unittest

from orangecontrib.crystal.util.PlotData2D import PlotData2D


class PlotData2DTest(unittest.TestCase):
    def testConstructor(self):
        plot_data_2d = PlotData2D("Title",
                                  "x axis",
                                  "y axis")
        
        self.assertIsInstance(plot_data_2d,
                              PlotData2D)

    def testPlotInfo(self):
        plot_data_2d = PlotData2D("Title",
                                  "x axis",
                                  "y axis")

        plot_data_2d.addPlotInfo("a title", "a info")
        self.assertIn("a title", plot_data_2d.plotInfo())
        self.assertEqual(plot_data_2d.plotInfo()["a title"],
                         "a info")
