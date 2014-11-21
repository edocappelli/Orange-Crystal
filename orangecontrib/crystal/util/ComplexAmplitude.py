"""
Represents a complex amplitude of a diffracted or transmissioned wave.
"""
import math


class ComplexAmplitude(object):

    def __init__(self, complex_amplitude):
        """
        Constructor.
        :param complex_amplitude: Complex amplitude of the wave.
        """
        self.setComplexAmplitude(complex_amplitude)

    def setComplexAmplitude(self, complex_amplitude):
        """
        Sets the complex amplitude.
        :param complex_amplitude: Complex amplitude of the wave.
        """
        self.__complex_amplitude = complex_amplitude

    def rescale(self, scalar):
        """
        Rescales the complex amplitude.
        :param scalar: Scalar to rescale the complex amplitude with.
        """
        self.__complex_amplitude = self.__complex_amplitude * scalar

    def complexAmplitude(self):
        """
        Returns the complex amplitude.
        :return: Complex amplitude.
        """
        return self.__complex_amplitude

    def intensity(self):
        """
        Return the intensity corresponding to the complex amplitude.
        :return: Intensity corresponding to the complex amplitude.
        """
        return abs(self.__complex_amplitude) ** 2

    def phase(self):
        """
        Returns the phase of the complex amplitude.
        :return: Phase of the complex amplitude.
        """
        PP = self.__complex_amplitude.real
        QQ = self.__complex_amplitude.imag
        return math.atan2(QQ,PP)

    def __truediv__(self, divisor):
        """
        Defines complex amplitude division.
        :param divisor: ComplexAmplitude dividing this instance.
        :return: Result of the division.
        """
        division = ComplexAmplitude(self.complexAmplitude()
                                        /
                                        divisor.complexAmplitude())
        return division
