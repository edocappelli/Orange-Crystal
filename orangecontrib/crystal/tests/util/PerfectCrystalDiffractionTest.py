import unittest
from quantities import *

from orangecontrib.crystal.util.PerfectCrystalDiffraction import PerfectCrystalDiffraction
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission


class PerfectCrystalDiffractionTest(unittest.TestCase):
    def testConstructor(self):
        perfect_crystaldiffraction = PerfectCrystalDiffraction(geometry_type=None,
                                                               normal_bragg=None,
                                                               normal_surface=None,
                                                               angle_bragg=None,
                                                               psi_0=None,
                                                               psi_H=None,
                                                               psi_H_bar=None,
                                                               thickness=None,
                                                               d_spacing=None)
