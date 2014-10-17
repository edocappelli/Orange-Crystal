import unittest
import sys
from quantities import *
from PyQt4 import *
from PyQt4.Qt import *


from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission

from orangecontrib.crystal.widgets.diffraction.PlotViewer2D import PlotViewer2D


class CrystalDiffractionWidgetTest(unittest.TestCase):
    def testConstructor(self):
#        plot_viewer_2d = PlotViewer2D()
        
#        self.assertIsInstance(plot_viewer_2d,
#                              PlotViewer2D)
        pass

    def testPlotViewer(self):
        appl = QApplication(sys.argv)
        ow = PlotViewer2D()
        ow.show()
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * cm,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=3,
                                             energy=10 * keV,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=50)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        plot_data_2d = res.asPlotData2D()
        ow.setPlots(plot_data_2d)  
        appl.exec_()
