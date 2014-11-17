import unittest
import numpy as np

from orangecontrib.crystal.util.Diffraction import Diffraction
from orangecontrib.crystal.util.DiffractionSetup import DiffractionSetup
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission, allGeometryTypes

class DiffractionTest(unittest.TestCase):

    def assertAlmostEqualLists(self, list1, list2):
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

        s_intensity_fraction=[0.017519141613069177, 0.0321954521714361, 0.07981125895068454, 0.920965084591721, 0.9417181994525138]
        s_phase=[-0.745427562155594, -0.8048350757616735, -0.7441070552657782, -1.0347178161614214, -2.353510138419943]
        p_intensity_fraction=[0.014173087736472335, 0.025303154305706777, 0.06615101317795873, 0.5244213525516417, 0.9369357917670563]
        p_phase=[-0.793312359389805, -0.7582549664194022, -0.750381901971316, -0.8168058020223106, -2.353282699138147]

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

        s_intensity_fraction=[0.6226567465900791, 0.6438109466925752, 0.6414813069615722, 0.5966674813771604, 0.45178497063185913]
        s_phase=[2.286827125757465, 2.11586718740292, 1.8761281776985377, 1.444935411854202, -0.015769881275207204]
        p_intensity_fraction=[0.6287809489878944, 0.6436830110383608, 0.6260332041734042, 0.5556946212761588, 0.4666570232587092]
        p_phase=[2.4244705128134725, 2.2877506323333496, 2.093850209325308, 1.7465537434885796, 0.8969740263938913]

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

        s_intensity_fraction=[0.0953161518048925, 0.158471134649239, 0.2844237578381098, 0.158487539849245, 0.09531815291902448]
        s_phase=[2.7878364694515985, -0.816280378494231, -1.6227539168093197, -2.0061870787600458, 0.4081575143878531]
        p_intensity_fraction=[0.0067872399580799405, 0.09329690887082268, 0.12605693490089803, 0.09327296207883676, 0.006786852383095909]
        p_phase=[-1.843856553406182, 1.687240781547736, 0.9198814442403762, 0.49730800506928513, 2.059512850321714]

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

        s_intensity_fraction=[0.500009760116572, 0.3730481560147652, 0.1926195176946302, 0.1283757246156211, 0.25695819698222316]
        s_phase=[2.2281966144788545, -0.23994912028908538, -0.215722969718611, 0.25956794505611297, -1.8920272377134075]
        p_intensity_fraction=[0.44963571348593884, 0.5762774883052565, 0.4809772356165785, 0.345952433909957, 0.23751769111657017]
        p_phase=[2.8624375781774436, 0.5308696618055758, 0.1704734474721342, -0.3129214909448153, -2.5856672658533006]

        self.assertDiffractionResult(s_intensity_fraction,
                                     s_phase,
                                     p_intensity_fraction,
                                     p_phase,
                                     res)

    @unittest.skip("Do not test against XRT")
    def testXRTDriver(self):
        import orangecontrib.crystal.util.XRTDriver as XRTDriver
        from pylab import plot, show, legend, ylabel, xlabel, title, savefig, figure

        energy = 8100.0
        for geo in allGeometryTypes():
            for asymmetry in [10.0, 0.0, 5.0]:

                res = XRTDriver.calculateDiffraction(E0=energy,
                                                     alpha=asymmetry)

                xrt_res = res[geo]

                effective_asymmetry = asymmetry
                if geo is LaueDiffraction or geo is LaueTransmission:
                    effective_asymmetry = 90.0-asymmetry

                diffraction_setup = DiffractionSetup(geo,
                                                     "Si",
                                                     thickness=100 * 1e-6,
                                                     miller_h=1,
                                                     miller_k=1,
                                                     miller_l=1,
                                                     asymmetry_angle=effective_asymmetry,
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

    @unittest.skip("Do not produce former bug output.")
    def testBugsByLaurence(self):
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

        import sys
        from orangecontrib.crystal.widgets.diffraction.PlotViewer2D import PlotViewer2D
        from PyQt4.Qt import QApplication

        application = QApplication(sys.argv)
        ow = PlotViewer2D()
        ow.show()
        ow.setPlots(plots)  
        application.exec_()
