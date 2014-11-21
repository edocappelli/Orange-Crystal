"""
Represents diffraction results.
"""
from pylab import plot, show
import matplotlib.pyplot as plt

from orangecontrib.crystal.util.PlotData2D import PlotData2D


class DiffractionResult():
    def __init__(self, diffraction_setup, bragg_angle):
        """
        Constructor.
        :param diffraction_setup: Setup used for these results.
        :param bragg_angle: Bragg angle of the setup.
        """
        self._diffraction_setup = diffraction_setup.clone()
        self._bragg_angle = bragg_angle
        self._angle_deviations = []
        self._s_reflectivity = []
        self._s_phase = []
        self._p_reflectivity = []
        self._p_phase = []
        self._difference_reflectivity = []
        self._difference_phase = []

    def diffractionSetup(self):
        """
        Returns the diffraction setup used for the calculation of these results.
        :return: Diffraction setup used for the calculation of these results.
        """
        return self._diffraction_setup

    def braggAngle(self):
        """
        Returns Bragg angle used for these results.
        :return: Bragg angle used for these results.
        """
        return self._bragg_angle

    def angleDeviations(self):
        """
        Returns the angle deviations used for these results.
        :return: Angle deviations used for these results.
        """
        return self._angle_deviations

    def angles(self):
        """
        Returns the angles used for calculation of these results.
        :return: The angles used for the calculation of these results.
        """
        return [self.braggAngle() + dev for dev in  self.angleDeviations()]

    def sIntensity(self):
        """
        Returns the intensity of the S polarization.
        :return: Intensity of the S polarization.
        """
        return self._s_reflectivity

    def sPhase(self):
        """
        Returns the phase of the S polarization.
        :return: Phase of the S polarization.
        """
        return self._s_phase

    def pIntensity(self):
        """
        Returns the intensity of the P polarization.
        :return: Intensity of the P polarization.
        """
        return self._p_reflectivity

    def pPhase(self):
        """
        Returns the phase of the P polarization.
        :return: Phase of the P polarization.
        """
        return self._p_phase

    def differenceIntensity(self):
        """
        Returns the intensity of the difference between S and P polarizations.
        :return: Intensity of the  difference between the S and P polarization.
        """
        return self._difference_reflectivity

    def differencePhase(self):
        """
        Returns the phase of the difference between S and P polarizations.
        :return: Phase of the difference between S and P polarization.
        """
        return self._difference_phase

    def add(self, deviation, s_complex_amplitude, p_complex_amplitude, difference_complex_amplitude):
        """
        Adds a result for a given deviation.
        """
        self._angle_deviations.append(deviation)
        self._s_reflectivity.append(s_complex_amplitude.intensity())
        self._s_phase.append(s_complex_amplitude.phase())
        self._p_reflectivity.append(p_complex_amplitude.intensity())
        self._p_phase.append(p_complex_amplitude.phase())
        self._difference_reflectivity.append(difference_complex_amplitude.intensity())
        self._difference_phase.append(difference_complex_amplitude.phase())

    def asPlotData2D(self):
        """
        Returns this result instance in PlotData2D representation.
        """
        # Retrieve setup information.
        info_dict = self.diffractionSetup().asInfoDictionary()
        info_dict["Bragg angle"] = str(self.braggAngle())

        # Retrieve angles of the results.
        angles_in_um = [i * 1e+6 for i in self.angleDeviations()]

        # Define nested function to duplicate info for every plot.
        def addPlotInfo(info_dict, plot_data, angles_in_um, y):
            plot_data.setX(angles_in_um)
            plot_data.setY(y)
            for key, value in info_dict.items():
                plot_data.addPlotInfo(key, value)

        # Intensity S polarization.
        s_intensity = PlotData2D("Intensity - Polarization S",
                                 "Angle deviation in urad",
                                 "Intensity")
        addPlotInfo(info_dict, s_intensity, angles_in_um, self.sIntensity())

        # Intensity P polarization.
        p_intensity = PlotData2D("Intensity - Polarization P",
                                 "Angle deviation in urad",
                                 "Intensity")
        addPlotInfo(info_dict, p_intensity, angles_in_um, self.pIntensity())

        # Intensity difference S and P polarization.
        intensity_difference = PlotData2D("Intensity difference",
                                          "Angle deviation in urad",
                                          "Intensity")
        addPlotInfo(info_dict, intensity_difference, angles_in_um, self.differenceIntensity())

        # Phase S polarization.
        s_phase = PlotData2D("Phase - Polarization S",
                             "Angle deviation in urad",
                             "Phase in rad")
        addPlotInfo(info_dict, s_phase, angles_in_um, self.sPhase())

        # Phase P polarization.
        p_phase = PlotData2D("Phase - Polarization P",
                             "Angle deviation in urad",
                             "Phase in rad")
        addPlotInfo(info_dict, p_phase, angles_in_um, self.pPhase())

        # Phase of S and P polarization difference.
        phase_difference = PlotData2D("Phase difference",
                                      "Angle deviation in urad",
                                      "Phase in rad")
        addPlotInfo(info_dict, phase_difference, angles_in_um, self.differencePhase())

        return [s_intensity, s_phase,
                p_intensity, p_phase,
                intensity_difference, phase_difference,
               ]

    def _debugPlot(self):
        """
        Debug plot intensities.
        """
        x = [i * 1e+6 for i in self.angleDeviations()]
        plot(x, self.sIntensity(), label="S polarization")
        plot(x, self.pIntensity(), label="P polarization")
       # plot(x, self.sPhase(), label="S polarization")
       # plot(x, self.pPhase(), label="P polarization")
        show()
        return

    def _debugPrint(self):
        """
        Debug print of S and P intensities and phases.
        """
        # S polarization.
        print("s_intensity="+str(self.sIntensity()).replace("array(","").replace(") * dimensionless",""))
        print("s_phase="+str(self.sPhase()))

        # P polarization.
        print("p_intensity="+str(self.pIntensity()).replace("array(","").replace(") * dimensionless",""))
        print("p_phase="+str(self.pPhase()))