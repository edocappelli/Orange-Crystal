"""
Represents a diffraction setup.
Except for energy all units are in SI. Energy is in eV.
"""
from collections import OrderedDict
from copy import deepcopy
import numpy as np
import xraylib

from orangecontrib.crystal.util.Vector import Vector

class DiffractionSetup(object):

    def __init__(self, geometry_type, crystal_name, thickness,
                 miller_h, miller_k, miller_l,
                 asymmetry_angle,
                 energy_min,
                 energy_max,
                 energy_points,
                 angle_deviation_min,
                 angle_deviation_max,
                 angle_deviation_points):
        """
        Constructor.
        :param geometry_type: GeometryType (BraggDiffraction,...).
        :param crystal_name: The name of the crystal, e.g. Si.
        :param thickness: The crystal thickness.
        :param miller_h: Miller index H.
        :param miller_k: Miller index K.
        :param miller_l: Miller index L.
        :param asymmetry_angle: The asymmetry angle between surface normal and Bragg normal.
        :param energy_min: The minimum energy.
        :param energy_max: The maximum energy.
        :param energy_points: Number of energy points.
        :param angle_deviation_min: Minimal angle deviation.
        :param angle_deviation_max: Maximal angle deviation.
        :param angle_deviation_points: Number of deviations points.
        :return:
        """
        self._geometry_type = geometry_type
        self._crystal_name = crystal_name
        self._thickness = thickness
        self._miller_h = miller_h
        self._miller_k = miller_k
        self._miller_l = miller_l
        self._asymmetry_angle = asymmetry_angle
        self._energy_min = energy_min
        self._energy_max = energy_max
        self._energy_points = energy_points
        self._angle_deviation_min = angle_deviation_min
        self._angle_deviation_max = angle_deviation_max
        self._angle_deviation_points = angle_deviation_points

        # Set Debye Waller factor.
        self._debyeWaller = 1.0

        # Load crystal from xraylib.
        self._crystal = xraylib.Crystal_GetCrystal(self.crystalName())

        
    def geometryType(self):
        """
        Returns the GeometryType, e.g. BraggDiffraction, LaueTransmission,...
        :return: The GeometryType.
        """
        return self._geometry_type

    def crystalName(self):
        """
        Return the crystal name, e.g. Si.
        :return: Crystal name.
        """
        return self._crystal_name

    def thickness(self):
        """
        Returns the crystal thickness,
        :return: The crystal thickness.
        """
        return self._thickness

    def millerH(self):
        """
        Returns the Miller H index.
        :return: Miller H index.
        """
        return self._miller_h

    def millerK(self):
        """
        Returns the Miller K index.
        :return: Miller K index.
        """
        return self._miller_k
    
    def millerL(self):
        """
        Returns the Miller L index.
        :return: Miller L index.
        """
        return self._miller_l

    def asymmetryAngle(self):
        """
        Returns the asymmetry angle between surface normal and Bragg normal.
        :return: Asymmetry angle.
        """
        return self._asymmetry_angle

    def energyMin(self):
        """
        Returns the minimum energy in eV.
        :return: The minimum energy in eV.
        """
        return self._energy_min

    def energyMax(self):
        """
        Returns the maximum energy in eV.
        :return: The maximum energy in eV.
        """
        return self._energy_max

    def energyPoints(self):
        """
        Returns the number of energy points.
        :return: Number of energy points.
        """
        return self._energy_points

    def energies(self):
        """
        Returns the energies of this setup.
        :return: The angle deviations grid.
        """
        return np.linspace(self.energyMin(),
                           self.energyMax(),
                           self.energyPoints())

    def angleDeviationMin(self):
        """
        Returns the minimal angle deviation.
        :return: Minimal angle deviation.
        """
        return self._angle_deviation_min

    def angleDeviationMax(self):
        """
        Returns the maximal angle deviation.
        :return: Maximal angle deviation.
        """
        return self._angle_deviation_max

    def angleDeviationPoints(self):
        """
        Returns the angle deviation points.
        :return: Angle deviation points.
        """
        return self._angle_deviation_points
    
    def angleDeviationGrid(self):
        """
        Returns the grid of angle deviations according to this setup.
        :return: The angle deviations grid.
        """
        return np.linspace(self.angleDeviationMin(),
                           self.angleDeviationMax(),
                           self.angleDeviationPoints())

    def angleBragg(self, energy):
        """
        Returns the Bragg angle for a given energy.

        :param energy: Energy to calculate the Bragg angle for.
        :return: Bragg angle.
        """
        energy_in_kev = energy / 1000.0

        # Retrieve bragg angle from xraylib.
        angle_bragg = xraylib.Bragg_angle(self._crystal,
                                          energy_in_kev,
                                          self.millerH(),
                                          self.millerK(),
                                          self.millerL())
        return angle_bragg

    def F0(self, energy):
        energy_in_kev = energy / 1000.0
        F_0 = xraylib.Crystal_F_H_StructureFactor(self._crystal,
                                                  energy_in_kev,
                                                  0, 0, 0,
                                                  self._debyeWaller, 1.0)
        return F_0

    def FH(self, energy):
        energy_in_kev = energy / 1000.0

        F_H = xraylib.Crystal_F_H_StructureFactor(self._crystal,
                                                  energy_in_kev,
                                                  self.millerH(),
                                                  self.millerK(),
                                                  self.millerL(),
                                                  self._debyeWaller, 1.0)
        return F_H

    def FH_bar(self, energy):
        energy_in_kev = energy / 1000.0

        F_H_bar = xraylib.Crystal_F_H_StructureFactor(self._crystal,
                                                      energy_in_kev,
                                                      -self.millerH(),
                                                      -self.millerK(),
                                                      -self.millerL(),
                                                      self._debyeWaller, 1.0)

        return F_H_bar

    def dSpacing(self):
        """
        Returns the lattice spacing d.
        :return: Lattice spacing.
        """

        # Retrieve lattice spacing d from xraylib.
        d_spacing = xraylib.Crystal_dSpacing(self._crystal,
                                             self.millerH(),
                                             self.millerK(),
                                             self.millerL())

        return d_spacing

    def normalBragg(self):
        """
        Calculates the normal on the reflection lattice plane B_H.
        :return: Bragg normal B_H.
        """
        normal_bragg = Vector(0, 0, 1).scalarMultiplication(2.0 * np.pi / (self.dSpacing() * 1e-10))

        return normal_bragg

    def normalSurface(self):
        """
        Calculates surface normal n.
        :param asymmetry_angle: Asymmetry angle of the surface cut.
        :return: Surface normal n.
        """

        assymmetry_angle = self.asymmetryAngle()

        normal_surface = Vector(np.sin(assymmetry_angle / 180.0 * np.pi),
                                0.0,
                                np.cos(assymmetry_angle / 180.0 * np.pi))

        return normal_surface

    def incomingPhotonDirection(self, energy, deviation):
        """
        Calculates the direction of the incoming photon. Parallel to k_0.
        :param angle_bragg: Bragg angle.
        :param deviation: Deviation from the Bragg angle.
        :return: Direction of the incoming photon.
        """
        angle = np.pi / 2.0 - (self.angleBragg(energy) + deviation)

        photon_direction = Vector(-np.sin(angle),
                                  0,
                                  -np.cos(angle))

        return photon_direction

    def unitcellVolume(self):
        """
        Returns the unitcell volume.

        :return: Unitcell volume
        """
        # Retrieve unitcell volume from xraylib.
        unitcell_volume = self._crystal['volume']

        return unitcell_volume

    def asInfoDictionary(self):
        """
        Returns this setup in InfoDictionary form.
        :return: InfoDictionary form of this setup.
        """
        info_dict = OrderedDict()
        info_dict["Geometry Type"] = self.geometryType().description()
        info_dict["Crystal Name"] = self.crystalName()
        info_dict["Thickness"] = str(self.thickness())
        info_dict["Miller indices (h,k,l)"] = "(%i,%i,%i)" % (self.millerH(),
                                                              self.millerK(),
                                                              self.millerL())
        info_dict["Asymmetry Angle"] = str(self.asymmetryAngle())
        info_dict["Minimum energy"] = str(self.energyMin())
        info_dict["Maximum energy"] = str(self.energyMax())
        info_dict["Number of energy points"] = str(self.energyPoints())
        info_dict["Angle deviation minimum"] = "%.2e" % (self.angleDeviationMin())
        info_dict["Angle deviation maximum"] = "%.2e" % (self.angleDeviationMax())
        info_dict["Angle deviation points"] = str(self.angleDeviationPoints())
       
        return info_dict

    def __eq__(self, candidate):
        """
        Determines if two setups are equal.
        :param candidate: Instance to compare to.
        :return: True if the two instances are equal. False otherwise.
        """
        if self._geometry_type != candidate._geometry_type:
            return False

        if self._crystal_name != candidate._crystal_name:
            return False

        if self._thickness != candidate._thickness:
            return False

        if self._miller_h != candidate._miller_h:
            return False

        if self._miller_k != candidate._miller_k:
            return False

        if self._miller_l != candidate._miller_l:
            return False

        if self._asymmetry_angle != candidate._asymmetry_angle:
            return False

        if self._energy_min != candidate._energy_min:
            return False

        if self._energy_max != candidate._energy_max:
            return False

        if self._energy_points != candidate._energy_points:
            return False


        if self._angle_deviation_min != candidate._angle_deviation_min:
            return False

        if self._angle_deviation_max != candidate._angle_deviation_max:
            return False

        if self._angle_deviation_points != candidate._angle_deviation_points:
            return False

        # All members are equal so are the instances.
        return True

    def __ne__(self, candidate):
        """
        Determines if two setups are not equal.
        :param candidate: Instance to compare to.
        :return: True if the two instances are not equal. False otherwise.
        """
        return not self == candidate

    def clone(self):
        """
        Returns a copy of this instance.
        :return: A copy of this instance.
        """
        return deepcopy(self)