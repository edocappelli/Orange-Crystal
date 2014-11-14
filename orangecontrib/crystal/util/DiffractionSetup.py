from collections import OrderedDict
import copy
import numpy

class DiffractionSetup(object):

    def __init__(self, geometry_type, crystal_name, thickness,
                 miller_h, miller_k, miller_l,
                 asymmetry_angle,
                 energy,
                 angle_deviation_min,
                 angle_deviation_max,
                 angle_deviation_points):
        
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
        return self._geometry_type

    def crystalName(self):
        return self._crystal_name

    def thickness(self):
        return self._thickness

    def millerH(self):
        return self._miller_h

    def millerK(self):
        return self._miller_k
    
    def millerL(self):
        return self._miller_l

    def asymmetryAngle(self):
        return self._asymmetry_angle

    def energy(self):
        return self._energy

    def angleDeviationMin(self):
        return self._angle_deviation_min

    def angleDeviationMax(self):
        return self._angle_deviation_max

    def angleDeviationPoints(self):
        return self._angle_deviation_points
    
    def angleDeviationGrid(self):
        return numpy.linspace(self.angleDeviationMin(),
                              self.angleDeviationMax(),
                              self.angleDeviationPoints())
        
    def asInfoDictionary(self):
       info_dict = OrderedDict()
       info_dict["Geometry Type"] = self.geometryType().description()
       info_dict["Crystal Name"] = self.crystalName()
       info_dict["Thickness"] = str(self.thickness())
       info_dict["Miller indices (h,k,l)"] = "(%i,%i,%i)" % (self.millerH(),
                                                             self.millerK(),
                                                             self.millerL())
       info_dict["Asymmetry Angle"] = str(self.asymmetryAngle())
       info_dict["Energy"] = str(self.energy())
       info_dict["Angle deviation minimum"] = str(self.angleDeviationMin())
       info_dict["Angle deviation maximum"] = str(self.angleDeviationMax())
       info_dict["Angle deviation points"] = str(self.angleDeviationPoints())
       
       return info_dict

    def clone(self):
        return copy.deepcopy(self)