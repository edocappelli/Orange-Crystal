import unittest
from quantities import *

from orangecontrib.crystal.util.PerfectCrystalDiffraction import PerfectCrystalDiffraction
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission
from orangecontrib.crystal.util.Vector import Vector
from orangecontrib.crystal.util.Photon import Photon

def generatePerfectCrystalDiffraction():

    # Si(111), E=3124eV
    angle_bragg = 0.685283
    psi_0 = -0.00010047702301 -0.00001290853605j
    psi_H = -0.00004446850675 + 0.00003155997069j
    psi_H_bar = -0.00003155997069 -0.00004446850675j
    d_spacing = 3.135416 * angstrom

    geometry_type = LaueTransmission
    normal_bragg = Vector(0,0,1).scalarMultiplication(2.0 * np.pi / d_spacing)
    normal_surface = Vector(1.0,0.0,0.0)

    thickness = 128 * um

    perfect_crystal_diffraction = PerfectCrystalDiffraction(geometry_type,
                                                            normal_bragg,
                                                            normal_surface,
                                                            angle_bragg,
                                                            psi_0,
                                                            psi_H,
                                                            psi_H_bar,
                                                            thickness,
                                                            d_spacing)

    return perfect_crystal_diffraction

def generatePhotonIn():
    direction = Vector(-0.7742395148517507,
                       -0.0,
                       -0.6328927031038719)

    return Photon(3124*eV, direction)

def generatePhotonOut():
    direction = Vector(-0.7742395017022543,
                       0.0,
                       0.6328927191901048)

    return Photon(3124*eV, direction)


class PerfectCrystalDiffractionTest(unittest.TestCase):
    def testConstructor(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        self.assertIsInstance(perfect_crystal_diffraction, PerfectCrystalDiffraction)

        self.assertEqual(perfect_crystal_diffraction.geometryType(),
                         LaueTransmission)
        self.assertEqual(perfect_crystal_diffraction.normalBragg(),
                         Vector(0,0,1).scalarMultiplication(2.0 * np.pi / (3.135416 * angstrom)))
        self.assertEqual(perfect_crystal_diffraction.normalSurface(),
                         Vector(1,0,0))


        self.assertEqual(perfect_crystal_diffraction.angleBragg(),
                         0.685283)

        self.assertAlmostEqual(perfect_crystal_diffraction.Psi0(),
                                -0.00010047702301 -0.00001290853605j)
        self.assertAlmostEqual(perfect_crystal_diffraction.PsiH(),
                               -0.00004446850675 + 0.00003155997069j)
        self.assertAlmostEqual(perfect_crystal_diffraction.PsiHBar(),
                               -0.00003155997069 -0.00004446850675j)
        self.assertAlmostEqual(perfect_crystal_diffraction.dSpacing(),
                               3.135416 * angstrom)
        self.assertAlmostEqual(perfect_crystal_diffraction.thickness(),
                               128 * um)

    def testNormalBragg(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertEqual(perfect_crystal_diffraction.normalBragg(),
                         Vector(0,0,1).scalarMultiplication(2.0 * np.pi / (3.135416 * angstrom)))

    def testNormalSurface(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertEqual(perfect_crystal_diffraction.normalSurface(),
                         Vector(1,0,0))

    def testAngleBragg(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertEqual(perfect_crystal_diffraction.angleBragg(),
                         0.685283)

    def testPsi0(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertAlmostEqual(perfect_crystal_diffraction.Psi0(),
                               -0.00010047702301 -0.00001290853605j)

    def testPsiH(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertAlmostEqual(perfect_crystal_diffraction.PsiH(),
                               -0.00004446850675 + 0.00003155997069j)

    def testPsiHBar(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertAlmostEqual(perfect_crystal_diffraction.PsiHBar(),
                               -0.00003155997069 -0.00004446850675j)

    def testThickness(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertAlmostEqual(perfect_crystal_diffraction.thickness(),
                               128 * um)

    def testDSpacing(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertAlmostEqual(perfect_crystal_diffraction.dSpacing(),
                               3.135416 * angstrom)

    def testGeometryType(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        self.assertEqual(perfect_crystal_diffraction.geometryType(),
                         LaueTransmission)


    def testTompc(self):
        import mpmath

        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        complex_number = 1+3j

        mpc = perfect_crystal_diffraction.tompc(complex_number)

        self.assertAlmostEqual(mpc,complex_number)
        self.assertIsInstance(mpc,mpmath.ctx_mp_python.mpc)


    def testCalculateGamma(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        photon = generatePhotonOut()

        gamma = perfect_crystal_diffraction.calculateGamma(photon)
        self.assertAlmostEqual(gamma,
                               0.7742395148)

        photon = generatePhotonIn()

        gamma = perfect_crystal_diffraction.calculateGamma(photon)
        self.assertAlmostEqual(gamma,
                               0.7742395148)

    def testCalculatePhotonOut(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        photon_in = generatePhotonIn()
        photon_out = perfect_crystal_diffraction.calculatePhotonOut(photon_in)

        self.assertEqual(photon_out,
                         generatePhotonOut())

    def testCalculateZacAlpha(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        zac_alpha = perfect_crystal_diffraction.calculateZacAlpha(generatePhotonIn())
        self.assertAlmostEqual(zac_alpha,
                               1.81e-07)

    def testCalculateZacB(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        self.assertAlmostEqual(zac_b,
                               1.0)

    def testCalculateZacQ(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        zac_q = perfect_crystal_diffraction.calculateZacQ(zac_b,
                                                          perfect_crystal_diffraction.PsiH(),
                                                          perfect_crystal_diffraction.PsiHBar())

        self.assertAlmostEqual(zac_q.real, 2.8068495869e-09, 10)
        self.assertAlmostEqual(zac_q.imag, 9.8141635928e-10, 14)

    def testCalculateZacZ(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        zac_alpha = perfect_crystal_diffraction.calculateZacAlpha(generatePhotonIn())
        zac_z=perfect_crystal_diffraction.calculateZacZ(zac_b, zac_alpha)

        self.assertAlmostEqual(zac_z.real,9.07310664e-08, 14)
        self.assertAlmostEqual(zac_z.imag,1.09617725e-13, 18)

    def testCalculateReflectivity(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        photon_in=generatePhotonIn()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        zac_alpha = perfect_crystal_diffraction.calculateZacAlpha(photon_in)
        zac_q = perfect_crystal_diffraction.calculateZacQ(zac_b,
                                                          perfect_crystal_diffraction.PsiH(),
                                                          perfect_crystal_diffraction.PsiHBar())
        zac_z=perfect_crystal_diffraction.calculateZacZ(zac_b, zac_alpha)
        gamma_0=perfect_crystal_diffraction.calculateGamma(photon_in)
        psi_h_bar=perfect_crystal_diffraction.PsiHBar()

        reflectivity = perfect_crystal_diffraction._calculateReflectivity(photon_in, zac_q, zac_z, gamma_0, psi_h_bar)

        self.assertAlmostEqual(reflectivity.reflectivity(),1.2638962217937542e-05,10)
        self.assertAlmostEqual(reflectivity.phase(),-1.57678799)

    def testCalculatePolarizationS(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        photon_in=generatePhotonIn()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        zac_alpha = perfect_crystal_diffraction.calculateZacAlpha(photon_in)
        zac_z=perfect_crystal_diffraction.calculateZacZ(zac_b, zac_alpha)
        gamma_0=perfect_crystal_diffraction.calculateGamma(photon_in)

        reflectivity = perfect_crystal_diffraction.calculatePolarizationS(photon_in, zac_b, zac_z, gamma_0)

        self.assertAlmostEqual(reflectivity.reflectivity(),1.263896221e-05, 10)
        self.assertAlmostEqual(reflectivity.phase(),-1.57678799)

    def testCalculatePolarizationP(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        photon_in=generatePhotonIn()

        zac_b = perfect_crystal_diffraction.calculateZacB(generatePhotonIn(), generatePhotonOut())
        zac_alpha = perfect_crystal_diffraction.calculateZacAlpha(photon_in)
        zac_z=perfect_crystal_diffraction.calculateZacZ(zac_b, zac_alpha)
        gamma_0=perfect_crystal_diffraction.calculateGamma(photon_in)

        reflectivity = perfect_crystal_diffraction.calculatePolarizationP(photon_in, zac_b, zac_z, gamma_0)

        self.assertAlmostEqual(reflectivity.reflectivity(),6.144079578e-14,19)
        self.assertAlmostEqual(reflectivity.phase(),-1.76339661)

    def testCalculateDiffraction(self):
        perfect_crystal_diffraction = generatePerfectCrystalDiffraction()
        photon_in=generatePhotonIn()

        reflectivity = perfect_crystal_diffraction.calculateDiffraction(photon_in)

        self.assertAlmostEqual(reflectivity["S"].reflectivity(),1.263895932e-05,10)
        self.assertAlmostEqual(reflectivity["S"].phase(),-1.576785742)
        self.assertAlmostEqual(reflectivity["P"].reflectivity(),6.144079578e-14,19)
        self.assertAlmostEqual(reflectivity["P"].phase(),-1.763392341)


