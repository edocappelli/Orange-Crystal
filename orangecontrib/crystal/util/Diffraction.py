import xraylib
import numpy as np
import scipy.constants.codata

from quantities import *
import mpmath
from mpmath import mpc

from orangecontrib.crystal.util.Vector import Vector
from orangecontrib.crystal.util.Photon import Photon
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.PerfectCrystalDiffraction import PerfectCrystalDiffraction
from orangecontrib.crystal.util.ReflectivityAndPhase import ReflectivityAndPhase
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission


class Diffraction():
    
    def __init__(self):
        self.setOnProgress(None)

    def calculatePsiFromStructureFactor(self, crystal, photon_in , F):
        codata = scipy.constants.codata.physical_constants
        codata_r = (codata["classical electron radius"][0]) * meter

        volume = crystal['volume'] * 10 ** -30 * (meter ** 3)
        psi = (-codata_r * photon_in.wavelength() ** 2 / (np.pi * volume)) * F

        return psi

    def getBraggNormal(self, d_spacing):
        normal_bragg = Vector(0, 0, 1)
        normal_bragg = normal_bragg.getNormalizedVector().scalarMultiplication(2.0 * np.pi / d_spacing)
            
        return normal_bragg

    def getSurfaceNormal(self, asymmetry_angle, geometry_type):
        normal_surface = Vector(sin(asymmetry_angle / 180.0 * np.pi),
                                0,
                                cos(asymmetry_angle / 180.0 * np.pi)) 
        #if geometry_type is LaueDiffraction or geometry_type is LaueTransmission:
        #    normal_surface = Vector(1, 0, 0)
            
        return normal_surface
    
    def log(self, str):
        print(str)
        
    def setOnProgress(self, on_progress):
        self._on_progress = on_progress
        
    def _onProgres(self):
        return self._on_progress

    def calculateDiffraction(self, diffraction_setup):

        energy = diffraction_setup.energy()
        miller_h = diffraction_setup.millerH()
        miller_k = diffraction_setup.millerK()
        miller_l = diffraction_setup.millerL()
        
        crystal = xraylib.Crystal_GetCrystal(diffraction_setup.crystalName())

        angle_bragg = xraylib.Bragg_angle(crystal,
                                          float(energy.rescale(keV).magnitude),
                                          miller_h,
                                          miller_k,
                                          miller_l)

        self.log("Bragg angle: %f degrees \n" % (angle_bragg * 180 / np.pi))

        #if diffraction_setup.asymmetryAngle() >= angle_bragg * 180 / np.pi:
        #    self.log("Impossible geometry...")
        #    exit(-1)

        #
        # Get the structure factors (at a given energy)
        #
        debyeWaller = 1.0
        F_0 = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  float(energy.rescale(keV).magnitude),
                                                  0, 0, 0,
                                                  debyeWaller, 1.0)

        F_H = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  float(energy.rescale(keV).magnitude),
                                                  miller_h, miller_k, miller_l,
                                                  debyeWaller, 1.0)

        F_H_bar = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                      float(energy.rescale(keV).magnitude),
                                                      - miller_h, -miller_k, -miller_l,
                                                      debyeWaller, 1.0)

        self.log( "f0: (%f , %f)" % (F_0.real, F_0.imag))
        self.log( "fH: (%f , %f)" % (F_H.real, F_H.imag))

        d_spacing = xraylib.Crystal_dSpacing(crystal,
                                             miller_h,
                                             miller_k,
                                             miller_l) * angstrom

        normal_bragg = self.getBraggNormal(d_spacing)
        normal_surface = self.getSurfaceNormal(diffraction_setup.asymmetryAngle(), 
                                               diffraction_setup.geometryType())

        photon_direction = normal_bragg.getVectorWithAngle(np.pi / 2.0 - angle_bragg)
        photon_in = Photon(energy, photon_direction)

        psi_0 = self.calculatePsiFromStructureFactor(crystal, photon_in, F_0)
        psi_H = self.calculatePsiFromStructureFactor(crystal, photon_in, F_H)
        psi_H_bar = self.calculatePsiFromStructureFactor(crystal, photon_in, F_H_bar)

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
        
        self.log("Calculation start")
        
        for index, deviation in enumerate(diffraction_setup.angleDeviationGrid()):
            if((index + 1) % ten_percent) == 0 \
              or \
              index == diffraction_setup.angleDeviationPoints():
                if self._onProgres() is None:
                    self.log( "Currently calculating point %i of %i" % (index + 1, diffraction_setup.angleDeviationPoints()))
                else:
                    on_progress = self._onProgres()
                    on_progress(index+1, diffraction_setup.angleDeviationPoints())

            angle = np.pi / 2.0 - (angle_bragg + deviation)

            photon_direction = normal_bragg.getVectorWithAngle(angle)
            # Ensure incoming direction
            if(photon_direction.scalarProduct(normal_bragg).magnitude > 0):
                photon_direction = photon_direction.scalarMultiplication(-1.0)
                #photon_direction.printComponents()

            photon_in = Photon(energy, photon_direction)
            res = perfect_crystal.calculateDiffraction(photon_in)
            result.add(deviation,
                       res["S"],
                       res["P"])

        self.log("Calculation end")


        return result
