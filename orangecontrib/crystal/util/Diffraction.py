"""
Calculates a crystal diffraction.
Except for energy all units are in SI. Energy is in eV.
"""

import xraylib
from numpy import sin,cos,pi
import scipy.constants.codata

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

    def calculatePsiFromStructureFactor(self, crystal, photon_in, structure_factor):
        codata   = scipy.constants.codata.physical_constants
        classical_electron_radius = codata["classical electron radius"][0]

        volume = crystal['volume'] * 10 ** -30
        psi = (-classical_electron_radius * photon_in.wavelength() ** 2 / (pi * volume)) * structure_factor

        return psi

    def getBraggNormal(self, d_spacing):
        normal_bragg = Vector(0, 0, 1).scalarMultiplication(2.0 * pi / d_spacing)

        return normal_bragg

    def getSurfaceNormal(self, asymmetry_angle):
        normal_surface = Vector(sin(asymmetry_angle / 180.0 * pi),
                                0,
                                cos(asymmetry_angle / 180.0 * pi))

        return normal_surface

    def getIncomingPhotonDirection(self, angle_bragg, deviation):
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

    def _testSetup(self, diffraction_setup, bragg_angle):
        if diffraction_setup.asymmetryAngle() >= bragg_angle * 180 / pi:
            self.log("Impossible geometry...")
        #    exit(-1)


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

        self._testSetup(diffraction_setup, angle_bragg)

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

        self.log( "f0: (%f , %f)" % (F_0.real, F_0.imag))
        self.log( "fH: (%f , %f)" % (F_H.real, F_H.imag))
        self.log( "fHbar: (%f , %f)" % (F_H_bar.real, F_H_bar.imag))

        d_spacing = xraylib.Crystal_dSpacing(crystal,
                                             miller_h,
                                             miller_k,
                                             miller_l) * 1e-10
        self.log( "d_spacing: %f " % d_spacing)

        normal_bragg = self.getBraggNormal(d_spacing)
        normal_surface = self.getSurfaceNormal(diffraction_setup.asymmetryAngle())

        photon_direction = self.getIncomingPhotonDirection(angle_bragg,0.0)
        photon_in = Photon(energy, photon_direction)

        psi_0     = self.calculatePsiFromStructureFactor(crystal, photon_in, F_0)
        psi_H     = self.calculatePsiFromStructureFactor(crystal, photon_in, F_H)
        psi_H_bar = self.calculatePsiFromStructureFactor(crystal, photon_in, F_H_bar)

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

            photon_direction = self.getIncomingPhotonDirection(angle_bragg,
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
