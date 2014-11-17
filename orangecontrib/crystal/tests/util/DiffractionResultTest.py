import unittest

from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission


class DiffractionResultTest(unittest.TestCase):
    def testConstructor(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * 1e-2,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=3,
                                             energy=10000,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=50)

        diffraction_result = DiffractionResult(diffraction_setup,
                                               1)

    def testAsPlotData2D(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * 1e-2,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=3,
                                             energy=10000,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=50)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        plot_data_2d = res.asPlotData2D()  
        plot_info =  plot_data_2d[0].plotInfo()
        self.assertIn("Geometry Type", plot_info)                 
        self.assertIn("Crystal Name", plot_info)
        self.assertIn("Miller indices (h,k,l)", plot_info)         
        
        self.assertEqual(plot_info["Geometry Type"], "Bragg diffraction")                 
        self.assertEqual(plot_info["Crystal Name"], "Si")
        self.assertEqual(plot_info["Miller indices (h,k,l)"], "(1,1,1)")