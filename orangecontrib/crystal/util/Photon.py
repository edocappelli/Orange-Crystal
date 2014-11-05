import numpy as np
from quantities import *
import scipy.constants.codata

class Photon():

    def __init__(self, energy, direction_vector):
        self._energy = energy
        self._unit_direction_vector = direction_vector.getNormalizedVector()

    def energy(self):
        return self._energy

    def wavelength(self):
        codata = scipy.constants.codata.physical_constants
        codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
        codata_h, tmp1, tmp2 = codata["Planck constant"]
        E_in_Joule = float(self.energy().rescale(J).magnitude)

        wavelength = (codata_c * codata_h / E_in_Joule) * meter

        return wavelength

    def wavenumber(self):
        return (2.0 * np.pi) / self.wavelength()

    def wavevector(self):
        return self.unitDirectionVector().scalarMultiplication(self.wavenumber())

    def unitDirectionVector(self):
        return self._unit_direction_vector

    def __eq__(self, candidate):
        return self.wavenumber() == candidate.wavenumber() and self.unitDirectionVector() == candidate.unitDirectionVector()

    def __ne__(self, candidate):
        return not (self==candidate)
