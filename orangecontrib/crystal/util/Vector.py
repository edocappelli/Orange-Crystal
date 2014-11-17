import numpy as np


class Vector():
    def __init__(self, x, y, z):
        self.setComponents(x, y, z)

    @staticmethod
    def fromComponents(components):
        return Vector(components[0],
                      components[1],
                      components[2])

    def setComponents(self, x, y, z):
        self._components = np.array([x, y, z])

    def components(self):
        return self._components

    def __eq__(self, candidate):
        return np.linalg.norm(self.components()
                              -
                              candidate.components()) < 1.e-7

    def __ne__(self, candidate):
        return not (self == candidate)

    def addVector(self, summand):
        components = self.components() + summand.components()
        return Vector.fromComponents(components)

    def scalarMultiplication(self, factor):
        components = self.components() * factor
        return Vector.fromComponents(components)

    def subtractVector(self, subtrahend):
        result = self.addVector(subtrahend.scalarMultiplication(-1.0))
        return result

    def scalarProduct(self, factor):
        scalar_product = np.dot(self.components(), factor.components())
        return scalar_product

    def crossProduct(self, factor):
        components = np.cross(self.components(), factor.components())
        return Vector.fromComponents(components)

    def norm(self):
        norm = self.scalarProduct(self) ** 0.5
        return norm

    def getNormalizedVector(self):
        return self.scalarMultiplication(self.norm() ** -1.0)

    def rotateAroundAxis(self, rotation_axis, angle):
        unit_rotation_axis = rotation_axis.getNormalizedVector()

        rotated_vector = self.scalarMultiplication(np.cos(angle))

        tmp_vector = unit_rotation_axis.crossProduct(self)
        tmp_vector = tmp_vector.scalarMultiplication(np.sin(angle))
        rotated_vector = rotated_vector.addVector(tmp_vector)

        scalar_factor = self.scalarProduct(unit_rotation_axis) * (1.0 - np.cos(angle))
        tmp_vector = unit_rotation_axis.scalarMultiplication(scalar_factor)
        rotated_vector = rotated_vector.addVector(tmp_vector)

        return rotated_vector

    def parallelTo(self, vector):
        unit_direction = vector.getNormalizedVector()
        projection_in_direction = self.scalarProduct(unit_direction)
        parallel_projection = unit_direction.scalarMultiplication(projection_in_direction)

        return parallel_projection

    def perpendicularTo(self, vector):
        perpendicular = self.subtractVector(self.parallelTo(vector))
        return perpendicular

    def getOnePerpendicularVector(self):
        vector_y = Vector(0, 1, 0)
        vector_z = Vector(0, 0, 1)

        if(self.getNormalizedVector() == vector_z):
            return vector_y

        vector_perpendicular = vector_z.perpendicularTo(self)
        vector_perpendicular = vector_perpendicular.getNormalizedVector()

        return vector_perpendicular

    def angle(self, factor):
        n1 = self.getNormalizedVector()
        n2 = factor.getNormalizedVector()

        cos_angle = n1.scalarProduct(n2)

        if hasattr(cos_angle, "magnitude"):
            cos_angle = cos_angle.magnitude

        angle = np.arccos(cos_angle)

        while angle > 2.0 * np.pi:
            angle = angle - 2.0 * np.pi

        if angle > np.pi:
            angle = 2.0 * np.pi - angle

        return angle

    def getVectorWithAngle(self, angle):
        vector_perpendicular = self.getOnePerpendicularVector()
        vector_with_angle = self.rotateAroundAxis(vector_perpendicular,
                                                  angle)

        return vector_with_angle

    def printComponents(self):
        print("x", self.components()[0])
        print("y", self.components()[1])
        print("z", self.components()[2])