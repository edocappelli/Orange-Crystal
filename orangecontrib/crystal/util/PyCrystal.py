import numpy as np
from Diffraction import Diffraction
import unittest
import xraylib
from quantities import *
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission, allGeometryTypes

from pylab import plot, show
import matplotlib.pyplot as plt

print("PyCrystal")

possible_geometries=allGeometryTypes()


for index, geometry in enumerate(possible_geometries):
    print("%i %s" % (index, geometry.description()))

geometry_index = int(raw_input("Enter number of geometry (e.g. 0): ")) 

geometry_type = possible_geometries[geometry_index]


crystal_name = raw_input("Crystal name to pass to xraylib (e.g.: Si): ")

try:                          
    crystal = xraylib.Crystal_GetCrystal(crystal_name)
except:
    print("Could not load crystal with name %s" % crystal_name)
    exit(-1)

thickness  = float(raw_input("Thickness in micrometer (e.g. 128.0): ")) * um

miller_h  = int(raw_input("Miller index h (e.g. 1): "))
miller_k  = int(raw_input("Miller index k (e.g. 1): "))
miller_l  = int(raw_input("Miller index l (e.g. 1): "))

energy = float(raw_input("Energy in keV (e.g. 8.0): ")) * keV

angle_deviation_min  = float(raw_input("Min negative angle deviation in microradiant (e.g. -150.0): ")) * 1e-6
angle_deviation_max  = float(raw_input("Max positive angle deviation in microradiant (e.g. 150.0): ")) * 1e-6

angle_deviation_points  = int(raw_input("Angle deviation points (e.g. 200): "))

diffraction = Diffraction()
result = diffraction.calculateDiffraction(geometry_type,
                                          crystal,
                                          thickness,
                                          miller_h,
                                          miller_k,
                                          miller_l,
                                          energy,
                                          angle_deviation_min,
                                          angle_deviation_max,
                                          angle_deviation_points)

result.plot()