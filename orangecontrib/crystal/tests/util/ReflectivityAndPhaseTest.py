import unittest
import numpy as np

from orangecontrib.crystal.util.ReflectivityAndPhase import ReflectivityAndPhase

class ReflectivityAndPhaseTest(unittest.TestCase):
    def testConstructor(self):
        
        number = 1 + 2j
        rap = ReflectivityAndPhase(number)
        
        self.assertAlmostEqual(rap._ReflectivityAndPhase__complex_reflexivity,
                               number)
        
    def testSetComplexReflectivity(self):
        rap = ReflectivityAndPhase(0)
        number = 1 + 2j
        rap.setComplexReflectivity(number)
        
        self.assertAlmostEqual(rap._ReflectivityAndPhase__complex_reflexivity,
                               number)

    def testReflectivity(self):
        number = 1 + 2j
        rap = ReflectivityAndPhase(number)

        self.assertAlmostEqual(rap.reflectivity(),
                               5)

    def testRescale(self):
        number = 1 + 2j
        rap = ReflectivityAndPhase(number)

        rap.rescale(2.0)

        self.assertAlmostEqual(rap._ReflectivityAndPhase__complex_reflexivity,
                               2+4j)

    def testPhase(self):
        rap = ReflectivityAndPhase(1 + 1j)

        self.assertAlmostEqual(rap.phase(),
                               np.pi / 4.0)
