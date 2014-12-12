import numpy as np
import unittest

from orangecontrib.crystal.tests.util.VectorTest import VectorTest
from orangecontrib.crystal.tests.util.PhotonTest import PhotonTest
from orangecontrib.crystal.tests.util.ComplexAmplitudeTest import ComplexAmplitudeTest
from orangecontrib.crystal.tests.util.GeometryTypeTest import GeometryTypeTest
from orangecontrib.crystal.tests.util.PerfectCrystalDiffractionTest import PerfectCrystalDiffractionTest
from orangecontrib.crystal.tests.util.DiffractionSetupTest import DiffractionSetupTest
from orangecontrib.crystal.tests.util.DiffractionTest import DiffractionTest
from orangecontrib.crystal.tests.util.DiffractionResultTest import DiffractionResultTest

from orangecontrib.crystal.tests.util.PlotData1DTest import PlotData1DTest
from orangecontrib.crystal.tests.widgets.PlotViewer1DTest import PlotViewer1DTest
from orangecontrib.crystal.tests.widgets.CrystalDiffractionWidgetTest import CrystalDiffractionWidgetTest


def suite():
    suites = (
        unittest.makeSuite(VectorTest, 'test'),
        unittest.makeSuite(PhotonTest, 'test'),
        unittest.makeSuite(ComplexAmplitudeTest, 'test'),
        unittest.makeSuite(GeometryTypeTest, 'test'),

        unittest.makeSuite(PerfectCrystalDiffractionTest, 'test'),
        unittest.makeSuite(DiffractionSetupTest, 'test'),
        unittest.makeSuite(DiffractionTest, 'test'),
        unittest.makeSuite(DiffractionResultTest, 'test'),

        unittest.makeSuite(PlotData1DTest, 'test'),
        unittest.makeSuite(PlotViewer1DTest, 'test'),
        unittest.makeSuite(CrystalDiffractionWidgetTest, 'test'),
    )
    return unittest.TestSuite(suites)


if __name__ == "__main__":
    unittest.main(defaultTest="suite")

