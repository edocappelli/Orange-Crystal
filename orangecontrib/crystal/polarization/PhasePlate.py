import numpy as np
from orangecontrib.crystal.polarization.MuellerMatrix import MuellerMatrix

class PhasePlate(MuellerMatrix):
    def __init__(self, reflectivity_sigma, phase_sigma, reflectivity_pi, phase_pi, inclination_angle=0):
        self._reflectivity_sigma = reflectivity_sigma
        self._phase_sigma = phase_sigma
        self._reflectivity_pi = reflectivity_pi
        self._phase_pi = phase_pi

        self._inclination_angle = inclination_angle


        element_array = self._createMatrixElements()
        MuellerMatrix.__init__(element_array)

    def _createMatrixElements(self):
        element_array = np.zeros((4,4))

        element_array[0,0] = 0.5 * (self._reflectivity_pi**2 + self._reflectivity_sigma**2)
        element_array[0,1] = 0.5 * (self._reflectivity_pi**2 - self._reflectivity_sigma**2)
        element_array[1,0] = element_array[0,1]
        element_array[1,1] = element_array[0,0]

        scalar = 0.5 * self._reflectivity_sigma * self._reflectivity_pi
        delta_phase = self._phase_sigma - self._phase_pi
        element_array[2,2] = scalar * np.cos(delta_phase)
        element_array[2,3] = scalar * np.sin(delta_phase)
        element_array[3,2] = -1.0 * element_array[2,3]
        element_array[3,3] = element_array[2,2]

        return element_array