# -*- coding: utf-8 -*-
"""
The module compares reflectivity, transmittivity, refraction index,
absorption coefficient etc. with those calculated by XOP.
"""

import os
import sys
import math
#import cmath
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cmath
from pylab import plot, show

import xrt.backends.raycing.materials as rm

from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission

class XRTResult(object):
    def __init__(self):
        self._s_reflectivity = []
        self._p_reflectivity = []
        self._s_phase = []
        self._p_phase = []
        self._deviation = []

    def deviation(self):
        return self._deviation

    def sReflectivity(self):
        return self._s_reflectivity

    def sPhase(self):
        return self._s_phase

    def pReflectivity(self):
        return self._p_reflectivity

    def pPhase(self):
        return self._p_phase

    def plot(self):
        x = [i * 1e+6 for i in self.deviation()]
        plot(x, self.sReflectivity(), label="S polarization")
        plot(x, self.pReflectivity(), label="P polarization")
        show()



def for_one_alpha(crystal, alphaDeg, hkl, geom, E, theta):
    alpha = math.radians(alphaDeg)
    s0 = (np.zeros_like(theta), np.cos(theta + alpha), -np.sin(theta + alpha))
    sh = (np.zeros_like(theta), np.cos(theta - alpha), np.sin(theta - alpha))
    if geom.startswith('Bragg'):
        n = (0, 0, 1)  # outward surface normal
    else:
        n = (0, -1, 0)  # outward surface normal
    hn = (0, math.sin(alpha), math.cos(alpha))  # outward Bragg normal
    gamma0 = sum(i * j for i, j in zip(n, s0))
    gammah = sum(i * j for i, j in zip(n, sh))
    hns0 = sum(i * j for i, j in zip(hn, s0))

    return crystal.get_amplitude(E, gamma0, gammah, hns0)


def calculateDiffraction(hkl='111', E0=10000.0, beamPath=0.1, alpha= -5.0, factDW=1.):
#    alpha = alpha * np.pi / 180.0
    convFactor = 180 / math.pi * 3600.  # arcsec
    if hkl == '111':  # Si111
        dtheta = np.linspace(-100, 100, 400) * 1e-6
        dSpacing = 3.13562
        hklInd = 1, 1, 1
    elif hkl == '333':  # Si333
        dtheta = np.linspace(-30, 30, 400) * 1e-6
        dSpacing = 3.13562 / 3
        hklInd = 3, 3, 3

    thetaCenter = math.asin(rm.ch / (2 * dSpacing * E0))
    t = beamPath * math.sin(thetaCenter)

    geo_types = {BraggDiffraction : 'Bragg reflected',
                 LaueDiffraction  : 'Laue reflected' ,
                 BraggTransmission: 'Bragg transmitted',
                 LaueTransmission : 'Laue transmitted'}

    siCrystal = {}
    cur_S = {}
    cur_P = {}
    result = {}
    for geo, geo_str in geo_types.items():
        current_result = XRTResult()
        t = beamPath * math.cos(thetaCenter)
        siCrystal = rm.CrystalDiamond(hklInd, dSpacing, t=t,
                                           geom=geo_str, factDW=factDW)
        theta = dtheta + thetaCenter
        E = np.ones_like(dtheta) * E0
        cur_S, cur_P = for_one_alpha(siCrystal, alpha, hkl,
                                     geo_str, E, theta)
        current_result._s_reflectivity = abs(cur_S) ** 2
        current_result._p_reflectivity = abs(cur_P) ** 2
        current_result._s_phase = [math.atan(c.imag/c.real) for c in cur_S]
        current_result._p_phase = [math.atan(c.imag/c.real) for c in cur_P]

        current_result._deviation = [i - thetaCenter for i in theta]


        result[geo] = current_result

    return result
