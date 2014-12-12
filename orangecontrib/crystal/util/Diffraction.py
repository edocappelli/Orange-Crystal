"""
Calculates a crystal diffraction.
Except for energy all units are in SI. Energy is in eV.
"""

import xraylib
from numpy import sin,cos,pi
from math import isnan
import scipy.constants.codata
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, BraggTransmission, LaueDiffraction, LaueTransmission

from orangecontrib.crystal.util.Vector import Vector
from orangecontrib.crystal.util.Photon import Photon
from orangecontrib.crystal.util.DiffractionResult import DiffractionResult
from orangecontrib.crystal.util.PerfectCrystalDiffraction import PerfectCrystalDiffraction


class Diffraction():
    
    def __init__(self):
        """
        Constructor.
        """
        # Initialize events to being unhandled.
        self.setOnCalculationStart(None)
        self.setOnProgress(None)
        self.setOnCalculationEnd(None)

    def _calculatePsiFromStructureFactor(self, unitcell_volume, photon_in, structure_factor):
        """
        Calculates the Psi as defined in Zachariasen [3-95].
        :param unitcell_volume: Volume of the unitcell.
        :param photon_in: Incoming photon.
        :param structure_factor: Structure factor.
        :return: Psi as defined in Zachariasen [3-95].
        """
        codata   = scipy.constants.codata.physical_constants
        classical_electron_radius = codata["classical electron radius"][0]

        psi = (-classical_electron_radius * photon_in.wavelength() ** 2 / (pi * unitcell_volume)) * structure_factor

        return psi

    def _calculateBraggNormal(self, d_spacing):
        """
        Calculates the normal on the reflection lattice plane B_H.
        :param d_spacing: Distance between parallel planes.
        :return: Bragg normal B_H.
        """
        normal_bragg = Vector(0, 0, 1).scalarMultiplication(2.0 * pi / d_spacing)

        return normal_bragg

    def _calculateSurfaceNormal(self, asymmetry_angle):
        """
        Calculates surface normal n.
        :param asymmetry_angle: Asymmetry angle of the surface cut.
        :return: Surface normal n.
        """
        normal_surface = Vector(sin(asymmetry_angle / 180.0 * pi),
                                0,
                                cos(asymmetry_angle / 180.0 * pi))

        return normal_surface

    def _calculateIncomingPhotonDirection(self, angle_bragg, deviation):
        """
        Calculates the direction of the incoming photon. Parallel to k_0.
        :param angle_bragg: Bragg angle.
        :param deviation: Deviation from the Bragg angle.
        :return: Direction of the incoming photon.
        """
        angle = pi / 2.0 - (angle_bragg + deviation)

        photon_direction = Vector(-sin(angle),
                                  0,
                                  -cos(angle))

        return photon_direction

    def log(self, str):
        """
        Logging function.
        :param str: Message to log.
        """
        print(str)

    def logStructureFactors(self, F_0,F_H,F_H_bar):
        """
        Logs the structure factors.
        :param F_0: Structure factor F_0.
        :param F_H: Structure factor F_H.
        :param F_H_bar: Structure factor F_H_bar.
        """
        self.log( "f0: (%f , %f)" % (F_0.real, F_0.imag))
        self.log( "fH: (%f , %f)" % (F_H.real, F_H.imag))
        self.log( "fHbar: (%f , %f)" % (F_H_bar.real, F_H_bar.imag))

    def setOnCalculationStart(self, on_calculation_start):
        """
        Sets handler for calculation start. The handler is called when the calculation starts.
        :param on_calculation_start: Delegate of calculation start event handler.
        """
        self._on_calculation_start = on_calculation_start

    def _onCalculationStart(self):
        """
        Invokes the calculation start event handler if any is registered.
        """
        if self._on_calculation_start is not None:
            self._on_calculation_start()

    def setOnProgress(self, on_progress):
        """
        Sets handler for calculation progression. The handler is called when the calculation progresses.
        :param on_progress: Delegate of calculation progress event handler.
        """
        self._on_progress = on_progress
        
    def _onProgress(self, index, angle_deviation_points):
        """
        Invokes the calculation progress event handler if any is registered.
        """
        if self._on_progress is not None:
            self._on_progress(index, angle_deviation_points)

    def _onProgressEveryTenPercent(self, index, angle_deviation_points):
        """
        Raises on progress event every ten percent of progression.
        :param index: Index of current point.
        :param angle_deviation_points: Number of total points to calculate.
        """
        ten_percent = angle_deviation_points / 10
        if((index + 1) % ten_percent) == 0 \
           or \
           index == angle_deviation_points:
            self._onProgress(index+1, angle_deviation_points)

    def setOnCalculationEnd(self, on_calculation_end):
        """
        Sets handler for calculation end. The handler is called when the calculation ends.
        :param on_calculation_end: Delegate of calculation end event handler.
        """
        self._on_calculation_end = on_calculation_end

    def _onCalculationEnd(self):
        """
        Invokes the calculation end event handler if any is registered.
        """
        if self._on_calculation_end is not None:
            self._on_calculation_end()

    def _checkSetup(self, diffraction_setup, bragg_angle, F_0, F_H, F_H_bar):
        """
        Checks if a given diffraction setup is possible, i.e. if a given Diffraction/Transmission for the given asymmetry
        and Miller indices is possible. Raises an exception if impossible.
        :param diffraction_setup: Diffraction setup.
        :param bragg_angle: Bragg angle.
        :param F_0: Structure factor F_0.
        :param F_H: Structure factor F_H.
        :param F_H_bar: Structure factor F_H_bar.
        """
        # Calculate bragg angle in degree.
        bragg_angle_in_degree = bragg_angle * 180 / pi

        # Check if the given geometry is a valid Bragg/Laue geometry.
        if diffraction_setup.geometryType() == BraggDiffraction() or diffraction_setup.geometryType() == BraggTransmission():
            if diffraction_setup.asymmetryAngle() >= bragg_angle_in_degree:
                raise Exception("Impossible geometry. Asymmetry angle larger than Bragg angle in Bragg geometry. No reflection possible.")
        elif diffraction_setup.geometryType() == LaueDiffraction() or diffraction_setup.geometryType() == LaueTransmission():
            if diffraction_setup.asymmetryAngle() <= bragg_angle_in_degree:
                raise Exception("Impossible geometry. Asymmetry angle smaller than Bragg angle in Laue geometry. No transmission possible.")

        # Check structure factor F_0.
        if abs(F_0.real) < 1e-7 or isnan(F_0.real):
            raise Exception("Structure factor for F_0 is zero.")

        # Check structure factor F_H.
        if abs(F_H.real) < 1e-7 or isnan(F_H.real) or abs(F_H.imag) < 1e-7 or isnan(F_H.imag):
            raise Exception("Structure factor for H=(hkl) is zero. Forbidden reflection for given Miller indices?")

        # Check structure factor F_H_bar.
        if abs(F_H_bar.real) < 1e-7 or isnan(F_H_bar.real) or abs(F_H_bar.imag) < 1e-7 or isnan(F_H_bar.imag):
            raise Exception("Structure factor for H_bar=(-h,-k,-l) is zero. Forbidden reflection for given Miller indices?")

    def calculateDiffraction(self, diffraction_setup):
        """
        Calculates the diffraction/transmission given by the setup.
        :param diffraction_setup: The diffraction setup.
        :return: DiffractionResult representing this setup.
        """
        # Calculate energy in keV.
        energy = diffraction_setup.energy()
        energy_in_kev = energy / 1000.0

        # Retrieve Miller indices from setup(for readability) .
        miller_h = diffraction_setup.millerH()
        miller_k = diffraction_setup.millerK()
        miller_l = diffraction_setup.millerL()

        # Load crystal from xraylib.
        crystal = xraylib.Crystal_GetCrystal(diffraction_setup.crystalName())

        # Retrieve bragg angle from xraylib.
        angle_bragg = xraylib.Bragg_angle(crystal,
                                          energy_in_kev,
                                          miller_h,
                                          miller_k,
                                          miller_l)

        # Get structure factors for all relevant lattice vectors 0,H,H_bar.
        debyeWaller = 1.0
        F_0 = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  energy_in_kev,
                                                  0, 0, 0,
                                                  debyeWaller, 1.0)

        F_H = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                  energy_in_kev,
                                                  miller_h, miller_k, miller_l,
                                                  debyeWaller, 1.0)

        F_H_bar = xraylib.Crystal_F_H_StructureFactor(crystal,
                                                      energy_in_kev,
                                                      - miller_h, -miller_k, -miller_l,
                                                      debyeWaller, 1.0)

        # Check if given Bragg/Laue geometry and given miller indices are possible.
        self._checkSetup(diffraction_setup, angle_bragg, F_0, F_H, F_H_bar)

        # Log the structure factors.
        self.logStructureFactors(F_0,F_H,F_H_bar)

        # Retrieve lattice spacing d from xraylib.
        d_spacing = xraylib.Crystal_dSpacing(crystal,
                                             miller_h,
                                             miller_k,
                                             miller_l) * 1e-10

        # Calculate the Bragg normal B_H.
        normal_bragg = self._calculateBraggNormal(d_spacing)

        # Calculate the surface normal n.
        normal_surface = self._calculateSurfaceNormal(diffraction_setup.asymmetryAngle())

        # Calculate the incoming photon direction (parallel to k_0).
        photon_direction = self._calculateIncomingPhotonDirection(angle_bragg,0.0)
        # Create photon k_0.
        photon_in = Photon(energy, photon_direction)

        # Retrieve unitcell volume from xraylib.
        unitcell_volume = crystal['volume'] * 10 ** -30

        # Calculate psis as defined in Zachariasen [3-95]
        psi_0     = self._calculatePsiFromStructureFactor(unitcell_volume, photon_in, F_0)
        psi_H     = self._calculatePsiFromStructureFactor(unitcell_volume, photon_in, F_H)
        psi_H_bar = self._calculatePsiFromStructureFactor(unitcell_volume, photon_in, F_H_bar)

        # Create PerfectCrystalDiffraction instance.
        perfect_crystal = PerfectCrystalDiffraction(diffraction_setup.geometryType(),
                                                    normal_bragg,
                                                    normal_surface,
                                                    angle_bragg,
                                                    psi_0,
                                                    psi_H,
                                                    psi_H_bar,
                                                    diffraction_setup.thickness(),
                                                    d_spacing)

        # Create DiffractionResult instance.
        result = DiffractionResult(diffraction_setup, angle_bragg)

        # Raise calculation start.
        self._onCalculationStart()

        # For every deviation from Bragg angle ...
        for index, deviation in enumerate(diffraction_setup.angleDeviationGrid()):
            # Raise OnProgress event if progressed by 10 percent.
            self._onProgressEveryTenPercent(index, diffraction_setup.angleDeviationPoints())

            # Calculate deviated incoming photon.
            photon_direction = self._calculateIncomingPhotonDirection(angle_bragg,
                                                                      deviation)
            photon_in = Photon(energy, photon_direction)

            # Calculate diffraction for current incoming photon.
            result_deviation = perfect_crystal.calculateDiffraction(photon_in)

            # Calculate polarization difference between sigma and pi polarization.
            polarization_difference = result_deviation["S"] / result_deviation["P"]

            # Add result of current deviation.
            result.add(deviation,
                       result_deviation["S"],
                       result_deviation["P"],
                       polarization_difference)

        # Raise calculation end.
        self._onCalculationEnd()

        # Return diffraction results.
        return result