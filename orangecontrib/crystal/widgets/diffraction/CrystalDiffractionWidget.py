"""
<name>Crystal diffraction</name>
<description>Calculates a crystal diffraction pattern</description>
<icon>icons/crystal.svg</icon>
<priority>1</priority>
"""
import sys

# from PyQt4.Qt import *

# from Orange.widgets import widget, settings, gui
from orangewidget import gui
from oasys.widgets import widget
from orangewidget.settings import Setting


from orangecontrib.crystal.diffraction.GeometryType import GeometryType
from orangecontrib.crystal.diffraction.DiffractionExceptions import DiffractionException
from orangecontrib.crystal.diffraction.DiffractionSetupSweeps import DiffractionSetupSweeps
from orangecontrib.crystal.diffraction.Diffraction import Diffraction

from orangecontrib.crystal.plotting.PlotGenerator import PlotGenerator
from orangecontrib.crystal.plotting.DiffractionResultPlotGenerator import DiffractionResultPlotGenerator


class CrystalDiffractionWidget(widget.OWWidget):

    name = "Crystal diffraction"
    description = "Calculates crystal diffraction"
    icon = "icons/crystal.svg"

    want_control_area = False
    want_main_area = False
    outputs = [("Plots", PlotGenerator)]
      
    value_cbb_geometry_type = Setting(0)
    value_cbb_crystal_name = Setting(0)
    value_le_thickness = Setting(0.01)

    value_sp_miller_h = Setting(1)
    value_sp_miller_k = Setting(1)
    value_sp_miller_l = Setting(1)
    
    value_sp_asymmetry_angle = Setting(0)
    value_sp_azimuthal_angle = Setting(0)

    value_le_energy_min = Setting(8.0)
    value_le_energy_max = Setting(8.0)
    value_le_energy_points = Setting(1)

    value_le_angle_min = Setting(-100)
    value_le_angle_max = Setting(100)
    value_le_angle_points = Setting(200)
    
    crystal_names_mapping = {0: "Si",
                             1: "Diamond"}

    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        # GUI
        possible_geometries = GeometryType.allGeometryTypes()
        geometries = [geo.description() for geo in possible_geometries]
        self.geometries_mapping = {}
        for index, geo in enumerate(possible_geometries):
            self.geometries_mapping[index] = geo
            
        self.cbb_geometry_type = gui.comboBox(self,
                                              self,
                                              "value_cbb_geometry_type",
                                              box=None,
                                              label="Geometry type",
                                              items=geometries,
                                              control2attributeDict=self.geometries_mapping)
        
        crystal_names = ["Si",
                         "Diamond"]

        self.cbb_crystal_name = gui.comboBox(self,
                                             self,
                                             "value_cbb_crystal_name",
                                             box=None,
                                             label="Crystal Name",
                                             items=crystal_names,
                                             control2attributeDict=self.crystal_names_mapping)

        self.le_thickness = gui.lineEdit(self,
                                         self,
                                         "value_le_thickness",
                                         label="Thickness [cm]")
        
        self.sp_miller_h = gui.spin(self,
                                    self,
                                    "value_sp_miller_h",
                                    -100000,
                                    100000,
                                    step=1,
                                    label="Miller index h")

        self.sp_miller_k = gui.spin(self,
                                    self,
                                    "value_sp_miller_k",
                                    -100000,
                                    100000,
                                    step=1,
                                    label="Miller index k")

        self.sp_miller_l = gui.spin(self,
                                    self,
                                    "value_sp_miller_l",
                                    -100000,
                                    100000,
                                    step=1,
                                    label="Miller index l")
        
        self.sp_asymmetry_angle = gui.spin(self,
                                           self,
                                           "value_sp_asymmetry_angle",
                                           0,
                                           90,
                                           step=1,
                                           label="Asymmetry angle [deg]")

        self.sp_azimuthal_angle = gui.spin(self,
                                           self,
                                           "value_sp_azimuthal_angle",
                                           0,
                                           90,
                                           step=1,
                                           label="Azimuthal angle [deg]")

        self.le_energy_min = gui.lineEdit(self,
                                          self,
                                          "value_le_energy_min",
                                          label="Minimum energy [keV]")

        self.le_energy_max = gui.lineEdit(self,
                                          self,
                                          "value_le_energy_max",
                                          label="Maximum energy [keV]")

        self.le_energy_points = gui.lineEdit(self,
                                             self,
                                             "value_le_energy_points",
                                             label="Energy points")

        self.le_angle_min = gui.lineEdit(self,
                                         self,
                                         "value_le_angle_min",
                                         label="Angle min [micro rad]")

        self.le_angle_max = gui.lineEdit(self,
                                         self,
                                         "value_le_angle_max",
                                         label="Angle max [micro rad]")

        self.le_angle_points = gui.lineEdit(self,
                                            self,
                                            "value_le_angle_points",
                                            label="Angle points")
        
        self.btn_calculate = gui.button(self,
                                        self,
                                        "Calculate",
                                        self.calculate)
        
    def calculationProgress(self, current, total):
        percent = int(100*float(current)/float(total)) 
        
        if percent <= 11:
            self.progressBarInit()

        self.progressBarSet(percent)
        
        if percent >= 99:
            self.progressBarFinished()
        
    def calculate(self):        
        print(self.value_cbb_geometry_type)
        geometry_type = self.geometries_mapping[self.value_cbb_geometry_type]
        crystal_name = self.crystal_names_mapping[self.value_cbb_crystal_name]

        # Create a diffraction setup.
        diffraction_setup = DiffractionSetupSweeps(geometry_type=geometry_type,
                                                   crystal_name=crystal_name,
                                                   thickness=float(self.value_le_thickness) * 1e-2,
                                                   miller_h=int(self.value_sp_miller_h),
                                                   miller_k=int(self.value_sp_miller_k),
                                                   miller_l=int(self.value_sp_miller_l),
                                                   asymmetry_angle=float(self.value_sp_asymmetry_angle),
                                                   azimuthal_angle=float(self.value_sp_azimuthal_angle),
                                                   energy_min=float(self.value_le_energy_min) * 1e3,
                                                   energy_max=float(self.value_le_energy_max) * 1e3,
                                                   energy_points=int(self.value_le_energy_points),
                                                   angle_deviation_min=float(self.value_le_angle_min) * 1e-6,
                                                   angle_deviation_max=float(self.value_le_angle_max) * 1e-6,
                                                   angle_deviation_points=int(self.value_le_angle_points))
        # Create a Diffraction object.
        diffraction = Diffraction()

        diffraction.setOnProgress(self.calculationProgress)

        # Create a DiffractionResult object holding the results of the diffraction calculations.
        try:
            res = diffraction.calculateDiffraction(diffraction_setup)

        except DiffractionException as de:
            self.showException(de)
            return

        self.send("Plots", DiffractionResultPlotGenerator(res))
        #from PlotViewer2D import PlotViewer2D
        #pv = PlotViewer2D()
        #pv.setPlots(res.asPlotData2D())
        #pv.show()

    def showException(self, exception):
        message_box = gui.QtGui.QMessageBox()
        exception_text=str(exception)
        message_box.setText(exception_text)
        message_box.exec_()

    
# if __name__=="__main__":
    # appl = QApplication(sys.argv)
    # ow = CrystalDiffractionWidget()
    # ow.show()
    # appl.exec_()
