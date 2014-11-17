
import xraylib
from numpy import pi, cos, sqrt, arcsin, real
import mpmath
from mpmath import mpc

from orangecontrib.crystal.util.Vector import Vector
from orangecontrib.crystal.util.Photon import Photon
from orangecontrib.crystal.util.ReflectivityAndPhase import ReflectivityAndPhase
from orangecontrib.crystal.util.GeometryType import BraggDiffraction, LaueDiffraction, BraggTransmission, LaueTransmission

class PerfectCrystalDiffraction():
    isDebug = False

    def __init__(self, geometry_type, normal_bragg, normal_surface, angle_bragg, psi_0, psi_H, psi_H_bar, thickness, d_spacing):
        self._geometryType = geometry_type
        self._normal_bragg = normal_bragg
        self._normal_surface = normal_surface
        self._angle_bragg = angle_bragg
        self._psi_0 = psi_0
        self._psi_H = psi_H
        self._psi_H_bar = psi_H_bar
        self._thickness = thickness
        self._d_spacing = d_spacing

    def normalBragg(self):
        return self._normal_bragg

    def normalSurface(self):
        return self._normal_surface

    def angleBragg(self):
        return self._angle_bragg

    def Psi0(self):
        return self._psi_0

    def PsiH(self):
        return self._psi_H

    def PsiHBar(self):
        return self._psi_H_bar

    def thickness(self):
        return self._thickness

    def dSpacing(self):
        return self._d_spacing

    def geometryType(self):
        return self._geometryType

    def tompc(self, var_c):
        mpc = mpmath.mpc(complex(var_c.real) + 1j * complex(var_c.imag))
        #print "tompc", var_c,mpc
        return mpc

    def log(self, str):
        print(str)

    def calculateGamma(self, photon):
        gamma = photon.unitDirectionVector().scalarProduct(self.normalSurface().getNormalizedVector())
        # Our crystal normal is pointing outside me medium. Zachariasen normal is
        # pointing into the crystal medium (pag 112). Therefore, we must change the
        # sign.
        gamma = -gamma
        return gamma

    def calculatePhotonOut(self, photon_in):
        k_in = photon_in.wavevector()#.scalarMultiplication(-1.0)
        k_in_parallel_surface = k_in.parallelTo(self.normalSurface())
        k_in_perpendicular_surface = k_in.perpendicularTo(self.normalSurface())
        normal_bragg_parallel_surface = self.normalBragg().parallelTo(self.normalSurface())
        normal_bragg_perpendicular_surface = self.normalBragg().perpendicularTo(self.normalSurface())

        k_out_parallel_surface = k_in_parallel_surface.addVector(normal_bragg_parallel_surface)
        norm_k_out_perpendicular = (photon_in.wavenumber() ** 2 - k_out_parallel_surface.norm() ** 2) ** 0.5
#        k_out_perpendicular_surface = k_in_perpendicular_surface.addVector(normal_bragg_perpendicular_surface)
        k_out_perpendicular_surface = k_in_perpendicular_surface.getNormalizedVector().scalarMultiplication(norm_k_out_perpendicular)

        v_out_1 = (k_out_parallel_surface.addVector(k_out_perpendicular_surface)).getNormalizedVector()
        v_out_2 = (k_out_parallel_surface.subtractVector(k_out_perpendicular_surface)).getNormalizedVector()

        v_out_Ewald = self.normalBragg().addVector(photon_in.wavevector())

        tmp1 = 1.0 - abs(v_out_Ewald.scalarProduct(v_out_1))
        tmp2 = 1.0 - abs(v_out_Ewald.scalarProduct(v_out_2))

        #if (self.isDebug):
        #    self.log( "<DEBUG>: tmp1, tmp2", tmp1, tmp2

        if tmp1 <= tmp2:
            v_photon_out = v_out_1
        else:
            v_photon_out = v_out_2

        v_photon_out = v_out_Ewald
        photon_out = Photon(photon_in.energy(), v_photon_out)

        return photon_out
        if(self.isDebug):
            self.log( "<DEBUG>: surface normal", self.normalSurface().components())
            self.log( "<DEBUG>: v_out_1 direction", v_out_1.components())
            self.log( "<DEBUG>: v_out_2 direction", v_out_2.components())
            self.log( "<DEBUG>: Angle bragg normal photon_in", photon_in.unitDirectionVector().angle(self.normalBragg()), pi * 0.5 - photon_in.unitDirectionVector().angle(self.normalBragg()))
            self.log( "<DEBUG>: Angle bragg normal photon_out", photon_out.unitDirectionVector().angle(self.normalBragg()), pi * 0.5 - photon_out.unitDirectionVector().angle(self.normalBragg()))
            self.log( "<DEBUG>: photon_in direction", photon_in.unitDirectionVector().components())
            self.log( "<DEBUG>: photon_out direction", photon_out.unitDirectionVector().components())


    def calculateZacAlpha(self, photon_in):
        k_in_parallel = photon_in.wavevector() #.parallelTo(self.normalBragg())

        tmp = k_in_parallel.scalarProduct(self.normalBragg())
        wavenumber = photon_in.wavenumber()

        #if(self.isDebug):
        #    self.log( "<DEBUG>: zac_alpha tmp", tmp
        #    self.log( "<DEBUG>: zac_alpha norm", self.normalBragg().norm() ** 2
        #    self.log( "<DEBUG>: zac_alpha wavenumber", wavenumber ** -2
        #!!!!!!
        zac_alpha = (wavenumber ** -2) * (self.normalBragg().norm() ** 2
                                          +
                                          2 * tmp)

        return zac_alpha


    def calculateZacB(self, photon_in, photon_out):
        #C numerator
        numerator = self.normalSurface().scalarProduct(photon_in.wavevector())
        #C denominator
        denominator = self.normalSurface().scalarProduct(photon_out.wavevector())
        #C ratio
        zac_b = numerator / denominator

        return zac_b


    def calculateZacQ(self, zac_b, effective_psi_h, effective_psi_h_bar):
        return zac_b * effective_psi_h * effective_psi_h_bar


    def calculateZacZ(self, zac_b, zac_alpha):
        return (1.0e0 - zac_b) * 0.5e0 * self.Psi0() + zac_b * 0.5e0 * zac_alpha

    def _calculateReflectivity(self, photon_in, zac_q, zac_z, gamma_0, effective_psi_h_bar):
        #C
        #C s-polarization. Zachariasen Eqs 3.122, 3.121, 3.126 and 3.132
        #C
        mpmath.dps = 32
        ctemp = (zac_q + zac_z * zac_z) ** 0.5

        zac_x1 = (-1.0 * zac_z + ctemp) / effective_psi_h_bar
        zac_x2 = (-1.0 * zac_z - ctemp) / effective_psi_h_bar
        zac_delta1 = 0.5 * (self.Psi0() - zac_z + ctemp)
        zac_delta2 = 0.5 * (self.Psi0() - zac_z - ctemp)
        zac_phi1 = 2 * pi / gamma_0 / photon_in.wavelength() * zac_delta1
        zac_phi2 = 2 * pi / gamma_0 / photon_in.wavelength() * zac_delta2
       
        zac_c1 = -1j * self.thickness() * zac_phi1
        zac_c2 = -1j * self.thickness() * zac_phi2

        #C
        if (self.isDebug):
            self.log( "<DEBUG>: __zac_c1"+str( zac_c1))
            self.log( "<DEBUG>: __zac_c2"+str( zac_c2))
        mp_zac_c1 = mpmath.exp(self.tompc(zac_c1))
        mp_zac_c2 = mpmath.exp(self.tompc(zac_c2))

        mp_zac_x1 = self.tompc(zac_x1)
        mp_zac_x2 = self.tompc(zac_x2)

        #C
        if (self.geometryType() is BraggDiffraction):
            reflectivity = mp_zac_x1 * mp_zac_x2 * (mp_zac_c1 - mp_zac_c2) / (mp_zac_c2 * mp_zac_x2 - mp_zac_c1 * mp_zac_x1)
        elif (self.geometryType() is LaueDiffraction):
            reflectivity = mp_zac_x1 * mp_zac_x2 * (mp_zac_c1 - mp_zac_c2) / (mp_zac_x2 - mp_zac_x1)
        elif (self.geometryType() is BraggTransmission):
            reflectivity = mp_zac_c1 * mp_zac_c2 * (mp_zac_x2 - mp_zac_x1) / (mp_zac_c2 * mp_zac_x2 - mp_zac_c1 * mp_zac_x1)
        elif (self.geometryType() is LaueTransmission):
            reflectivity = (mp_zac_x2 * mp_zac_c1 - mp_zac_x1 * mp_zac_c2) / (mp_zac_x2 - mp_zac_x1)

        if (self.isDebug):
            self.log( "<DEBUG>: ctemp: "+str(ctemp))
            self.log( "<DEBUG>: zac_z"+str( zac_z))
            self.log( "<DEBUG>: zac_q"+str( zac_q))
            self.log( "<DEBUG>: zac delta 1"+str( zac_delta1))
            self.log( "<DEBUG>: zac delta 2"+str( zac_delta2))
            self.log( "<DEBUG>: gamma_0"+str( gamma_0))
            self.log( "<DEBUG>: wavelength"+str( photon_in.wavelength()))
            self.log( "<DEBUG>: zac phi 1"+str( zac_phi1))
            self.log( "<DEBUG>: zac phi 2"+str(zac_phi2))

            self.log( "<DEBUG>: zac_c1: "+str( mp_zac_c1))
            self.log( "<DEBUG>: zac_c2: "+str( mp_zac_c2))
            self.log( "<DEBUG>: zac_x1: "+str( mp_zac_x1))
            self.log( "<DEBUG>: zac_x2: "+str( mp_zac_x2))

        return ReflectivityAndPhase(complex(reflectivity))

    def calculatePolarizationS(self, photon_in, zac_b, zac_z, gamma_0):
        #C
        #C s-polarization. Zachariasen Eqs 3.122, 3.121, 3.126 and 3.132
        #C

        zac_q = self.calculateZacQ(zac_b,
                                   self.PsiH(), self.PsiHBar())

        return self._calculateReflectivity(photon_in, zac_q, zac_z, gamma_0,
                                           self.PsiHBar())

    def calculatePolarizationP(self, photon_in, zac_b, zac_z, gamma_0):
        #C
        #C p-polarization
        #C


        effective_psi_h = self.PsiH() * cos(2 * self.angleBragg())
        effective_psi_h_bar = self.PsiHBar() * cos(2 * self.angleBragg())

        zac_q = self.calculateZacQ(zac_b, effective_psi_h, effective_psi_h_bar)

        return self._calculateReflectivity(photon_in, zac_q, zac_z, gamma_0,
                                           effective_psi_h_bar)

    def calculateDiffraction (self, photon_in):

        result = {"S": None,
                  "P": None}

        #if (self.isDebug):
        #    self.printDebugHeader()

        photon_out = self.calculatePhotonOut(photon_in)

        #photon_in.unitDirectionVector().printComponents()
        #photon_out.unitDirectionVector().printComponents()

        gamma_0 = self.calculateGamma(photon_in)
        gamma_h = self.calculateGamma(photon_out)

        #if (self.isDebug):
        #    self.printDebugPsis()
        #    self.printDebugSinBrg(photon_in)

        zac_alpha = self.calculateZacAlpha(photon_in)

        #if (self.isDebug):
        #    self.printDebugCrystalData(photon_in)
        #    self.printDebugCryBApproximation(gamma_0, gamma_h)

        zac_b = self.calculateZacB(photon_in, photon_out)

        #if (self.isDebug):
        #    self.printDebugCryB(zac_b, zac_alpha)

        zac_z = self.calculateZacZ(zac_b, zac_alpha)

        #if (self.isDebug):
        #    self.printDebugZacY(zac_b, zac_alpha)

        result["S"] = self.calculatePolarizationS(photon_in, zac_b, zac_z, gamma_0)
        result["P"] = self.calculatePolarizationP(photon_in, zac_b, zac_z, gamma_0)

        # note division by |b| in intensity (thus sqrt(|b|) in amplitude) 
        # for power balance (see Zachariasen pag. 122)
        #
        # this factor only applies to diffracted beam, not to transmitted beams
        # changed srio@esrf.eu 20130131, see private communication J. Sutter (DLS)
        if (self.geometryType() is BraggDiffraction \
            or \
            self.geometryType() is LaueDiffraction):
            result["S"].rescale(1.0 / sqrt(abs(zac_b)))
            result["P"].rescale(1.0 / sqrt(abs(zac_b)))

        if (self.isDebug):
            self.log( '<DEBUG>: rcs: '+str( result["S"].reflectivity())+str(result["S"].phase()))
            self.log( '<DEBUG>: rcp: '+str( result["P"].reflectivity())+str(result["P"].phase()))

        return result

    def _printMembers(self):
        self.log("Bragg angle: %f degrees \n" % (self.angleBragg() * 180 / pi))
        self.log( "psi0: (%.14f , %.14f)" % (self.Psi0().real, self.Psi0().imag))
        self.log( "psiH: (%.14f , %.14f)" % (self.PsiH().real, self.PsiH().imag))
        self.log( "psiHbar: (%.14f , %.14f)" % (self.PsiHBar().real, self.PsiHBar().imag))
        self.log( "d_spacing: %f " % self.dSpacing())


    def printDebugHeader(self):
        self.log( '<><>')
        self.log( '<DEBUG>: ******** crystal_perfect called ********')


    def printDebugSinBrg(self, photon_in):
        sin_brg = photon_in.unitDirectionVector().angle(self.normalBragg()) # angle vin with BH 

        #zac_alpha =-((R_LAM0/oe1%crystalData%D_SPACING)**2+ &
        #        2*R_LAM0* sin_brg/oe1%crystalData%D_SPACING)
        #write (i_debug,*) '<DEBUG>: !!!!! zac_alpha_old: ',zac_alpha
        self.log( '<DEBUG>: ')
        self.log( '<DEBUG>: theta:  ', arcsin(sin_brg) / pi * 180)
        self.log( '<DEBUG>: bh: ', self.normalBragg().components()[-1])


    def printDebugPsis(self):
        self.log( '<DEBUG>: PSI_H = ', self.PsiH())
        self.log( '<DEBUG>: PSI_HBAR = ', self.PsiHBar())
        self.log( '<DEBUG>: PSI_0 = ', self.Psi0())


    def printDebugCrystalData(self, photon_in):
        self.log( '<DEBUG>: !!!!! R_LAM0: ', photon_in.wavelength())
        self.log( '<DEBUG>: !!!!! D_SPACING: ', self.dSpacing())


    def printDebugCryBApproximation(self, gamma_0, gamma_h):
        cry_b = gamma_0 / gamma_h
        self.log( 'CRYSTAL_PERFECT: b(approx)= ', cry_b)


    def printDebugCryB(self, cry_b, zac_alpha):
        self.log( 'CRYSTAL_PERFECT: b(exact)= ', cry_b)
        self.log( '<DEBUG>: zac_alpha: ', zac_alpha)
        # this is the approximated alpha, eq. 3.116, with signs!!
#            tmp = 2 * (asin(sin_brg0) - asin(sin_brg)) * sin(2 * asin(sin_brg0))
#            self.log( '<DEBUG>: zac_alpha approx: ', tmp
#            self.log( '<DEBUG>: thetaB-theta=', asin(sin_brg0) - asin(sin_brg)
        #tmp = photon_in.unitDirectionVector().scalarProduct(self.normalBragg())
        #print '<DEBUG>: Vin.BH=', tmp


    def printDebugZacY(self, cry_b, zac_alpha):
        # y of Zachariasen (not needed)
        # this is y of Zachariasen, eq. 3.141
        #TODO: check the formula, replace  sqrt(psi_h*psi_hbar) by cdabs(psi_h) ??
        tmp = real((1.0e0 - cry_b) * self.Psi0() + cry_b * zac_alpha) / (2.0e0 * sqrt(abs(cry_b)) \
                                                                      *  1.0e0 * sqrt(self.PsiH() * self.PsiHBar()))
        self.log( '<DEBUG>: y of Zachariasen: ', tmp)
