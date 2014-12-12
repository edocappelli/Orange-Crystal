"""
Unittest for DiffractionResult class.
"""

import unittest

from orangecontrib.crystal.util.ComplexAmplitude import ComplexAmplitude
from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.GeometryType import BraggDiffraction

def diffractionSetup():
    diffraction_setup = DiffractionSetup(BraggDiffraction(),
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
    return diffraction_setup

def diffractionResult():
    diffraction_setup = diffractionSetup()

    bragg_angle = 0.3
    diffraction_result = DiffractionResult(diffraction_setup,
                                               bragg_angle)
    return diffraction_result


class DiffractionResultTest(unittest.TestCase):
    def testConstructor(self):
        diffraction_setup = diffractionSetup()

        bragg_angle = 0.3
        diffraction_result = DiffractionResult(diffraction_setup,
                                               bragg_angle)

        self.assertIsInstance(diffraction_result,
                              DiffractionResult)

        self.assertEqual(diffraction_result._diffraction_setup,
                         diffraction_setup)

        self.assertEqual(diffraction_result._bragg_angle,
                         bragg_angle)

        self.assertEqual(diffraction_result._angle_deviations,
                         [])

        self.assertEqual(diffraction_result._s_reflectivity,
                         [])
        self.assertEqual(diffraction_result._s_phase,
                         [])
        self.assertEqual(diffraction_result._p_reflectivity,
                         [])
        self.assertEqual(diffraction_result._p_phase,
                         [])
        self.assertEqual(diffraction_result._difference_reflectivity,
                         [])
        self.assertEqual(diffraction_result._difference_phase,
                         [])

    def testDiffractionSetup(self):
        diffraction_setup = diffractionSetup()

        bragg_angle = 0.3
        diffraction_result = DiffractionResult(diffraction_setup,
                                               bragg_angle)

        self.assertEqual(diffraction_result.diffractionSetup(),
                         diffraction_setup)


    def testBraggAngle(self):
        diffraction_setup = diffractionSetup()

        bragg_angle = 0.3
        diffraction_result = DiffractionResult(diffraction_setup,
                                               bragg_angle)
        self.assertEqual(diffraction_result.braggAngle(),
                         bragg_angle)

    def testAngleDeviations(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.angleDeviations(),
                         [])

    def testAngles(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.angles(),
                         [])

    def testSIntensity(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.sIntensity(),
                         [])

    def testSPhase(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.sPhase(),
                         [])

    def testPIntensity(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.pIntensity(),
                         [])

    def testPPhase(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.pPhase(),
                         [])

    def testDifferenceIntensity(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.differenceIntensity(),
                         [])

    def testDifferencePhase(self):
        diffraction_result = diffractionResult()
        self.assertEqual(diffraction_result.differencePhase(),
                         [])

    def testAdd(self):
        diffraction_result = diffractionResult()

        deviation = 1e-6

        s_complex_amplitude = ComplexAmplitude(1+1j)
        p_complex_amplitude = ComplexAmplitude(1+2j)
        difference_complex_amplitude = s_complex_amplitude / p_complex_amplitude

        diffraction_result.add(deviation,
                               s_complex_amplitude,
                               p_complex_amplitude,
                               difference_complex_amplitude)

        self.assertAlmostEqual(diffraction_result._angle_deviations,
                               [deviation])
        self.assertAlmostEqual(diffraction_result.sIntensity()[0],2.0)
        self.assertAlmostEqual(diffraction_result.sPhase()[0],0.785398163)
        self.assertAlmostEqual(diffraction_result.pIntensity()[0],5.0)
        self.assertAlmostEqual(diffraction_result.pPhase()[0],1.107148717)
        self.assertAlmostEqual(diffraction_result.differenceIntensity()[0], 0.4)
        self.assertAlmostEqual(diffraction_result.differencePhase()[0],-0.32175055)

    def testAsPlotData2D(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction(),
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

        plot_data_2d = res.asPlotData1D()
        plot_info =  plot_data_2d[0].plotInfo()
        self.assertIn("Geometry Type", plot_info)
        self.assertIn("Crystal Name", plot_info)
        self.assertIn("Miller indices (h,k,l)", plot_info)

        self.assertEqual(plot_info["Geometry Type"], "Bragg diffraction")
        self.assertEqual(plot_info["Crystal Name"], "Si")
        self.assertEqual(plot_info["Miller indices (h,k,l)"], "(1,1,1)")