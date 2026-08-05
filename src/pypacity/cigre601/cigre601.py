# -*- coding: utf-8 -*-
"""
Module: cigre601.py

Description
-----------
Steady-state and transient thermal rating solver for bare overhead conductors
following CIGRE Technical Brochure 601. Supports four analysis modes:
steady-state conductor temperature (NSELECT = 1), steady-state ampacity
(NSELECT = 2), transient conductor temperature (NSELECT = 3), and transient
thermal rating (NSELECT = 4). Inputs are provided through a
:class:`cable.Cable` object and a :class:`case.Case` object.

Copyright
---------
Copyright (c) 2026 Group of Advanced Electro-Technologies (GTEA). Universidad de Cantabria. All rights reserved.

License
-------
SPDX-License-Identifier: GPL-3.0-only

Notes
-----
This module is part of the PyPacity project.

References
----------
- CIGRE Technical Brochure 601, Guide for Thermal Rating Calculations of Overhead Lines, 2nd ed., 2014
"""


import numpy as np
import sys
from pypacity.cable import cable
from pypacity.case import case
from importlib import reload
#reload( cable)
#reload( case)

class CIGRE601():
    """Thermal rating solver implementing CIGRE Technical Brochure 601.

    Computes steady-state conductor temperature (NSELECT = 1), steady-state
    ampacity (NSELECT = 2), and transient conductor temperature (NSELECT = 3)
    for bare overhead conductors. Inputs are provided via :attr:`Cable1` and
    :attr:`Case1` before calling :meth:`cigre601`.

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Attributes</p>

    .. csv-table::
       :header: "Attribute", "Type", "Description"
       :widths: 20, 8, 72
       :align: center

       "``Cable1``", "Cable", "Conductor physical and thermal properties."
       "``Case1``", "Case", "Environmental and operational inputs."
       "``Debug``", "int", "Debug output level. ``0`` disables output; ``1`` prints intermediate values during computation. Defaults to ``0``."
       "``Debug_Dec``", "int", "Number of decimal places used in debug output. Defaults to ``3``."
       "``Tolerance``", "float", "Convergence tolerance for the conductor temperature iteration in amperes. Defaults to ``1``."
       "``MaxIterations``", "int", "Maximum number of iterations allowed in the conductor temperature solver. Defaults to ``400``."
       "``error``", "int", "Error code. ``0`` indicates no error; ``100`` indicates a thermal balance inconsistency. Defaults to ``0``."
    """

    def __init__(self):
        """Initialise the solver with default Cable, Case, and control parameters."""
        self.Cable1 = cable.Cable()
        self.Case1 = case.Case()
        self.Debug = 0 # 1 print intermediate values
        self.Debug_Dec = 3 # number of decimal value for printing debug info
        self.Tolerance = 1 # Tolerance for temperature estimation
        self.MaxIterations = 400 # Maximum number of iteration
        self.error = 0 # 0 no error


    def set_error(self, error):
        """Set the solver error code.

        :param error: Error code to assign. Use ``0`` to clear a previous error.
        :type error: int

        .. note::
            Sets :attr:`error` on this instance.
        """
        self.error = error
        return


    def get_error(self):
        """Return the current solver error code.

        :return: Error code. ``0`` indicates no error; ``100`` indicates a
            thermal balance inconsistency.
        :rtype: int
        """
        return(self.error)
    

    def set_cable(self, Cable):
        """Assign a conductor definition to this solver.

        :param Cable: Conductor physical and thermal properties.
        :type Cable: cable.Cable

        .. note::
            Sets :attr:`Cable1` on this instance.
        """
        self.Cable1 = Cable
        return


    def set_case(self, Case):
        """Assign an environmental and operational case to this solver.

        Initialises any unset attributes required by the solver
        (``CDR_LAT_DEG``, ``NDAY``, ``SUN_TIME``, ``A3``) to ``0`` if
        not already set.

        :param Case: Environmental and operational inputs.
        :type Case: case.Case

        .. note::
            Sets :attr:`Case1` on this instance.
        """
        self.Case1 = Case

        if self.Case1.CDR_LAT_DEG is None:
            self.Case1.CDR_LAT_DEG = 0

        if self.Case1.NDAY is None:
            self.Case1.NDAY = 0

        if self.Case1.SUN_TIME is None:
            self.Case1.SUN_TIME = 0

        if self.Case1.A3 is None:
            self.Case1.A3 = 0

        return

    def sind(self, angle):
        """Compute the sine of an angle given in degrees.

        :param angle: Angle in degrees.
        :type angle: float

        :return: Sine of the angle.
        :rtype: float
        """
        DEG_TO_RAD = np.pi/180
        return(np.sin(DEG_TO_RAD*angle))

    def cosd(self, angle):
        """Compute the cosine of an angle given in degrees.

        :param angle: Angle in degrees.
        :type angle: float

        :return: Cosine of the angle.
        :rtype: float
        """
        DEG_TO_RAD = np.pi/180
        return(np.cos(DEG_TO_RAD*angle))    
  
  
   ########################################################################
    def solar(self):
        """Compute the solar heat gain rate on the conductor using the IEEE 738 polynomial model.

        Computes the solar altitude from ``Case1.CDR_LAT_DEG``, ``Case1.NDAY``,
        and ``Case1.SUN_TIME``, then evaluates the solar irradiance at the Earth
        surface using the polynomial coefficients selected by ``Case1.A3``
        (``0`` for clear air, ``1`` for industrial atmosphere). When
        ``Case1.SUN_TIME >= 24``, ``Case1.SolarRadiation`` is used directly as
        the irradiance instead of computing it from solar position.

        :return: Solar heat gain rate QS in W/m.
        :rtype: float

        .. note::
            Sets ``Case1.QS`` to the computed value.
        """
        DEG_TO_RAD = np.pi/180
        RAD_TO_DEG = 180/np.pi
        #self.CDR_LAT_RAD = self.Case1.CDR_LAT_DEG*self.DEG_TO_RAD
        CDR_LAT_RAD = self.Case1.CDR_LAT_DEG*DEG_TO_RAD # Conductor latitude in radians
   
    
        #5060 REM * SOLAR DECLINATION
        #data['DECL_DEG'] = 23.4583*np.sin(((284 + data['NDAY'])/365)*2*np.pi)
        #data['DECL_RAD'] = data['DECL_DEG']*data['DEG_TO_RAD']
        DECL_DEG = 23.4583*np.sin(((284 + self.Case1.NDAY)/365)*2*np.pi)
        DECL_RAD = DECL_DEG*DEG_TO_RAD     
        
    
        #5090 REM * SOLAR ANGLE RELATIVE TO NOON
        #data['HOUR_ANG_DEG'] = (data['SUN_TIME']-12)*15
        #data['HOUR_ANG_RAD'] = data['HOUR_ANG_DEG']*data['DEG_TO_RAD']
        HOUR_ANG_DEG = (12 - self.Case1.SUN_TIME)*15
        HOUR_ANG_RAD = HOUR_ANG_DEG*DEG_TO_RAD
    
        #5120 REM * FIND SOLAR ALTITUDE - H3
        #data['H3ARG'] = (np.cos(data['CDR_LAT_RAD'])*np.cos(data['DECL_RAD'])*np.cos(data['HOUR_ANG_RAD'])
        #                +np.sin(data['CDR_LAT_RAD'])*np.sin(data['DECL_RAD']))
        #data['H3_RAD'] = np.arctan(data['H3ARG']/np.sqrt(1-data['H3ARG']**2))
        #data['H3_DEG'] = data['H3_RAD']/data['DEG_TO_RAD']
        H3ARG = (np.cos(CDR_LAT_RAD)*np.cos(DECL_RAD)*np.cos(HOUR_ANG_RAD) \
                     +np.sin(CDR_LAT_RAD)*np.sin(DECL_RAD))
        
        #H3_RAD = np.arctan(H3ARG/np.sqrt(1-(H3ARG)**2))
        H3_RAD = np.arcsin(H3ARG)
        H3_DEG = H3_RAD*RAD_TO_DEG
  
        if self.Case1.A3 == 1:
        #5260 REM *****************************************************************
        #5270 REM * SOLAR HEAT (Q3) AT EARTH SURFACE (W/M2) IN INDUSTRIAL AIR (P6)
        #5280 REM *****************************************************************
            Q3 = 53.1821 + 14.211*H3_DEG + 0.66138*(H3_DEG)**2 
            Q3 += -0.031658*(H3_DEG)**3 + 5.4654E-04*(H3_DEG)**4
            Q3 += -4.3446E-06*(H3_DEG)**5 + 1.3236E-08*(H3_DEG)**6
            self.Bstring = 'INDUSTRIAL'
        elif self.Case1.A3 == 0:
        #5180 REM ***************************************************************
        #5190 REM * SOLAR HEATING (Q3) AT EARTH SURFACE (W/M2) IN CLEAR AIR (P6)
        #5200 REM ***************************************************************
            Q3 = -42.2391 + 63.8044*H3_DEG - 1.922*(H3_DEG)**2
            Q3 += 0.034692*(H3_DEG)**3 - 3.6112E-04*(H3_DEG)**4
            Q3 += 1.9432E-06*(H3_DEG)**5 - 4.0761E-09*(H3_DEG)**6
            self.Bstring = 'CLEAR'
    
        #5330 REM * CALCULATE SOLAR AZIMUTH VARIABLE, CHI
        auxi1 = (np.sin(CDR_LAT_RAD)*np.cos(HOUR_ANG_RAD) \
              - np.cos(CDR_LAT_RAD)*np.tan(DECL_RAD))
        CHI = np.sin(HOUR_ANG_RAD)/auxi1
    
        #5360 REM * CALCULATE SOLAR AZIMUTH CONSTANT, CAZ
        if (HOUR_ANG_DEG < 0) and (CHI >= 0):
            CAZ = 0
        elif (HOUR_ANG_DEG >= 0) and (CHI < 0):
            CAZ = 360
        else:
            CAZ = 180
    
        #Set QS if solar measurement available
        if ( self.Case1.SUN_TIME >= 24) or (self.Case1.SUN_TIME == 99):
            Q3 = self.Case1.SolarRadiation
    
        #5400 REM * CALCULATE SOLAR AZIMUTH IN DEGREES, Z4.DEG
        Z4_DEG = CAZ + np.arctan(CHI)/DEG_TO_RAD
        Z4_RAD = Z4_DEG*DEG_TO_RAD
        Z1_RAD = self.Case1.Z1_DEG*DEG_TO_RAD
        E1 = np.cos(H3_RAD)*np.cos(Z4_RAD-Z1_RAD)
        E2_RAD = np.arctan(np.sqrt(1/(E1)**2 - 1))
        QS = (self.Cable1.ABSORP*Q3*np.sin(E2_RAD)*self.Cable1.D/1000*(1 \
            + 0.0001148*self.Case1.CDR_ELEV-1.108E-08*(self.Case1.CDR_ELEV)**2))
    
        if QS < 0:
            QS = 0.0
    
        self.Case1.QS = QS
        #print("Solar Radiation QS: ", self.Case1.QS, " W/m")
        return QS
   #End Function ieee_738_2013_solar  
  
  
  
    def solarx(self):
        """Compute the solar heat gain rate on the conductor per CIGRE TB 601 Section 3.3.

        Uses the CIGRE TB 601 solar model with clearness ratio ``Case1.Ns``
        and ground reflectance ``Case1.ALBEDO``. The solar source is selected
        by ``Case1.SOLAR``: ``0`` uses the measured ``Case1.SolarRadiation``
        directly; ``1`` computes the irradiance from date, time, and location.

        :return: Solar heat gain rate in W/m.
        :rtype: float
        """

        if self.Debug == 1:
            print("****************************************")
            print("Solar heating")
        
        DEG_TO_RAD = np.pi/180.0
        RAD_TO_DEG = 180.0/np.pi
             
        # 3.3 Pag. 18. Eq (8)
        if self.Case1.SolarRadiation != None:
            Psm = self.Cable1.ABSORP*self.Case1.SolarRadiation*self.Cable1.D/1000.0 
            if self.Debug == 1:
                print("Measured solar heating: " + self.str_round(Psm) + " W/m")
    
        # Z Hour angle of the Sun
        Z = 15*(12-self.Case1.SUN_TIME)
        if self.Debug == 1:
            print("Hour angle Z: " + self.str_round(Z) + " deg")
       
        # Declination
        deltas = 23.3*np.sin((2*np.pi*(284+self.Case1.NDAY))/365)
        if self.Debug == 1:
            print("Declination: " + self.str_round(deltas) + " deg")
       
        # Solar Altitude
        Hs = RAD_TO_DEG*np.arcsin( self.sind(self.Case1.CDR_LAT_DEG)*self.sind(deltas)+
                                  self.cosd(self.Case1.CDR_LAT_DEG)*self.cosd(deltas)*self.cosd(Z))
        if self.Debug == 1:
            print("Solar Altitude Hs: " + self.str_round(Hs) + " deg")
        
        # Azimuth of the Sun
        gammas = -RAD_TO_DEG*np.arcsin((self.cosd(deltas)*self.sind(Z))/(self.cosd(Hs)))
        if self.Debug == 1:
            print("gammas: " + self.str_round(gammas) + " deg")
            
        # Albedo
        if self.Debug == 1:
            print("Albedo F: " + self.str_round( self.Case1.ALBEDO))

        # IB(0) Pag. 19. Eq (10)
        IB0 = self.Case1.Ns*(1280*self.sind(Hs))/(self.sind(Hs)+0.314) 
        if self.Debug == 1:
            print("IB0: " + self.str_round(IB0) + " W/m^2")
        
        # IB(y) Pag. 19. Eq (11)
        IBy = IB0*(1 + 1.4e-4*self.Case1.CDR_ELEV*((1367/IB0)-1))
        if self.Debug == 1:
            print("CDR_ELEV: " + self.str_round(self.Case1.CDR_ELEV) + " m")
            print("IBy: " + self.str_round(IBy) + " W/m^2")
        
        # Id Difuse solar radiation Pag. 20. Eq (13)
        Id = (430.5 - 0.3288*IBy)*self.sind(Hs)
        if self.Debug == 1:
            print("Id: " + self.str_round(Id) + " W/m^2")
        
        # eta Pag. 20. Eq (14)
        eta = RAD_TO_DEG*np.arccos(self.cosd(Hs)*self.cosd(gammas - self.Case1.Z1_DEG))
        if self.Debug == 1:
            print("eta: " + self.str_round(eta) + " deg")
        
        # Computed solar heating. Pag. 18. Eq (9)
        # Global solar radiation
        IT = (IBy*(self.sind(eta) + (np.pi/2)*self.Case1.ALBEDO*self.sind(Hs)) + Id*(1+(np.pi/2*self.Case1.ALBEDO)))
        if self.Debug == 1:
            print("Global solar radiation IT: " + self.str_round(IT) + " W/m^2")
        Psc = self.Cable1.ABSORP*(self.Cable1.D/1000)*IT
        if self.Debug == 1:
            print("Computed solar heating: " + self.str_round(Psc) + " W/m")
           
        if self.Case1.SOLAR == 0:
            Ps = Psm
        else:
            Ps = Psc

        if self.Debug == 1:
            print("Ps: " + self.str_round(Ps) + " W/m")
        
        return Ps



    def radiation(self):
        """Compute the radiative heat loss rate of the conductor.

        Applies the Stefan-Boltzmann law using surface emissivity
        ``Cable1.EMISS`` and the conductor temperature ``Case1.TCDR``.

        :return: Radiative heat loss rate in W/m.
        :rtype: float
        """
        # Pr Pag. 30. Eq (27).
        # sigmaB. Stefan-Boltzmann constant        
        sigmaB = 5.6697e-8 # W.m^(-2).K^(-4)
        
        Pr = np.pi*(self.Cable1.D/1000.0)*sigmaB*self.Cable1.EMISS*(pow(self.Case1.TCDR + 273,4)-pow(self.Case1.TAMB + 273,4))
        if self.Debug == 1:
            print("****************************************")
            print("Radiative cooling: " + self.str_round(Pr) + " W/m")
            
        return Pr
        

    def joule(self):
        """Compute the Joule heating rate of the conductor.

        The current used depends on ``Case1.NSELECT``: ``Case1.XIPRELOAD``
        for NSELECT = 1, ``Case1.TR`` for NSELECT = 2, and ``Case1.XISTEP``
        for NSELECT = 3 and 4.

        :return: Joule heating rate in W/m.
        :rtype: float

        .. note::
            Sets ``Case1.QJ`` to the computed value.
        """
        Rac = self.Rac()
        
        if self.Case1.NSELECT == 1:
            I = self.Case1.XIPRELOAD
        elif self.Case1.NSELECT == 2:
            I = self.Case1.TR 
        elif self.Case1.NSELECT == 3:
            I = self.Case1.XISTEP
        elif self.Case1.NSELECT == 4:
            I = self.Case1.XISTEP 
        
        
        PJ =(Rac)*(I**2)
        self.Case1.QJ = PJ
        return PJ



    def convection(self):
        """Compute the convective heat loss rate of the conductor.

        Evaluates both natural and forced convection following CIGRE TB 601
        and returns the larger of the two. Natural convection coefficients are
        selected from the Grashof-Prandtl product. Forced convection
        coefficients depend on the Reynolds number and the conductor roughness
        ratio ``d / (2*(D - d))``.

        :return: Convective heat loss rate in W/m.
        :rtype: float

        .. note::
            Computes ``Case1.WINDANG_DEG`` from ``Case1.DWIND_DEG`` and
            ``Case1.Z1_DEG`` before evaluating forced convection.
        """
        if self.Debug == 1:
            print("****************************************")
            print('Natural convection')
        
        # Film temperature
        Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        if self.Debug == 1:
            print("Tfilm Tf: " + self.str_round(Tf) + " ºC")
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        cf = 1006 
        if self.Debug == 1:
            print("Specific air heat capacity cf: " + self.str_round(cf) + " J/kg.ºK")
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        if self.Debug == 1:
            print("Thermal conductivity of the air lambdaf: " + self.str_round(lambdaf) + " W/ºK.m")
        # Dynamic viscosity [kg/m.s]
        muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6
        if self.Debug == 1:
            print("Dynamic viscosity muf: %.4e kg/m.s" %(muf))
        # Prandtl number, Pr = cf . muf / lambdaf   W/m
        Pr = cf*muf/lambdaf        
        if self.Debug == 1:
            print('Prandtl: ' + self.str_round(Pr)) 
            

        # Air density
        gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        if self.Debug == 1:
            print("Air density gamma: " + self.str_round(gamma) + " kg/m^3")

        # Kinematic viscosity
        vf = muf / gamma 
        if self.Debug == 1:
            print("Kinematic viscosity vf: %.4e m^2/s" %(vf))
        # Grashof number
        Gr = ((self.Cable1.D/1000)**3)*(self.Case1.TCDR - self.Case1.TAMB)*9.81/((Tf+273)*vf**2)
        if self.Debug == 1:
            print('Grashof: ' + self.str_round(Gr))
        
        # Table 5. Pg. 28
        GrPr = Gr*Pr
        if  GrPr < 1e2:
            A = 1.02
            m = 0.148
        elif (GrPr >= 1e2) and (GrPr < 1e4):
            A = 0.85
            m = 0.188
        elif (GrPr >= 1e4) and (GrPr < 1e7):
            A = 0.48
            m = 0.25
        elif GrPr >=1e7:
            A = 0.125
            m = 0.333

        Nunat = A*(GrPr)**m 
        
        # NOTE: Nubeta is the beta-corrected (conductor inclination) natural-convection
        # Nusselt number, but it is never used below — Pcnat is computed from the
        # uncorrected Nunat instead. As written, Case1.beta has no effect on natural
        # convection. Left as-is pending a decision on whether Pcnat should use Nubeta.
       
        if self.Cable1.Stranded == 1: # stranted conductor
            Nubeta = Nunat*(1 - 1.76e-6*(self.Case1.beta**2.5))
        else: # smooth conductor
            Nubeta = Nunat*(1 - 1.58e-4*(self.Case1.beta**1.5))
        
        Pcnat = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nunat
        if self.Debug == 1:
            print('Pc,nat: ' + self.str_round(Pcnat) + ' W/m')
        
        
        if self.Debug == 1:
            print("****************************************")
            print('Forced convection')

        # Film temperature
        #Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        #cf = 1006 
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        #lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        # Dynamic viscosity [kg/m.s]
        #muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6        
        # Air density
        #gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        # Kinematic viscosity
        #vf = muf / gamma 
        
        # Reynolds number. Pag. 25
        Rey = self.Case1.VWIND*(self.Cable1.D/1000)/vf
        if self.Debug == 1:
            print("Reynolds number: " +self.str_round(Rey))
        
        # Roughness of the conductor        
        Rs = self.Cable1.d/(2*(self.Cable1.D - self.Cable1.d))
        if self.Debug == 1:
            print("Roughness of the conductor: " + self.str_round(Rs))
        
        if self.Cable1.Stranded == 1: # Stranded conductor
            if Rs <= 0.05:
                if Rey < 2650:
                    B = 0.641
                    n = 0.471
                else:
                    B = 0.178
                    n = 0.633
            else:
                if Rey < 2650:
                    B = 0.641
                    n = 0.471
                else:
                    B = 0.048
                    n = 0.8
        else: # Smooth conductor
            if Rey < 5000:
                B = 0.583
                n = 0.471
            elif (Rey >= 5000) and (Rey < 50000):
                B = 0.148
                n = 0.633
            else:
                B = 0.0208
                n = 0.814
        
        
        Nu90 = B*(Rey**n)
        if self.Debug == 1:
            print("Nu90: " + self.str_round(Nu90))
        
        
        alpha = abs( self.Case1.DWIND_DEG - self.Case1.Z1_DEG )
        if alpha < 180:
            self.Case1.WINDANG_DEG = min( alpha, 180 - alpha)
        else: # >= 180
            alphap = alpha - 180.0
            self.Case1.WINDANG_DEG = min( alphap, 180 - alphap)
        
        if self.Debug == 1:
            print("Wind angle delta WINDANG_DEG: " + self.str_round(self.Case1.WINDANG_DEG) + " deg")
        
        if self.Cable1.Stranded == 1:
            if self.Case1.WINDANG_DEG <= 24:
                Nudelta = Nu90*(0.42 + 0.68*( self.sind(self.Case1.WINDANG_DEG)**1.08)) 
            else:
                Nudelta = Nu90*(0.42 + 0.58*( self.sind(self.Case1.WINDANG_DEG)**0.90)) 
        else:
            Nudelta = Nu90*(self.sind(self.Case1.WINDANG_DEG)**2 + 0.0169*self.cosd(self.Case1.WINDANG_DEG)**2)**0.225

        if self.Debug == 1:
            print("Nudelta: " + self.str_round(Nudelta))

        Pcfor = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nudelta
        if self.Debug == 1:
            print("Pc forced: " + self.str_round(Pcfor) + " W/m")

        Pc = max( Pcnat, Pcfor)
        if self.Debug == 1:
            print("-----------------")
            print("Pconvective: " + self.str_round(Pc) + " W/m")
            
        return Pc


    def Rac(self):
        """Compute the AC resistance of the conductor at the operating temperature.

        Applies a linear interpolation between ``Cable1.RLO`` at ``Cable1.TLO``
        and ``Cable1.RHI`` at ``Cable1.THI``, evaluated at ``Case1.TCDR``.

        :return: AC resistance in ohm/m.
        :rtype: float
        """
        
        alpha = (self.Cable1.RHI - self.Cable1.RLO)/(self.Cable1.THI - self.Cable1.TLO)
        if self.Debug == 1:
            print("****************************************")
            print("Rac(Tamb)")
            print("Conductor resistance temperature coefficient: %.4e ohm/m.ºC" %(alpha))
        
        Rac = self.Cable1.RLO + (self.Case1.TCDR - self.Cable1.TLO)*alpha
        if self.Debug == 1:
            print("Rac(TCDR): %.4e ohm/m" %(Rac) )
            
        return Rac



    def cigre601(self):
        """Run the CIGRE TB 601 thermal rating analysis for the configured mode.

        Dispatches to the appropriate solver method based on ``Case1.NSELECT``:

        - ``1``: calls :meth:`conductor_temperature` — steady-state conductor
          temperature for a given current.
        - ``2``: calls :meth:`thermal_rating` — steady-state ampacity for a
          given conductor temperature.
        - ``3``: calls :meth:`TCDR_vs_time` — transient conductor temperature
          evolution.
        - ``4``: transient thermal rating (reserved for future implementation).
        """

        if self.Case1.NSELECT == 1:
            #print("NSELECT == 1")
            self.conductor_temperature() 
        elif self.Case1.NSELECT == 2:
            self.Case1.TCDR = self.Case1.TCDRPRELOAD
            self.thermal_rating()
        elif self.Case1.NSELECT == 3:
            self.TCDR_vs_time() 
        elif self.Case1.NSELECT == 4:
            pass

        return
    

    def conductor_temperature(self):
        """Compute the steady-state conductor temperature for a given current.

        Iterates :meth:`thermal_rating` while stepping the conductor
        temperature downward from ``Cable1.TCDRMAX + 100`` until the rated
        current equals ``Case1.XIPRELOAD``, then interpolates to find the
        exact equilibrium temperature.

        .. note::
            Sets ``Case1.TCDRPRELOAD`` to the computed conductor temperature.
        """
        
        TCDR = self.Cable1.TCDRMAX + 100
        Niterations = 0
        deltaI = 1
        
        
        # abs(balance) > self.Tolerance) 
        while (deltaI > 0) and (Niterations < self.MaxIterations):
            self.Case1.TCDRPRELOAD = TCDR 
            self.Case1.TCDR = self.Case1.TCDRPRELOAD         
            #TCDRold = TCDR 
            self.thermal_rating()
            #balance = self.Case1.QS + self.Case1.RAC*(self.Case1.XIPRELOAD**2) - self.Case1.QC - self.Case1.QR
            
            deltaI = self.Case1.TR - self.Case1.XIPRELOAD 

            if self.Debug == 1:
                print("Iteration: ", Niterations, "; DeltaI: ", deltaI, "; TCDR: ", TCDR, " ;Current: ", self.Case1.TR)

            if  deltaI > 0:
               TCDRold = TCDR
               TRold = self.Case1.TR
               TCDR -= 0.5
            else:
                TCDRx = TCDR + ((TCDRold - TCDR)/(TRold - self.Case1.TR))*(self.Case1.XIPRELOAD - self.Case1.TR)
                if self.Debug == 1:
                    print("Current: ", self.Case1.XIPRELOAD, " ; TCDR: ", TCDRx)
                 
            Niterations += 1
            
        
        self.Case1.TCDRPRELOAD = TCDRx   
            
    


    def TCDR_vs_time(self):
        """Compute the transient conductor temperature evolution over time.

        Integrates the heat balance equation step by step using
        ``Case1.DELTIME`` as the time step. The starting temperature is either
        computed from steady state (when ``Case1.TTfromST = 1``) or taken
        directly from ``Case1.TCDRinitial`` (when ``Case1.TTfromST = 0``).
        Total simulation time is ``Case1.TT`` seconds, or
        ``Case1.TT * 60`` seconds when ``Case1.SORM = 1``.

        .. note::
            Sets ``Case1.TIME`` and ``Case1.ATCDR`` with the time and
            temperature traces respectively.
        """        
        t = 0
        Tc = 0
        time = []
        temp = []
        
        if self.Case1.TTfromST == 0:
            Tc = self.Case1.TCDRinitial
        elif self.Case1.TTfromST == 1:
            self.conductor_temperature()
            Tc = self.Case1.TCDRPRELOAD
       
        if self.Debug == 1:
            print("Starting point")
            print("Initial current: ", self.Case1.XIPRELOAD, " ; Initial temperature: ", Tc)
            
        time.append(t)
        temp.append( Tc)
        
        
        # DeltaTime (update to use loaded values from IEEE case)
        # deltaTime = 60.0
        deltaTime = self.Case1.DELTIME

        if self.Case1.SORM == 1:
            tend = self.Case1.TT*60
        else:
            tend = self.Case1.TT
            
        steps = int(tend/self.Case1.DELTIME)
        if self.Debug == 1:
            print("steps: ", steps)
            
        for _ in range(steps):
            
            
            self.Case1.TCDR = Tc
            
            # Compute the heat balance power terms 
            Pj = self.joule() 
            Ps = self.solarx()
            Pr = self.radiation()
            Pc = self.convection()
            
            # Compute the equivalent thermal capacity of the aluminum-steel conductor
            maca = self.Cable1.mAlum*self.Cable1.CAlum20*(1+self.Cable1.BetaAlum20*(Tc - 20.0))
            mscs = self.Cable1.mSteel*self.Cable1.CSteel20*(1+self.Cable1.BetaSteel20*(Tc - 20.0))
            mc   = maca + mscs
            
            # Compute the temperature increment for the next time step
            deltaT = (Pj + Ps - Pr - Pc)*deltaTime/(mc)
            
            # Update time and conductor temperature for the transient step
            if self.Debug == 1:
                print(f"Tinitial: {Tc:6.3f}°C  dT:{deltaT:0.3f}") 


            t += deltaTime
            Tc += deltaT
            time.append( t)
            temp.append( Tc)
            
        self.Case1.TIME  = time
        self.Case1.ATCDR = temp              
        
   
    def thermal_rating(self):
        """Compute the steady-state ampacity for a given conductor temperature.

        Evaluates solar heat gain (:meth:`solarx`), radiative cooling
        (:meth:`radiation`), convective cooling (:meth:`convection`), and AC
        resistance (:meth:`Rac`) at ``Case1.TCDR``, then solves the heat
        balance for the current that produces thermal equilibrium.

        :return: Steady-state ampacity in amperes.
        :rtype: float

        .. note::
            Sets ``Case1.QS``, ``Case1.QR``, ``Case1.QC``, ``Case1.RAC``,
            ``Case1.TR``, and ``self.deltaTcTs_value``. Sets
            ``self.error = 100`` if no thermal balance is achievable.
        """

        # Solar heating
        Ps = self.solarx()  
        self.Case1.QS = Ps
       
        # Radiation cooling 
        Pr = self.radiation()
        self.Case1.QR = Pr
    
        # Convective cooling
        Pc = self.convection()
        self.Case1.QC = Pc
        
        # Rac
        Rac = self.Rac()
        self.Case1.RAC = Rac
        
        interm = Pr + Pc - Ps
        if interm < 0:
            self.error = 100 # no thermal balance
            interm *= (-1)
            print('CIGRE inconsistency -> Ps: %.2f; Pr:%.2f; Pc:%.2f' %(Ps, Pr, Pc))
            print('VWIND: %.2f; WINDANG_DEG: %.2f; SolarRadiation: %.2f' %(self.Case1.VWIND, self.Case1.WINDANG_DEG, self.Case1.SolarRadiation))
        I = np.sqrt((interm)/(Rac))
        self.Case1.TR = I

        # Radial temperature difference between conductor surface and core
        self.deltaTcTs_value = self.deltaTcTs()

        if self.Debug == 1:
            print("Dynamic Current Rating: " + self.str_round(I) + " A")
            print(f"Tc-Ts: {self.str_round(self.deltaTcTs_value)} ºC")

    
        return I       


    def str_round(self, valuex):
        """Return a rounded string representation of a numeric value.

        Rounds to the number of decimal places defined by :attr:`Debug_Dec`.

        :param valuex: Value to round and convert.
        :type valuex: float

        :return: Rounded value as a string.
        :rtype: str
        """
        return str( round( valuex, self.Debug_Dec))

    
    def output(self):
        """Print a formatted summary of the most recent analysis results.

        For NSELECT = 1 prints the input current and the resulting steady-state
        temperature. For NSELECT = 2 prints the input temperature and the
        resulting ampacity. Solar heat gain, radiative cooling, convective
        cooling, and the core-surface temperature difference are always printed.
        """
        print(" ")
        print(" ")
        print("*******************************************************************")
        print("*******************************************************************")
        print("CIGRE TB601 ")
        print("*******************************************************************") 
        
        print("+The angle between wind and conductor is = ", self.Case1.WINDANG_DEG, " DEG")
     

        if self.Case1.NSELECT == 1:
            print("INPUT -> Steady-state current: ", self.Case1.XIPRELOAD, " A")
            print("OUTPUT -> Steady-state temperature: ", self.str_round( self.Case1.TCDRPRELOAD), " ºC")    
        
        elif self.Case1.NSELECT == 2:
            print("INPUT -> Steady-state temperature: ", self.Case1.TCDRPRELOAD, " ºC")
            print("OUTPUT -> Steady-state current: ", self.str_round( self.Case1.TR), " A" )

        print("Solar heating:  ", self.str_round( self.Case1.QS), " W/m")
        print("Radiation cooling: ", self.str_round( self.Case1.QR), " W/m")
        print("Convection cooling: ", self.str_round( self.Case1.QC), " W/m")   
        print(f"Temperature difference between conductor surface and core: {self.str_round(self.deltaTcTs_value)} ºC")
   
   
   
    
    def print_ver(self):
        """Print the module name and release date to standard output."""
        print("CIGRE TB601. 2/5/2026. 15:35")
        
    
    def deltaTcTs(self):
        """Compute the temperature difference between conductor core and surface.

        Uses the effective radial thermal conductivity ``Cable1.lambda_ertc``
        and the steady-state current ``Case1.TR`` to evaluate the radial
        temperature gradient through the conductor cross-section.

        :return: Temperature difference between conductor core and surface
            in deg C.
        :rtype: float

        .. note::
            Sets ``self.deltaTcTs_value`` to the computed value.
        """
        D1 = self.Cable1.D1
        D = self.Cable1.D
        I = self.Case1.TR
        Rac = self.Rac()
        lambda_ertc = self.Cable1.lambda_ertc
          
        if self.Debug == 1:
            print("****************************************")
            print("Temperature difference between conductor surface and core")
            print("D1: ", D1, " mm; D: ", D, " mm; I: ", I, " A; Rac: ", Rac, " ohm/m; lambda_ertc: ", lambda_ertc, " W/m.K")
        
        deltaT = ((I*I*Rac)/(2*np.pi*lambda_ertc))*(0.5 - ((D1*D1)/(D*D - D1*D1))*(np.log(D/D1)))        
        self.deltaTcTs_value = deltaT   
        
        return deltaT