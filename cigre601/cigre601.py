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
        Z = 15*(12-self.Case1.SUN_TIME)
       
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
        Psc = -self.Cable1.ABSORP*(self.Cable1.D/1000)*(IBy*(self.sind(eta) + (np.pi/2)*self.Case1.ALBEDO*self.sind(Hs)) + Id*(1+(np.pi/2*self.Case1.ALBEDO)))
        if self.Debug == 1:
            print("Computed solar heating: " + str(Psc) + " W/m")
           
        if self.Case1.SOLAR == 0:
            return Psm
        else:
            return Psc


    def radiation( self):
        """ 
        
        """
        # Pr Pag. 30. Eq (27)
        # sigmaB. Stefan-Boltzmann constant        
        sigmaB = 5.6697e-8 # W.m^(-2).K^(-4)
        
        Pr = np.pi*(self.Cable1.D/1000.0)*sigmaB*self.Cable1.EMISS*(pow(self.Cable1.TCDRMAX + 273,4)-pow(self.Case1.TAMB + 273,4))
        if self.Debug == 1:
            print("Radiative cooling: " + str(Pr) + " W/m")
            
        return Pr
        
   
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