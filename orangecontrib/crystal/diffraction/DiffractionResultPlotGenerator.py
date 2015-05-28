"""
Plot Generator for Diffraction results.
"""

from orangecontrib.crystal.plotting.PlotGenerator import PlotGenerator
from orangecontrib.crystal.plotting.PlotData1D import PlotData1D
from orangecontrib.crystal.plotting.PlotGeneratorSetting import PlotGeneratorSetting
from orangecontrib.crystal.util.Enum import Enum

class PlotType(Enum):
    def __init__(self, enum_type):
        super(PlotType, self).__init__(enum_type)


class EnergySweepIntensity(PlotType):
    def __init__(self):
        super(EnergySweepIntensity, self).__init__("energy sweep intensity")


class EnergySweepPhase(PlotType):
    def __init__(self):
        super(EnergySweepPhase, self).__init__("energy sweep phase")


class AngleSweepIntensity(PlotType):
    def __init__(self):
        super(AngleSweepIntensity, self).__init__("angle sweep intensity")


class AngleSweepPhase(PlotType):
    def __init__(self):
        super(AngleSweepPhase, self).__init__("angle sweep phase")


class Polarization(Enum):
    def __init__(self, polarization_name):
        super(Polarization, self).__init__(polarization_name)
        self._name = polarization_name

    def name(self):
        return self._name


class PolarizationS(Polarization):
    def __init__(self):
        super(PolarizationS, self).__init__("Polarization S")


class PolarizationP(Polarization):
    def __init__(self):
        super(PolarizationP, self).__init__("Polarization P")


class PolarizationDifference(Polarization):
    def __init__(self):
        super(PolarizationDifference, self).__init__("Polarization SP Difference")


class DiffractionResultPlotGenerator(PlotGenerator):
    def __init__(self, diffraction_result):
        super(DiffractionResultPlotGenerator, self).__init__()
        self._diffraction_result = diffraction_result

    def _generatePlot(self, plot_type, parameter, polarization, axis_y):
        polarization_name = polarization.name()

        info_dict = self._diffraction_result.diffractionSetup().asInfoDictionary()
        info_dict["Bragg angle"] = str(self._diffraction_result.braggAngle())

        if plot_type == AngleSweepIntensity() or plot_type == AngleSweepPhase():
            # Retrieve angles of the results.
            parameter_name = "Energy"
            axis_x = [i * 1e+6 for i in self._diffraction_result.angleDeviations()]

            if plot_type==AngleSweepIntensity():
                plot_data = PlotData1D("Intensity - " + polarization_name,
                                       "Angle deviation in urad",
                                       "Intensity")

            if plot_type==AngleSweepPhase():
                plot_data = PlotData1D("Phase - " + polarization_name,
                                       "Angle deviation in urad",
                                       "Phase")

        elif plot_type == EnergySweepIntensity() or plot_type == EnergySweepPhase():
            # Retrieve energies of the results.
            parameter_name = "Deviation"
            axis_x = self._diffraction_result.energies()

            if plot_type==EnergySweepIntensity():
                plot_data = PlotData1D("Intensity - " + polarization_name,
                                       "Energy in eV",
                                       "Intensity")

            if plot_type==EnergySweepPhase():
                plot_data = PlotData1D("Phase - " + polarization_name,
                                       "Energy in eV",
                                       "Phase")


        plot_data.setX(axis_x)
        plot_data.setY(axis_y)
        for key, value in info_dict.items():
            plot_data.addPlotInfo(key, value)
        plot_data.addPlotInfo(parameter_name, str(parameter))

        return plot_data

    def _defaultSettings(self):
        default_settings = []

        default_settings.append(PlotGeneratorSetting("Angle sweep", "Include angle sweeps (fixed energy)", bool, True))
        default_settings.append(PlotGeneratorSetting("Energy sweep", "Include energy sweeps (fixed energy)", bool, True))

        default_settings.append(PlotGeneratorSetting("Intensity plot", "Include intensity plots", bool, True))
        default_settings.append(PlotGeneratorSetting("Phase plot", "Include phase plots", bool, True))

        default_settings.append(PlotGeneratorSetting("Polarization S", "Include S polarization", bool, True))
        default_settings.append(PlotGeneratorSetting("Polarization P", "Include P polarization", bool, True))
        default_settings.append(PlotGeneratorSetting("Polarization SP difference", "Include SP difference polarization", bool, True))

        return default_settings

    def _plotTypeFromSettings(self):
        angle_sweep = self._settingByName("Angle sweep")
        energy_sweep = self._settingByName("Energy sweep")
        intensity_plot = self._settingByName("Intensity plot")
        phase_plot = self._settingByName("Phase plot")

        plot_types = []
        if angle_sweep.value() == True:
            if intensity_plot.value() == True:
                plot_types.append(AngleSweepIntensity())
            if phase_plot.value() == True:
                plot_types.append(AngleSweepPhase())

        if energy_sweep.value() == True:
            if intensity_plot.value() == True:
                plot_types.append(EnergySweepIntensity())
            if phase_plot.value() == True:
                plot_types.append(EnergySweepPhase())
        return plot_types

    def _polarizationsFromSettings(self):
        polarization_s = self._settingByName("Polarization S")
        polarization_p = self._settingByName("Polarization P")
        polarization_sp = self._settingByName("Polarization SP difference")

        polarizations = []
        if polarization_s.value() == True:
            polarizations.append(PolarizationS())

        if polarization_p.value() == True:
            polarizations.append(PolarizationP())

        if polarization_sp.value() == True:
            polarizations.append(PolarizationDifference())

        return polarizations

    def _plots(self):
        plots = []
        plot_types = self._plotTypeFromSettings()
        for plot_type in plot_types:

            if plot_type == AngleSweepIntensity() or plot_type == AngleSweepPhase():
                parameters = self._diffraction_result.energies()
            elif plot_type == EnergySweepIntensity() or plot_type == EnergySweepPhase():
                parameters = self._diffraction_result.angleDeviations()

            for parameter in parameters:
                polarizations = self._polarizationsFromSettings()
                for polarization in polarizations:

                    # Angle sweep intensity
                    if plot_type == AngleSweepIntensity():
                        if polarization==PolarizationS():
                            axis_y = self._diffraction_result.sIntensityByEnergy(parameter)

                        if polarization==PolarizationP():
                            axis_y = self._diffraction_result.pIntensityByEnergy(parameter)

                        if polarization==PolarizationDifference():
                            axis_y = self._diffraction_result.differenceIntensityByEnergy(parameter)

                    # Angle sweep phase
                    if plot_type == AngleSweepPhase():
                        if polarization==PolarizationS():
                            axis_y = self._diffraction_result.sPhaseByEnergy(parameter)

                        if polarization==PolarizationP():
                            axis_y = self._diffraction_result.pPhaseByEnergy(parameter)

                        if polarization==PolarizationDifference():
                            axis_y = self._diffraction_result.differencePhaseByEnergy(parameter)

                    # Energy sweep intensity
                    if plot_type == EnergySweepIntensity():
                        if polarization==PolarizationS():
                            axis_y = self._diffraction_result.sIntensityByDeviation(parameter)

                        if polarization==PolarizationP():
                            axis_y = self._diffraction_result.pIntensityByDeviation(parameter)

                        if polarization==PolarizationDifference():
                            axis_y = self._diffraction_result.differenceIntensityByDeviation(parameter)

                    # Energy sweep phase
                    if plot_type == EnergySweepPhase():
                        if polarization==PolarizationS():
                            axis_y = self._diffraction_result.sPhaseByDeviation(parameter)

                        if polarization==PolarizationP():
                            axis_y = self._diffraction_result.pPhaseByDeviation(parameter)

                        if polarization==PolarizationDifference():
                            axis_y = self._diffraction_result.differencePhaseByDeviation(parameter)

                    if len(axis_y)<=1:
                        continue

                    plot = self._generatePlot(plot_type,
                                              parameter,
                                              polarization,
                                              axis_y)

                    plots.append(plot)
        return plots