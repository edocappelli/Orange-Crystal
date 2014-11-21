from pylab import plot, show
import matplotlib.pyplot as plt

from orangecontrib.crystal.util.PlotData2D import PlotData2D


class DiffractionResult():
    def __init__(self, diffraction_setup, bragg_angle):
        self._diffraction_setup = diffraction_setup #.clone()
        self._bragg_angle = bragg_angle
        self._deviation = []
        self._s_reflectivity = []
        self._s_phase = []
        self._p_reflectivity = []
        self._p_phase = []
        self._difference_reflectivity = []
        self._difference_phase = []


    def diffractionSetup(self):
        return self._diffraction_setup

    def braggAngle(self):
        return self._bragg_angle

    def deviation(self):
        return self._deviation

    def angle(self):
        return [self.braggAngle() + dev for dev in  self.deviation()]

    def sReflectivity(self):
        return self._s_reflectivity

    def sPhase(self):
        return self._s_phase

    def pReflectivity(self):
        return self._p_reflectivity

    def pPhase(self):
        return self._p_phase

    def differenceReflectivity(self):
        return self._difference_reflectivity

    def differencePhase(self):
        return self._difference_phase

    def add(self, deviation, s_reflectivity_and_phase, p_reflectivity_and_phase, diff_reflectivity_and_phase):
        self._deviation.append(deviation)
        self._s_reflectivity.append(s_reflectivity_and_phase.intensity())
        self._s_phase.append(s_reflectivity_and_phase.phase())
        self._p_reflectivity.append(p_reflectivity_and_phase.intensity())
        self._p_phase.append(p_reflectivity_and_phase.phase())
        self._difference_reflectivity.append(diff_reflectivity_and_phase.intensity())
        self._difference_phase.append(diff_reflectivity_and_phase.phase())

    def plot(self):
        x = [i * 1e+6 for i in self.deviation()]
        plot(x, self.sReflectivity(), label="S polarization")
        plot(x, self.pReflectivity(), label="P polarization")
       # plot(x, self.sPhase(), label="S polarization")
       # plot(x, self.pPhase(), label="P polarization")
        show()
        return
        # Two subplots, unpack the axes array immediately
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
        ax1.set_title('Reflectivity')
        ax2.set_title('Phase shift')


        ax1.set_xlabel("Angle deviation in urad")
        ax1.set_ylabel("Reflectivity")
        s_reflectivity = ax1.plot(x, self.sReflectivity(), label="S polarization")
        p_reflectivity = ax1.plot(x, self.pReflectivity(), label="P polarization")
        ax1.legend()

        ax2.set_xlabel("Angle deviation in urad")
        ax2.set_ylabel("Phase shift in rad")
        s_phase = ax2.plot(x, self.sPhase(), label="S polarization")
        p_phase = ax2.plot(x, self.pPhase(), label="P polarization")

        ax2.legend()

        show()

    def print(self):
        print("s_intensity_fraction="+str(self.sReflectivity()).replace("array(","").replace(") * dimensionless",""))
        print("s_phase="+str(self.sPhase()))

        print("p_intensity_fraction="+str(self.pReflectivity()).replace("array(","").replace(") * dimensionless",""))
        print("p_phase="+str(self.pPhase()))

    def asPlotData2D(self):
        angles = [i * 1e+6 for i in self.deviation()]
        info_dict = self.diffractionSetup().asInfoDictionary()
        info_dict["Bragg angle"] = str(self.braggAngle())
        
        def addPlotInfo(info_dict, plot_data):
            for key, value in info_dict.items():
                plot_data.addPlotInfo(key, value)
        
        s_reflectivity = PlotData2D("Reflectivity - Polarization S",
                                    "Angle deviation in urad",
                                    "Reflectivity")
        s_reflectivity.setX(angles)
        s_reflectivity.setY(self.sReflectivity())
        addPlotInfo(info_dict, s_reflectivity)

        p_reflectivity = PlotData2D("Reflectivity - Polarization P",
                                    "Angle deviation in urad",
                                    "Reflectivity")
        p_reflectivity.setX(angles)
        p_reflectivity.setY(self.pReflectivity())
        addPlotInfo(info_dict, p_reflectivity)
        
        s_phase = PlotData2D("Phase - Polarization S",
                             "Angle deviation in urad",
                             "Phase in rad")
        s_phase.setX(angles)
        s_phase.setY(self.sPhase())
        addPlotInfo(info_dict, s_phase)

        p_phase = PlotData2D("Phase - Polarization P",
                             "Angle deviation in urad",
                             "Phase in rad")
        p_phase.setX(angles)
        p_phase.setY(self.pPhase())  
        addPlotInfo(info_dict, p_phase)

        intensity_difference = PlotData2D("Intensity difference",
                                      "Angle deviation in urad",
                                      "Phase in rad")
        intensity_difference.setX(angles)
        intensity_difference.setY(self.differenceReflectivity())
        addPlotInfo(info_dict, intensity_difference)


        phase_difference = PlotData2D("Phase difference",
                                      "Angle deviation in urad",
                                      "Phase in rad")
        phase_difference.setX(angles)
        phase_difference.setY(self.differencePhase())
        addPlotInfo(info_dict, phase_difference)


        return [s_reflectivity, s_phase,
                p_reflectivity, p_phase,
                intensity_difference, phase_difference
               ]
