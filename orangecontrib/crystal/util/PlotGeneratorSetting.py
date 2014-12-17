"""
Represents a plot generator setting. (e.g. EnergySweep, AngleSweep, PolarizationS,...)
"""
import copy

class PlotGeneratorSetting(object):
    def __init__(self, name, description, setting_type, default_value):
        self.__name = name
        self.__description = description
        self.__type = setting_type
        self.__default_value = default_value

        self.setValue(self.defaultValue())

    def name(self):
        return self.__name

    def isNamed(self, name):
        return self.name()==name

    def description(self):
        return self.__description

    def type(self):
        return self.__type

    def defaultValue(self):
        return self.__default_value

    def setValue(self, value):
        self.__value = value

    def value(self):
        return self.__value

    def clone(self):
        return copy.deepcopy(self)