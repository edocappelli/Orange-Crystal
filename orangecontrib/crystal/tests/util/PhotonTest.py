import unittest
import numpy as np
from quantities import *

from orangecontrib.crystal.util.Photon import Photon
from orangecontrib.crystal.util.Vector import Vector

class PhotonTest(unittest.TestCase):
    def testConstructor(self):
        photon = Photon(4 * keV, Vector(0, 0, 1))

        self.assertEqual(photon.energy(), 4 * keV)
        self.assertTrue(photon.unitDirectionVector() == Vector(0, 0, 1))

    def testEnergy(self):
        photon = Photon(4 * keV, Vector(0, 0, 1))
        self.assertEqual(photon.energy(), 4 * keV)

    def testWavelength(self):
        test_data = {3 * eV : 413.28 * nm,
                     4 * eV : 309.96 * nm,
                     8 * eV : 154.98 * nm,
                     5 * keV: 2.4797 * angstrom,
                    10 * keV: 1.2398 * angstrom}

        for energy, wavelength in test_data.iteritems():
            photon = Photon(energy, Vector(0, 0, 1))
            self.assertAlmostEqual(photon.wavelength(),
                                   wavelength, 2)

    def testWavenumber(self):
        test_data = {3 * eV : 152031.93111 * cm ** -1,
                     4 * eV : 202709.24149 * cm ** -1,
                     8 * eV : 405418.48298 * cm ** -1,
                     5 * keV: 253386541.53 * cm ** -1,
                    10 * keV: 506773083.07 * cm ** -1}


        for energy, wavenumber in test_data.iteritems():
            photon = Photon(energy, Vector(0, 0, 1))
            self.assertAlmostEqual(photon.wavenumber(),
                                   wavenumber, 1)

    def testWavevector(self):
        direction = Vector(0, 0, 1)
        photon = Photon(5 * keV, direction)

        wavevector = photon.wavevector()

        self.assertAlmostEqual(wavevector.norm().rescale(um **-1),
                               25338.655186 * um ** -1, 1)

        self.assertEqual(wavevector.getNormalizedVector(),
                         direction)

    def testUnitDirectionVector(self):
        photon = Photon(4000, Vector(0, 0, 5))

        self.assertTrue(photon.unitDirectionVector() == Vector(0, 0, 1))
