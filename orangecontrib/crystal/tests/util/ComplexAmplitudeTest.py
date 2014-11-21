import unittest
import numpy as np

from orangecontrib.crystal.util.ComplexAmplitude import ComplexAmplitude

class ComplexAmplitudeTest(unittest.TestCase):
    def testConstructor(self):
        
        number = 1 + 2j
        rap = ComplexAmplitude(number)
        
        self.assertAlmostEqual(rap._ComplexAmplitude__complex_amplitude,
                               number)
        
    def testSetComplexAmplitude(self):
        rap = ComplexAmplitude(0)
        number = 1 + 2j
        rap.setComplexAmplitude(number)
        
        self.assertAlmostEqual(rap._ComplexAmplitude__complex_amplitude,
                               number)

    def testReflectivity(self):
        number = 1 + 2j
        rap = ComplexAmplitude(number)

        self.assertAlmostEqual(rap.intensity(),
                               5)

    def testRescale(self):
        number = 1 + 2j
        rap = ComplexAmplitude(number)

        rap.rescale(2.0)

        self.assertAlmostEqual(rap._ComplexAmplitude__complex_amplitude,
                               2+4j)

    def testPhase(self):
        rap = ComplexAmplitude(1 + 1j)

        self.assertAlmostEqual(rap.phase(),
                               np.pi / 4.0)
