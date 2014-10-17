
class GeometryType(object):    pass
class LaueDiffraction(GeometryType):
    @staticmethod
    def description():
        return "Laue diffraction"

class BraggDiffraction(GeometryType):
    @staticmethod
    def description():
        return "Bragg diffraction"

class LaueTransmission(GeometryType):
    @staticmethod
    def description():
        return "Laue transmisson"

class BraggTransmission(GeometryType):
    @staticmethod
    def description():
        return "Bragg transmission"
    
def allGeometryTypes():
    return [BraggDiffraction,
            LaueDiffraction,
            BraggTransmission,
            LaueTransmission]

