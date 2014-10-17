import unittest
from quantities import *

from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission

class DiffractionSetupTest(unittest.TestCase):
    def testConstructor(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * cm,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=11,
                                             energy=10 * keV,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=175)
        
        self.assertIsInstance(diffraction_setup, DiffractionSetup)

