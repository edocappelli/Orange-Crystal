"""
Represents a diffraction setup for a single photon.
Except for energy all units are in SI. Energy is in eV.
"""
from orangecontrib.crystal.diffraction.DiffractionSetup import DiffractionSetup


class DiffractionSetupSweepsPhoton(DiffractionSetup):

    def __init__(self, geometry_type, crystal_name, thickness,
                 miller_h, miller_k, miller_l,
                 asymmetry_angle,
                 photon_in):
        """
        Constructor.
        :param geometry_type: GeometryType (BraggDiffraction,...).
        :param crystal_name: The name of the crystal, e.g. Si.
        :param thickness: The crystal thickness.
        :param miller_h: Miller index H.
        :param miller_k: Miller index K.
        :param miller_l: Miller index L.
        :param asymmetry_angle: The asymmetry angle between surface normal and Bragg normal.
        :param photon_in: Incoming photon.
        """
        DiffractionSetup.__init__(self, geometry_type, crystal_name, thickness,
                                  miller_h, miller_k, miller_l,
                                  asymmetry_angle,
                                  incoming_photons=[photon_in])