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

  
    def solar( self):
        """ 
        
        """
        
             
        # 3.3 Pag. 18. Eq (8)
        if self.Case1.SolarRadiation != None:
            Ps = self.Cable1.ABSORP*self.Case1.SolarRadiation*self.Cable1.D/1000.0 
    
    
        # Z Hour angle of the Sun
        Z = 15*(12-self.Case1.SUN_TIME)
        
    
    
        return Ps
        
   
    def cigre601( self):
        """Implementation of CIGRE TB601.
        

        """ 

        # Solar heating
        Ps = self.solar()
        self.Case1.QS = Ps
        
    
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