"""
Represents a diffraction setup.
Except for energy all units are in SI. Energy is in eV.
"""
from collections import OrderedDict
from copy import deepcopy
import numpy

class DiffractionSetup(object):

    def __init__(self, geometry_type, crystal_name, thickness,
                 miller_h, miller_k, miller_l,
                 asymmetry_angle,
                 energy,
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
        :param energy: The energy.
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
        self._energy = energy
        self._angle_deviation_min = angle_deviation_min
        self._angle_deviation_max = angle_deviation_max
        self._angle_deviation_points = angle_deviation_points
        
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

    def energy(self):
        """
        Returns the energy in eV.
        :return: The energy in eV.
        """
        return self._energy

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
        return numpy.linspace(self.angleDeviationMin(),
                              self.angleDeviationMax(),
                              self.angleDeviationPoints())
        
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
        info_dict["Energy"] = str(self.energy())
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

        if self._energy != candidate._energy:
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