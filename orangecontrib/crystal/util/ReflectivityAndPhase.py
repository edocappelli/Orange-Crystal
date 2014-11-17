import math

class ReflectivityAndPhase():

    def __init__(self, complex_reflexivity):
        self.setComplexReflectivity(complex_reflexivity)

    def setComplexReflectivity(self, complex_reflexivity):
        self.__complex_reflexivity = complex_reflexivity

    def reflectivity(self):
        return abs(self.__complex_reflexivity) ** 2

    def rescale(self, scalar):
        self.__complex_reflexivity = self.__complex_reflexivity * scalar

    def complexAmplitude(self):
        return self.__complex_reflexivity

    def phase(self):
        PP = self.__complex_reflexivity.real
        QQ = self.__complex_reflexivity.imag
        return math.atan2(QQ,PP)

    def __truediv__(self, divisor):
        division = ReflectivityAndPhase(self.complexAmplitude()
                                        /
                                        divisor.complexAmplitude())

        return division
