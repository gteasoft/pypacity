# -*- coding: utf-8 -*-

class Cable():
    """
    Definition of cable
    
    
    
    """
    
    def __init__(self):

        self.Cstring = None        # Conductor description
        self.D = None              # Conductor diameter (mm)
        self.TLO = None            # MIN CDR TEMP IN DEG C
        self.THI = None            # MAX CDR TEMP IN DEG C
        self.TCDRMAX = None        # TCDRMAX
        self.RLO = None            # MIN CDR RAC (OHMS/m)
        self.RHI = None            # MAX CDR RAC (OHMS/m)
        self.EMISS = None          # COEF OF EMISS
        self.ABSORP = None         # COEF OF SOLAR ABSORP
        self.HNH = None            # Number of layers (aluminum)
        self.HEATOUT = None        # ALUMINUM LAYER (W-SEC/M-C)
        self.HEATCORE = None       # STEEL CORE (W-SEC/M-C)
        self.B = None
        self.B1 = None
    
    def demo( self, NSELECT, conductor = 'Demo case' ):
        """
        Load a demo case.

        :param NSELECT: Type of computation
        :type NSELECT: int
        :param conductor: Conductor ID. Type of conductor. By default the function defines a demo case that is based on 400 mm2 DRAKE 26/7 ACSR
        :type conductor: string
        :return: None.
        :rtype: -       
        """
        if  conductor == 'Demo case':
            self.Cstring = 'Demo case'
            self.D = 28.12
            self.TLO = 25.0
            self.THI = 75.0
            self.TCDRMAX = 101.0
            self.RLO = 0.07284/1000.0
            self.RHI = 0.08689/1000.0
            self.EMISS = 0.5
            self.ABSORP = 0.5
            self.HNH = 3
            self.HEATOUT = 1139.5
            self.HEATCORE = 351.7
        elif conductor == '400 mm2 DRAKE 26/7 ACSR':
            self.Cstring = '400 mm2 DRAKE 26/7 ACSR'
            self.D = 28.12
            self.TLO = 25.0
            self.THI = 75.0
            self.TCDRMAX = 101.0
            self.RLO = 0.07284/1000.0
            self.RHI = 0.08689/1000.0
            self.EMISS = 0.5
            self.ABSORP = 0.5
            self.HNH = 3
            self.HEATOUT = 1139.5
            self.HEATCORE = 351.7
            
  
    
        if NSELECT == 2:
            self.TCDRPRELOAD = 101.1
            self.TCDRMAX = 1000.0
        elif NSELECT == 3:
            self.HEATOUT = 1066
            self.HEATCORE = 243
            self.TCDRMAX = 1000  
        elif NSELECT == 4:
            self.TCDRMAX = 150
            self.HEATOUT = 1066
            self.HEATCORE = 243
            
        self.HEATCAP = self.HEATCORE + self.HEATOUT     
        
       

    def set_param( self, param, value):
        """xxxx

        :param kind: Optional "kind" of ingredients.
        :type kind: list[str] or None
        :return: The ingredients list.
        :rtype: list[str]
        """
        if param == 'D':
            self.D = value
   
    def print_ver( self):        
        """Returns the current version of this module

        :return: Current version of Cable module.
        :rtype: string

        """
        print("Cable. 30/3/2023. 23:16") 