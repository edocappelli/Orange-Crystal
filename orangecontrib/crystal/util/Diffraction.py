"""
Calculates a crystal diffraction.
Except for energy all units are in SI. Energy is in eV.
"""

import xraylib
from numpy import sin,cos,pi
from math import isnan
import scipy.constants.codata
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, BraggTransmission, LaueDiffraction, LaueTransmission

from orangecontrib.crystal.util.Vector import Vector
from orangecontrib.crystal.util.Photon import Photon
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.PerfectCrystalDiffraction import PerfectCrystalDiffraction
from orangecontrib.crystal.util.ReflectivityAndPhase import ReflectivityAndPhase


class Diffraction():
    
    def __init__(self):
        self.setOnCalculationStart(None)
        self.setOnProgress(None)
        self.setOnCalculationEnd(None)

    def _calculatePsiFromStructureFactor(self, crystal, photon_in, structure_factor):
        codata   = scipy.constants.codata.physical_constants
        classical_electron_radius = codata["classical electron radius"][0]

        volume = crystal['volume'] * 10 ** -30
        psi = (-classical_electron_radius * photon_in.wavelength() ** 2 / (pi * volume)) * structure_factor

        return psi

    def _calculateBraggNormal(self, d_spacing):
        normal_bragg = Vector(0, 0, 1).scalarMultiplication(2.0 * pi / d_spacing)

        return normal_bragg

    def _calculateSurfaceNormal(self, asymmetry_angle):
        normal_surface = Vector(sin(asymmetry_angle / 180.0 * pi),
                                0,
                                cos(asymmetry_angle / 180.0 * pi))

        return normal_surface

    def _calculateIncomingPhotonDirection(self, angle_bragg, deviation):
        angle = pi / 2.0 - (angle_bragg + deviation)

        photon_direction = Vector(-sin(angle),
                                  0,
                                  -cos(angle))

        return photon_direction

    def log(self, str):
        print(str)

    def setOnCalculationStart(self, on_calculation_start):
        self._on_calculation_start = on_calculation_start

    def _onCalculationStart(self):
        if self._on_calculation_start is None:
            self.log("Calculating start")
        else:
            self._on_calculation_start()

    def setOnProgress(self, on_progress):
        self._on_progress = on_progress
        
    def _onProgres(self, index, angle_deviation_points):
        if self._on_progress is None:
            self.log( "Currently calculating point %i of %i" % (index, angle_deviation_points))
        else:
            self._on_progress(index, angle_deviation_points)

    def setOnCalculationEnd(self, on_calculation_end):
        self._on_calculation_end = on_calculation_end

    def _onCalculationEnd(self):
        if self._on_calculation_end is None:
            self.log("Calculating end")
        else:
            self._on_calculation_end()

    def _checkSetup(self, diffraction_setup, bragg_angle, F_0, F_H, F_H_bar):
        bragg_angle_in_degree = bragg_angle * 180 / pi

        if diffraction_setup.geometryType() is BraggDiffraction or diffraction_setup.geometryType() is BraggTransmission:
            if diffraction_setup.asymmetryAngle() >= bragg_angle_in_degree:
                raise Exception("Impossible geometry. Asymmetry angle larger than Bragg angle in Bragg geometry. No reflection possible.")
        elif diffraction_setup.geometryType() is LaueDiffraction or diffraction_setup.geometryType() is LaueTransmission:
            if diffraction_setup.asymmetryAngle() <= bragg_angle_in_degree:
                raise Exception("Impossible geometry. Asymmetry angle smaller than Bragg angle in Laue geometry. No transmission possible.")

        if abs(F_0.real) < 1e-7 or isnan(F_0.real):
            raise Exception("Structure factor for F_0 is zero.")

        if abs(F_H.real) < 1e-7 or isnan(F_H.real) or abs(F_H.imag) < 1e-7 or isnan(F_H.imag):
            raise Exception("Structure factor for H=(hkl) is zero. Forbidden reflection for given Miller indices?")

        if abs(F_H_bar.real) < 1e-7 or isnan(F_H_bar.real) or abs(F_H_bar.imag) < 1e-7 or isnan(F_H_bar.imag):
            raise Exception("Structure factor for H_bar=(-h,-k,-l) is zero. Forbidden reflection for given Miller indices?")

    def calculateDiffraction(self, diffraction_setup):

        energy = diffraction_setup.energy()
        energy_in_kev = energy / 1000.0

        miller_h = diffraction_setup.millerH()
        miller_k = diffraction_setup.millerK()
        miller_l = diffraction_setup.millerL()
        
        crystal = xraylib.Crystal_GetCrystal(diffraction_setup.crystalName())

        angle_bragg = xraylib.Bragg_angle(crystal,
                                          energy_in_kev,
                                          miller_h,
                                          miller_k,
                                          miller_l)

        self.log("Bragg angle: %f degrees \n" % (angle_bragg * 180 / pi))

        #
        # Get the structure factors (at a given energy)
        #
        debyeWaller = 1.0
        F_0 = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  energy_in_kev,
                                                  0, 0, 0,
                                                  debyeWaller, 1.0)

        F_H = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  energy_in_kev,
                                                  miller_h, miller_k, miller_l,
                                                  debyeWaller, 1.0)

        F_H_bar = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                      energy_in_kev,
                                                      - miller_h, -miller_k, -miller_l,
                                                      debyeWaller, 1.0)

        self._checkSetup(diffraction_setup, angle_bragg, F_0, F_H, F_H_bar)

        self.log( "f0: (%f , %f)" % (F_0.real, F_0.imag))
        self.log( "fH: (%f , %f)" % (F_H.real, F_H.imag))
        self.log( "fHbar: (%f , %f)" % (F_H_bar.real, F_H_bar.imag))

        d_spacing = xraylib.Crystal_dSpacing(crystal,
                                             miller_h,
                                             miller_k,
                                             miller_l) * 1e-10
        self.log( "d_spacing: %f " % d_spacing)

        normal_bragg = self._calculateBraggNormal(d_spacing)
        normal_surface = self._calculateSurfaceNormal(diffraction_setup.asymmetryAngle())

        photon_direction = self._calculateIncomingPhotonDirection(angle_bragg,0.0)
        photon_in = Photon(energy, photon_direction)

        psi_0     = self._calculatePsiFromStructureFactor(crystal, photon_in, F_0)
        psi_H     = self._calculatePsiFromStructureFactor(crystal, photon_in, F_H)
        psi_H_bar = self._calculatePsiFromStructureFactor(crystal, photon_in, F_H_bar)

        self.log( "psi0: (%.14f , %.14f)" % (psi_0.real, psi_0.imag))
        self.log( "psiH: (%.14f , %.14f)" % (psi_H.real, psi_H.imag))
        self.log( "psiHbar: (%.14f , %.14f)" % (psi_H_bar.real, psi_H_bar.imag))

        perfect_crystal = PerfectCrystalDiffraction(diffraction_setup.geometryType(),
                                                    normal_bragg,
                                                    normal_surface,
                                                    angle_bragg,
                                                    psi_0,
                                                    psi_H,
                                                    psi_H_bar,
                                                    diffraction_setup.thickness(),
                                                    d_spacing)

        result = DiffractionResult(diffraction_setup, angle_bragg)
        ten_percent = diffraction_setup.angleDeviationPoints() / 10
        
        self._onCalculationStart()
        
        for index, deviation in enumerate(diffraction_setup.angleDeviationGrid()):
            if((index + 1) % ten_percent) == 0 \
              or \
              index == diffraction_setup.angleDeviationPoints():
                self._onProgres(index+1, diffraction_setup.angleDeviationPoints())

            photon_direction = self._calculateIncomingPhotonDirection(angle_bragg,
                                                               deviation)

            photon_in = Photon(energy, photon_direction)
            res = perfect_crystal.calculateDiffraction(photon_in)

            difference = ReflectivityAndPhase(res["S"].complexAmplitude() / res["P"].complexAmplitude())

            result.add(deviation,
                       res["S"],
                       res["P"],
                       difference)

        self._onCalculationEnd()

        return result