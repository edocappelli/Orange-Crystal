import unittest
import numpy as np
from quantities import *

from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission, allGeometryTypes

#debug
from orangecontrib.crystal.widgets.diffraction.PlotViewer2D import PlotViewer2D
from PyQt4 import *
from PyQt4.Qt import *
import sys
#

class DiffractionTest(unittest.TestCase):
    def testConstructor(self):
        diffraction = Diffraction()

    def atestCalculateDiffraction(self):

        res = {}
        for geometry_type in allGeometryTypes():
            diffraction_setup = DiffractionSetup(geometry_type,
                                                 "Si",
                                                 thickness=128 * um,
                                                 miller_h=1,
                                                 miller_k=1,
                                                 miller_l=1,
                                                 asymmetry_angle=0,
                                                 energy=8.174 * keV,
                                                 angle_deviation_min= -150.0e-6,
                                                 angle_deviation_max=150e-6,
                                                 angle_deviation_points=100)
            diffraction = Diffraction()
            res[geometry_type] = diffraction.calculateDiffraction(diffraction_setup)

        print("Close plot window to continue")
        res[BraggDiffraction].plot()

    def atestCalculateBraggDiffraction(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * cm,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=3,
                                             energy=10 * keV,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=150)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        print("Close plot window to continue")
        res.plot()   


    def atestCalculateBraggTransmission(self):
        diffraction_setup = DiffractionSetup(BraggTransmission,
                                             "Si",
                                             thickness=7 * um,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle= -5,
                                             energy=10.174 * keV,
                                             angle_deviation_min= -100.0e-6,
                                             angle_deviation_max=100e-6,
                                             angle_deviation_points=300)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        print("Close plot window to continue")
        res.plot()



    def atestCalculateLaueDiffraction(self):
        diffraction_setup = DiffractionSetup(LaueDiffraction,
                                             "Si",
                                             thickness=100 * um,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=0,
                                             energy=8 * keV,
                                             angle_deviation_min= -0.0e-6,
                                             angle_deviation_max=15.3e-6,
                                             angle_deviation_points=100)
        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        print("Close plot window to continue")
        res.plot()

    def atestCalculateLaueTransmission(self):
        diffraction_setup = DiffractionSetup(LaueTransmission,
                                             "Si",
                                             thickness=100 * um,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=0,
                                             energy=10 * keV,
                                             angle_deviation_min= -15.3e-6,
                                             angle_deviation_max=15.3e-6,
                                             angle_deviation_points=200)
        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        print("Close plot window to continue")
        res.plot()

    def atestXRTDriver(self):
        import orangecontrib.crystal.util.XRTDriver as XRTDriver
        from pylab import plot, show, legend, ylabel, xlabel, title, savefig, figure

        energy = 8100.0
        for geo in allGeometryTypes():
            for asymmetry in [10.0, 0.0, 5.0]:

                res = XRTDriver.calculateDiffraction(E0=energy,
                                                     alpha=asymmetry)

                xrt_res = res[geo]

                effitive_asymmetry = asymmetry 
                if geo is LaueDiffraction or geo is LaueTransmission:
                    effitive_asymmetry = 90.0-asymmetry

                diffraction_setup = DiffractionSetup(geo,
                                                     "Si",
                                                     thickness=100 * um,
                                                     miller_h=1,
                                                     miller_k=1,
                                                     miller_l=1,
                                                     asymmetry_angle=effitive_asymmetry,
                                                     energy=energy * eV,
                                                     angle_deviation_min= -100e-6,
                                                     angle_deviation_max=100e-6,
                                                     angle_deviation_points=300)
                diffraction = Diffraction()
                res = diffraction.calculateDiffraction(diffraction_setup)

                x = [i * 1e+6 for i in res.deviation()]
                plot(x, res.sReflectivity(), label="S polarization")
                x = [i * 1e+6 for i in xrt_res.deviation()]
                plot(x, xrt_res.sReflectivity(), label="XRT S polarization")
                legend()
                title(geo.description())
                ylabel('Reflectivity')
                xlabel("Angle deviation in urad")
                filename = "%s_Asym%i_Reflectivity_S.png" % (geo.description().replace(" ", "_"),
                                                             asymmetry)
                savefig(filename)
                figure()

                x = [i * 1e+6 for i in res.deviation()]
                plot(x, res.pReflectivity(), label="P polarization")
                x = [i * 1e+6 for i in xrt_res.deviation()]
                plot(x, xrt_res.pReflectivity(), label="XRT P polarization")
                legend()
                title(geo.description())
                ylabel('Reflectivity')
                xlabel("Angle deviation in urad")
                filename = "%s_Asym%i_Reflectivity_P.png" % (geo.description().replace(" ", "_"),
                                                             asymmetry)
                savefig(filename)
                figure()

                x = [i * 1e+6 for i in res.deviation()]
                plot(x, res.sPhase(), label="S polarization")
                x = [i * 1e+6 for i in xrt_res.deviation()]
                plot(x, xrt_res.sPhase(), label="XRT S polarization")
                legend()
                title(geo.description())
                ylabel('Phase shift')
                xlabel("Angle deviation in urad")
                filename = "%s_Asym%i_Phase_S.png" % (geo.description().replace(" ", "_"),
                                                             asymmetry)
                savefig(filename)
                figure()

                x = [i * 1e+6 for i in res.deviation()]
                plot(x, res.pPhase(), label="P polarization")
                x = [i * 1e+6 for i in xrt_res.deviation()]
                plot(x, xrt_res.pPhase(), label="XRT P polarization")
                legend()
                title(geo.description())
                ylabel('Phase shift')
                xlabel("Angle deviation in urad")
                filename = "%s_Asym%i_Phase_P.png" % (geo.description().replace(" ", "_"),
                                                             asymmetry)
                savefig(filename)
                figure()
                
    def testBugsByLaurence(self):
        geometries = [ BraggTransmission, LaueTransmission]
        thicknessses = [128 * um, 5*um]
        crystal_names = ["Diamond","Si"]
        asymmetries = [0,10,30,50]
        
        plots = []
        for thickness in thicknessses:
            for crystal_name in crystal_names:
                for asymmetry in asymmetries:
                    effitive_asymmetry = asymmetry
                    for geo in geometries:
                        if geo is LaueDiffraction or geo is LaueTransmission:
                            effitive_asymmetry = 90.0-asymmetry
                        
                        diffraction_setup = DiffractionSetup(geo,
                                                     crystal_name,
                                                     thickness=thickness,
                                                     miller_h=1,
                                                     miller_k=1,
                                                     miller_l=1,
                                                     asymmetry_angle=effitive_asymmetry,
                                                     energy=3124 * eV,
                                                     angle_deviation_min= -120e-6,
                                                     angle_deviation_max=120e-6,
                                                     angle_deviation_points=300)
                        
                        diffraction = Diffraction()
                        try:
                            res = diffraction.calculateDiffraction(diffraction_setup)
                            for p in res.asPlotData2D():
                                plots.append(p)
                        except Exception as ex:
                            print(ex)
                           
        appl = QApplication(sys.argv)
        ow = PlotViewer2D()
        ow.show()
        ow.setPlots(plots)  
        appl.exec_()

                        
