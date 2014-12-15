"""
Represents diffraction results.
"""
import numpy
from pylab import plot, show
import matplotlib.pyplot as plt

from orangecontrib.crystal.util.PlotData1D import PlotData1D


class DiffractionResult():

    INDEX_POLARIZATION_S = 0
    INDEX_POLARIZATION_P = 1
    INDEX_DIFFERENCE_SP = 2

    def __init__(self, diffraction_setup, bragg_angle):
        """
        Constructor.
        :param diffraction_setup: Setup used for these results.
        :param bragg_angle: Bragg angle of the setup.
        """
        self._diffraction_setup = diffraction_setup.clone()
        self._bragg_angle = bragg_angle

        number_energies = len(self.energies())
        number_angles = len(self.angleDeviations())
        number_polarizations = 3

        self._intensities = numpy.zeros((number_energies,
                                         number_angles,
                                         number_polarizations))

        self._phases = numpy.zeros((number_energies,
                                    number_angles,
                                    number_polarizations))

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

    def energies(self):
        """
        Returns the energies used for these results.
        :return: Energies used for these results.
        """
        return self._diffraction_setup.energies()

    def _energyIndexByEnergy(self, energy):
        """
        Returns the index of the entry in the energies list that is closest to the given energy.
        :param energy: Energy to find index for.
        :return: Energy index that corresponds to the energy.
        """
        energy_index = abs(self.energies()-energy).argmin()
        return energy_index

    def angleDeviations(self):
        """
        Returns the angle deviations used for these results.
        :return: Angle deviations used for these results.
        """
        return self._diffraction_setup.angleDeviationGrid()

    def _deviationIndexByDeviation(self, deviation):
        """
        Returns the index of the entry in the angle deviations list that is closest to the given deviation.
        :param deviation: Deviation to find index for.
        :return: Deviation index that corresponds to the deviation.
        """
        deviation_index = abs(self.angleDeviations()-deviation).argmin()
        return deviation_index

    def angles(self):
        """
        Returns the angles used for calculation of these results.
        :return: The angles used for the calculation of these results.
        """
        return [self.braggAngle() + dev for dev in  self.angleDeviations()]

    def sIntensity(self, energy):
        """
        Returns the intensity of the S polarization.
        :param energy: Energy to return intensity for.
        :return: Intensity of the S polarization.
        """
        return self._intensities[energy_index, :, self.INDEX_POLARIZATION_S]

    def sPhase(self, energy):
        """
        Returns the phase of the S polarization.
        :param energy: Energy to return phase for.
        :return: Phase of the S polarization.
        """
        return self._phases[0, :, self.INDEX_POLARIZATION_S]

    def pIntensity(self, energy):
        """
        Returns the intensity of the P polarization.
        :param energy: Energy to return intensity for.
        :return: Intensity of the P polarization.
        """
        return self._intensities[0, :, self.INDEX_POLARIZATION_P]

    def pPhase(self, energy):
        """
        Returns the phase of the P polarization.
        :param energy: Energy to return phase for.
        :return: Phase of the P polarization.
        """
        return self._phases[0, :, self.INDEX_POLARIZATION_P]

    def differenceIntensity(self, energy):
        """
        Returns the intensity of the difference between S and P polarizations.
        :param energy: Energy to return intensity for.
        :return: Intensity of the  difference between the S and P polarization.
        """
        return self._intensities[0, :, self.INDEX_DIFFERENCE_SP]

    def differencePhase(self, energy):
        """
        Returns the phase of the difference between S and P polarizations.
        :param energy: Energy to return phase for.
        :return: Phase of the difference between S and P polarization.
        """
        return self._phases[0, :, self.INDEX_DIFFERENCE_SP]

    def add(self, energy, deviation, s_complex_amplitude, p_complex_amplitude, difference_complex_amplitude):
        """
        Adds a result for a given deviation.
        """
        energy_index = self._energyIndexByEnergy(energy)
        deviation_index = self._deviationIndexByDeviation(deviation)

        self._intensities[energy_index, deviation_index, self.INDEX_POLARIZATION_S] = s_complex_amplitude.intensity()
        self._intensities[energy_index, deviation_index, self.INDEX_POLARIZATION_P] = p_complex_amplitude.intensity()
        self._intensities[energy_index, deviation_index, self.INDEX_DIFFERENCE_SP] = difference_complex_amplitude.intensity()

        self._phases[energy_index, deviation_index, self.INDEX_POLARIZATION_S] = s_complex_amplitude.phase()
        self._phases[energy_index, deviation_index, self.INDEX_POLARIZATION_P] = p_complex_amplitude.phase()
        self._phases[energy_index, deviation_index, self.INDEX_DIFFERENCE_SP] = difference_complex_amplitude.phase()

    def asPlotData1D(self):
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

        plots = []
        for energy in self.energies():
            # Intensity S polarization.
            s_intensity = PlotData1D("Intensity - Polarization S",
                                     "Angle deviation in urad",
                                     "Intensity")
            addPlotInfo(info_dict, s_intensity, angles_in_um, self.sIntensity(energy))
            plots.append(s_intensity)

            # Intensity P polarization.
            p_intensity = PlotData1D("Intensity - Polarization P",
                                     "Angle deviation in urad",
                                     "Intensity")
            addPlotInfo(info_dict, p_intensity, angles_in_um, self.pIntensity(energy))
            plots.append(p_intensity)

            # Intensity difference S and P polarization.
            intensity_difference = PlotData1D("Intensity difference",
                                              "Angle deviation in urad",
                                              "Intensity")
            addPlotInfo(info_dict, intensity_difference, angles_in_um, self.differenceIntensity(energy))
            plots.append(intensity_difference)

            # Phase S polarization.
            s_phase = PlotData1D("Phase - Polarization S",
                                 "Angle deviation in urad",
                                 "Phase in rad")
            addPlotInfo(info_dict, s_phase, angles_in_um, self.sPhase(energy))
            plots.append(s_phase)

            # Phase P polarization.
            p_phase = PlotData1D("Phase - Polarization P",
                                 "Angle deviation in urad",
                                 "Phase in rad")
            addPlotInfo(info_dict, p_phase, angles_in_um, self.pPhase(energy))
            plots.append(p_phase)

            # Phase of S and P polarization difference.
            phase_difference = PlotData1D("Phase difference",
                                          "Angle deviation in urad",
                                          "Phase in rad")
            addPlotInfo(info_dict, phase_difference, angles_in_um, self.differencePhase(energy))
            plots.append(phase_difference)

        return plots

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