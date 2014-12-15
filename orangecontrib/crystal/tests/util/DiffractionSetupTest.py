"""
Unittest for DiffractionSetup class.
"""

import unittest
from quantities import *

import numpy

from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.GeometryType import BraggDiffraction


def diffractionSetup():
    diffraction_setup = DiffractionSetup(BraggDiffraction(),
                                         "Si",
                                         thickness=0.0001,
                                         miller_h=1,
                                         miller_k=1,
                                         miller_l=1,
                                         asymmetry_angle=11,
                                         energy_min=10000,
                                         energy_max=10000,
                                         energy_points=1,
                                         angle_deviation_min=-100.0e-6,
                                         angle_deviation_max=100e-6,
                                         angle_deviation_points=175)
    return diffraction_setup


class DiffractionSetupTest(unittest.TestCase):
    def testConstructor(self):
        diffraction_setup = diffractionSetup()
        self.assertIsInstance(diffraction_setup, DiffractionSetup)

        self.assertEqual(diffraction_setup._geometry_type,
                         BraggDiffraction())
        self.assertEqual(diffraction_setup._crystal_name,
                         "Si")
        self.assertEqual(diffraction_setup._thickness,
                         0.0001)
        self.assertEqual(diffraction_setup._miller_h,
                         1)
        self.assertEqual(diffraction_setup._miller_k,
                         1)
        self.assertEqual(diffraction_setup._miller_l,
                         1)
        self.assertEqual(diffraction_setup._asymmetry_angle,
                         11)
        self.assertEqual(diffraction_setup._energy_min,
                         10000)
        self.assertEqual(diffraction_setup._energy_max,
                         10000)
        self.assertEqual(diffraction_setup._energy_points,
                         1)
        self.assertEqual(diffraction_setup._angle_deviation_min,
                         -100.0e-6)
        self.assertEqual(diffraction_setup._angle_deviation_max,
                         100.0e-6)
        self.assertEqual(diffraction_setup._angle_deviation_points,
                         175)

    def testGeometryType(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.geometryType(),
                         BraggDiffraction())

    def testCrystalName(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.crystalName(),
                         "Si")

    def testThickness(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.thickness(),
                         0.0001)

    def testMillerH(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.millerH(),
                         1)

    def testMillerK(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.millerK(),
                         1)

    def testMillerL(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.millerL(),
                         1)

    def testAsymmetryAngle(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.asymmetryAngle(),
                         11)

    def testEnergyMin(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.energyMin(),
                         10000)

    def testEnergyMax(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.energyMax(),
                         10000)

    def testEnergyMin(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.energyPoints(),
                         1)

    def testAngleDeviationMin(self):
        diffraction_setup = diffractionSetup()
        self.assertAlmostEqual(diffraction_setup.angleDeviationMin(),
                               -100.0e-6)

    def testAngleDeviationMax(self):
        diffraction_setup = diffractionSetup()
        self.assertAlmostEqual(diffraction_setup.angleDeviationMax(),
                               100.0e-6)

    def testAngleDeviationPoints(self):
        diffraction_setup = diffractionSetup()
        self.assertEqual(diffraction_setup.angleDeviationPoints(),
                         175)

    def testAngleDeviationGrid(self):
        diffraction_setup = diffractionSetup()

        self.assertAlmostEqual(numpy.linalg.norm(diffraction_setup.angleDeviationGrid()-numpy.linspace(-100.0e-6, 100.0e-6,175)),
                               0.0)

    def testAsInfoDictionary(self):
        diffraction_setup = diffractionSetup()

        info_dict = diffraction_setup.asInfoDictionary()

        self.assertEqual(info_dict["Geometry Type"],
                         "Bragg diffraction")
        self.assertEqual(info_dict["Crystal Name"],
                         "Si")
        self.assertEqual(info_dict["Thickness"],
                         "0.0001")
        self.assertEqual(info_dict["Miller indices (h,k,l)"],
                         "(1,1,1)")
        self.assertEqual(info_dict["Asymmetry Angle"],
                         "11")
        self.assertEqual(info_dict["Minimum energy"],
                         "10000")
        self.assertEqual(info_dict["Maximum energy"],
                         "10000")
        self.assertEqual(info_dict["Number of energy points"],
                         "1")
        self.assertEqual(info_dict["Angle deviation minimum"],
                         "-1.00e-04")
        self.assertEqual(info_dict["Angle deviation maximum"],
                         "1.00e-04")
        self.assertEqual(info_dict["Angle deviation points"],
                         "175")

    def testOperatorEqual(self):
        diffraction_setup_one = diffractionSetup()
        diffraction_setup_two = DiffractionSetup(BraggDiffraction(),
                                                 "C",
                                                 thickness=0.001,
                                                 miller_h=1,
                                                 miller_k=1,
                                                 miller_l=1,
                                                 asymmetry_angle=11,
                                                 energy_min=8000,
                                                 energy_max=8000,
                                                 energy_points=1,
                                                 angle_deviation_min= -100.0e-6,
                                                 angle_deviation_max=100e-6,
                                                 angle_deviation_points=175)


        self.assertTrue(diffraction_setup_one == diffractionSetup())
        self.assertFalse(diffraction_setup_one == diffraction_setup_two)

    def testOperatorNotEqual(self):
        diffraction_setup_one = diffractionSetup()
        diffraction_setup_two = DiffractionSetup(BraggDiffraction(),
                                                 "C",
                                                 thickness=0.001,
                                                 miller_h=1,
                                                 miller_k=1,
                                                 miller_l=1,
                                                 asymmetry_angle=11,
                                                 energy_min=8000,
                                                 energy_max=8000,
                                                 energy_points=1,
                                                 angle_deviation_min= -100.0e-6,
                                                 angle_deviation_max=100e-6,
                                                 angle_deviation_points=175)


        self.assertTrue(diffraction_setup_one != diffraction_setup_two)
        self.assertFalse(diffraction_setup_one != diffractionSetup())

    def testClone(self):
        diffraction_setup = diffractionSetup()
        clone = diffraction_setup.clone()

        self.assertEqual(diffraction_setup, clone)
        self.assertIsNot(diffraction_setup, clone)