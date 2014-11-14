import unittest
import numpy as np

from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission, allGeometryTypes

#debug
from orangecontrib.crystal.widgets.diffraction.PlotViewer2D import PlotViewer2D
from PyQt4 import *
from PyQt4.Qt import *
import sys


class DiffractionTest(unittest.TestCase):

    def assertAlmostEqualLists(self, list1, list2):
        #self.assertAlmostEqual(np.linalg.norm(np.array(list1)-np.array(list2)),0,1)
        ###### TEMPORARY - one digit
        self.assertAlmostEqual(np.linalg.norm(np.array(list1)-np.array(list2)),0,1)


    def assertDiffractionResult(self,s_intensity_fraction, s_phase,p_intensity_fraction, p_phase, diffraction_results):
        self.assertAlmostEqualLists(diffraction_results.sReflectivity(),
                                    s_intensity_fraction)

        self.assertAlmostEqualLists(diffraction_results.sPhase(),
                                    s_phase)

        self.assertAlmostEqualLists(diffraction_results.pReflectivity(),
                                    p_intensity_fraction)

        self.assertAlmostEqualLists(diffraction_results.pPhase(),
                                    p_phase)

    def testConstructor(self):
        diffraction = Diffraction()

    def testCalculateDiffraction(self):

        res = {}
        for geometry_type in allGeometryTypes():
            diffraction_setup = DiffractionSetup(geometry_type,
                                                 "Si",
                                                 thickness=128 * 1e-6,
                                                 miller_h=1,
                                                 miller_k=1,
                                                 miller_l=1,
                                                 asymmetry_angle=0,
                                                 energy=8174 ,
                                                 angle_deviation_min= -20.0e-6,
                                                 angle_deviation_max=20e-6,
                                                 angle_deviation_points=5)
            diffraction = Diffraction()
            res[geometry_type] = diffraction.calculateDiffraction(diffraction_setup)

    def testCalculateBraggDiffraction(self):
        diffraction_setup = DiffractionSetup(BraggDiffraction,
                                             "Si",
                                             thickness=0.0100 * 1e-2,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=3,
                                             energy=10000,
                                             angle_deviation_min= -20.0e-6,
                                             angle_deviation_max=20e-6,
                                             angle_deviation_points=5)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        s_intensity_fraction=[0.01745773309816316, 0.03230557157531512, 0.07938090430258403, 0.9205237023176163, 0.9417346136452986]
        s_phase=[-0.7450035855031368, -0.8040977317553032, -0.7430560369448687, -1.0330253342700109, -2.353084085185629]
        p_intensity_fraction=[0.014207589907369166, 0.02524475838018493, 0.06585710242749995, 0.5225611069541105, 0.9369534929997342]
        p_phase=[-0.7941481534852283, -0.7597894833095722, -0.7493652702052911, -0.8164924894919168, -2.3528205469404995]

        self.assertDiffractionResult(s_intensity_fraction,
                                     s_phase,
                                     p_intensity_fraction,
                                     p_phase,
                                     res)



    def testCalculateBraggTransmission(self):
        diffraction_setup = DiffractionSetup(BraggTransmission,
                                             "Si",
                                             thickness=7 * 1e-6,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle= -5,
                                             energy=10174,
                                             angle_deviation_min= -20.0e-6,
                                             angle_deviation_max=20e-6,
                                             angle_deviation_points=5)

        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        s_intensity_fraction=[0.6227216744425335, 0.6438556927051833, 0.6414246949533766, 0.5964585113516425, 0.4527754471683625]
        s_phase=[2.286899392260667, 2.116030444391057, 1.8763927597551866, 1.445392409430685, -0.013387259911397002]
        p_intensity_fraction=[0.6288315928812124, 0.643693865934977, 0.6259472922778269, 0.5555072803116741, 0.4662075380059585]
        p_phase=[2.424542198713492, 2.2878910989802055, 2.0940387515328434, 1.7467984811760962, 0.8980799769748959]


        self.assertDiffractionResult(s_intensity_fraction,
                                     s_phase,
                                     p_intensity_fraction,
                                     p_phase,
                                     res)



    def testCalculateLaueDiffraction(self):
        diffraction_setup = DiffractionSetup(LaueDiffraction,
                                             "Si",
                                             thickness=100 * 1e-6,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=90,
                                             energy=8000,
                                             angle_deviation_min= -20.0e-6,
                                             angle_deviation_max=20.0e-6,
                                             angle_deviation_points=5)
        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        s_intensity_fraction=[0.09550464832549886, 0.1588102709294371, 0.28442376568534244, 0.15814726060570578, 0.09512692063559264]
        s_phase=[2.791850278765956, -0.8122621895778968, -1.6171710281301908, -1.999035269355459, 0.4153143950080879]
        p_intensity_fraction=[0.0067475416083409515, 0.0927940262113349, 0.1260566388221161, 0.09377613212752883, 0.006829644595304965]
        p_phase=[-1.8538144756209993, 1.69069964224202, 0.9254637256934777, 0.5050050628718205, 2.080546944343358]


        self.assertDiffractionResult(s_intensity_fraction,
                                     s_phase,
                                     p_intensity_fraction,
                                     p_phase,
                                     res)


    def testCalculateLaueTransmission(self):
        diffraction_setup = DiffractionSetup(LaueTransmission,
                                             "Si",
                                             thickness=100 * 1e-6,
                                             miller_h=1,
                                             miller_k=1,
                                             miller_l=1,
                                             asymmetry_angle=90,
                                             energy=10000,
                                             angle_deviation_min= -20.0e-6,
                                             angle_deviation_max=20.0e-6,
                                             angle_deviation_points=5)
        diffraction = Diffraction()
        res = diffraction.calculateDiffraction(diffraction_setup)

        s_intensity_fraction=[0.5005185059940847, 0.3725301844431062, 0.19270321929772727, 0.12894880304002923, 0.25644113466374563]
        s_phase=[2.2288442916782203, -0.23871849735853018, -0.21168003623088033, 0.26050613235172415, -1.8914833995886369]
        p_intensity_fraction=[0.4497098976306458, 0.5758691578045317, 0.48106441586554155, 0.3463440929523105, 0.23745864693751512]
        p_phase=[2.8626116399258565, 0.5331459647248921, 0.1749238966086084, -0.3100000878971298, -2.5858967703879725]


        self.assertDiffractionResult(s_intensity_fraction,
                                     s_phase,
                                     p_intensity_fraction,
                                     p_phase,
                                     res)


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
                                                     thickness=100 * 1e-6,
                                                     miller_h=1,
                                                     miller_k=1,
                                                     miller_l=1,
                                                     asymmetry_angle=effitive_asymmetry,
                                                     energy=energy,
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
                
    def atestBugsByLaurence(self):
        geometries = [ BraggTransmission, LaueTransmission]
        thicknessses = [128 * 1e-6, 5*1e-6]
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
                                                     energy=3124,
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

                        
