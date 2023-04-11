# -*- coding: utf-8 -*-
import numpy as np
import sys
from cable import cable
from case import case
from importlib import reload
reload( cable)
reload( case)

class CIGRE601():
    """Implementation of CIGRE TB601"""
    
    def __init__(self):
        self.Cable1 = cable.Cable()
        self.Case1 = case.Case()
        self.Debug = 1 # 1 print intermediate values


    def set_cable( self, Cable):
        """_summary_

        Args:
            Cable (class Cable): XX
        """
        self.Cable1 = Cable
        return
        

    def set_case( self, Case):
        self.Case1 = Case

        if type(self.Case1.CDR_LAT_DEG) == None:
            self.Case1.CDR_LAT_DEG = 0
        
        if type(self.Case1.NDAY) == None:
            self.Case1.NDAY = 0
        
        if type(self.Case1.SUN_TIME) == None:
            self.Case1.SUN_TIME = 0
       
        if type(self.Case1.A3) == None:
            self.Case1.A3 = 0       
            
        return

    def sind( self, angle):
        DEG_TO_RAD = np.pi/180
        return ( np.sin(DEG_TO_RAD*angle))
    
    def cosd( self, angle):
        DEG_TO_RAD = np.pi/180
        return( np.cos(DEG_TO_RAD*angle))    
  
    def solar( self):
        """Solar heating. Section 3.3 TB601. Pag. 18.
        
        """
        DEG_TO_RAD = np.pi/180.0
        RAD_TO_DEG = 180.0/np.pi
             
        # 3.3 Pag. 18. Eq (8)
        if self.Case1.SolarRadiation != None:
            Psm = self.Cable1.ABSORP*self.Case1.SolarRadiation*self.Cable1.D/1000.0 
            if self.Debug == 1:
                print("Measured solar heating: " + str(Psm) + " W/m")
    
        # Z Hour angle of the Sun
        Z = -15*(12-self.Case1.SUN_TIME)
       
        # Declination
        deltas = 23.3*np.sin((2*np.pi*(284+self.Case1.NDAY))/365)
        if self.Debug == 1:
            print("Declination: " + str(deltas) + " degrees")
       
        # Solar Altitude
        Hs = RAD_TO_DEG*np.arcsin( self.sind(self.Case1.CDR_LAT_DEG)*self.sind(deltas)+
                                  self.cosd(self.Case1.CDR_LAT_DEG)*self.cosd(deltas)*self.cosd(Z))
        if self.Debug == 1:
            print("Solar Altitude Hs: " + str(Hs) + " degrees")
        
        # Azimuth of the Sun
        gammas = RAD_TO_DEG*np.arcsin((self.cosd(deltas)*self.sind(Z))/(self.cosd(Hs)))

        # IB(0) Pag. 19. Eq (10)
        IB0 = self.Case1.Ns*(1280*self.sind(Hs))/(self.sind(Hs)+0.314) 
        
        # IB(y) Pag. 19. Eq (11)
        IBy = IB0*(1 + 1.4e-4*self.Case1.CDR_ELEV*((1367/IB0)-1))
        
        # Id Difuse solar radiation Pag. 20. Eq (13)
        Id = (430.5 - 0.3288*IBy)*self.sind(Hs)
        
        # eta Pag. 20. Eq (14)
        eta = RAD_TO_DEG*np.arccos(self.cosd(Hs)*self.cosd(gammas - self.Case1.Z1_DEG))
        
        # Computed solar heating. Pag. 18. Eq (9)
        Psc = self.Cable1.ABSORP*(self.Cable1.D/1000)*(IBy*(self.sind(eta) + (np.pi/2)*self.Case1.ALBEDO*self.sind(Hs)) + Id*(1+(np.pi/2*self.Case1.ALBEDO)))
        if self.Debug == 1:
            print("Computed solar heating: " + str(Psc) + " W/m")
           
        if self.Case1.SOLAR == 0:
            return Psm
        else:
            return Psc


    def radiation( self):
        """. 
        
        """
        # Pr Pag. 30. Eq (27)
        # sigmaB. Stefan-Boltzmann constant        
        sigmaB = 5.6697e-8 # W.m^(-2).K^(-4)
        
        Pr = np.pi*(self.Cable1.D/1000.0)*sigmaB*self.Cable1.EMISS*(pow(self.Cable1.TCDRMAX + 273,4)-pow(self.Case1.TAMB + 273,4))
        if self.Debug == 1:
            print("Radiative cooling: " + str(Pr) + " W/m")
            
        return Pr
        

    def natural_convection( self):
        """ 
        
        """
        print('Natural Convection')
        
        # Film temperature
        Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        cf = 1006 
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        # Dynamic viscosity [kg/m.s]
        muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6
        # Prandtl number, Pr = cf . muf / lambdaf   W/m
        Pr = cf*muf/lambdaf        
        if self.Debug == 1:
            print('Prandtl: ' + str(Pr)) 
            

        # Air density
        gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        # Kinematic viscosity
        vf = muf / gamma 
        # Grashof number
        Gr = ((self.Cable1.D/1000)**3)*(self.Case1.TCDR - self.Case1.TAMB)*9.81/((Tf+273)*vf**2)
        if self.Debug == 1:
            print('Grashof: ' + str(Gr))
        
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
       
        if self.Cable1.Stranded == 1: # stranted conductor
            Nubeta = Nunat*(1 - 1.76e-6*(self.Case1.beta**2.5))
        else: # smooth conductor
            Nubeta = Nunat*(1 - 1.58e-4*(self.Case1.beta**1.5))
        
        Pcnat = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nunat
        if self.Debug == 1:
            print('Pc,nat: ' + str(Pcnat) + ' W/m')
        
        

    def forced_convection( self):
        """ 
        
        """
        print('Forced convection')

        # Film temperature
        Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        cf = 1006 
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        # Dynamic viscosity [kg/m.s]
        muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6        
        # Air density
        gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        # Kinematic viscosity
        vf = muf / gamma 
        
        # Reynolds number. Pag. 25
        Rey = self.Case1.VWIND*(self.Cable1.D/1000)/vf
        
        # Roughness of the conductor        
        Rs = self.Cable1.d/(2*(self.Cable1.D - self.Cable1.d))
        
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
        
        if self.Cable1.Stranded == 1:
            if self.Case1.WINDANG_DEG <= 24:
                Nudelta = Nu90*(0.42 + 0.68*( self.sind(self.Case1.WINDANG_DEG)**1.08)) 
            else:
                Nudelta = Nu90*(0.42 + 0.58*( self.sind(self.Case1.WINDANG_DEG)**0.90)) 
        else:
            Nudelta = Nu90*(self.sind(self.Case1.WINDANG_DEG)**2 + 0.0169*self.cosd(self.Case1.WINDANG_DEG)**2)**0.225

        Pcfor = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nudelta
        if self.Debug == 1:
            print("Pc forced: " + str(Pcfor) + " W/m")

   
    def cigre601( self):
        """Implementation of CIGRE TB601.
        

        """ 

        # Solar heating
        Ps = self.solar()
        self.Case1.QS = Ps
        
        Pr = self.radiation()
        self.Case1.QR = Pr
    
        return 1.0       
    
    def output( self):
        """
            
        """ 
        print("Solar heating: ", self.Case1.QS, " W/m")
        print("Radiation cooling: ", self.Case1.QR, " W/m")
        print("Convection cooling: ", self.Case1.QC, " W/m")
            
        

   
   
   
   
    
    def print_ver( self):
        """XX"""
        print("CIGRE TB601. 30/3/2023. 23:15") 