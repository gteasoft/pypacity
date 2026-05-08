# -*- coding: utf-8 -*-
import pandas as pd
import os  


class Cable():
    """
    Definition of cable XX
    
    Defines an object of the class Cable() including basic information about the cable:
    
    
    Attributes:
        :Cstring (str): Conductor description.
        :D (float): Outside diameter of conductor (mm).
        :D1 (float): Diameter of a tubular conductor of the steel core (mm).
        :d (float): Diameter of the wires in the outermost layer (mm).
        :TLO (float): Conductor minimum temperature for resistance computation (ºC). 
        :THI (float): Conductor maximum temperature for resistance computation (ºC).
        :TCDRMAX (float): Maximum conductor temperature (ºC).
        :RLO (float): Conductor resistance at TLO (Ohms/m).
        :RHI (float): Conductor resistance at THI (Ohms/m).
        :EMISS (float): Coefficient of emission.
        :ABSORP (float): Coefficient of solar absorption.
        :HNH (int): Number of layers (aluminum)
        :HEATOUT (float): Aluminum layer (W.s/m.ºC)
        :HEATCORE (float): Steel core (W.s/m.ºC)
    """
    
    def __init__(self):

        self.Cstring = None        # Conductor description
        self.D = None              # Outside diameter of conductor  (mm)
        self.D1 = None             # Diameter of a tubular conductor of the steel core (mm)
        self.d = None              # Diameter of the wires in the outermost layer
        self.TLO = None            # MIN CDR TEMP IN DEG C for conductor resistance
        self.THI = None            # MAX CDR TEMP IN DEG C for conductor resistance
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
        self.Stranded = 1  # 1.- Stranted conductor; 0.- Smooth conductor
        self.CrossSection = None
        self.MASSCORE = None # Mass per unit length steel (kg/m)
        self.MASSOUT = None # Mass per unit length aluminum (kg/m)
        self.deltaTcTs_value = None # Temperature difference between core and surface
        self.lambda_ertc = None # Effective radial thermal conductivity (W/m-K)   
        
   
   
    def load_cable_db( self):
        """Load cable database
        
            The cable database is a file with name 'cable_db.xlsx' that is located in the same folder of cable module.

        :return cable_db, error: cable_db is a dataframe with the cable database. error is 1 if the database is empty. 0 is the load process is sucessful.
        :rtype: dataframe, int               
        """
        filename = u'cable_db.xlsx'

        package_dir = os.path.dirname(__file__)
        data_file_path = os.path.join( package_dir, filename) 
        
        # print('ruta: ', data_file_path) # print the full path
        
        cable_db = pd.read_excel( data_file_path)
        
        if len( cable_db) < 1:
            error = 1
        else:
            error = 0
   
        return cable_db, error

    
    def set_cable( self, NSELECT, conductor = 'Demo case' ):
        """
        Load a demo case.. Ejemplo para Alberto

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
            self.D1 = 10.4
            self.d = 4.44
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
            self.TotalS = 486.6
            self.CSteel20 = 481
            self.CAlum20 = 897
            self.BetaSteel20 = 1.00e-4
            self.BetaAlum20 = 3.80e-4
            self.mSteel = 0.5119
            self.mAlum = 1.116
            self.lambda_ertc = 0.7
        elif conductor == '400 mm2 DRAKE 26/7 ACSR':
            self.Cstring = '400 mm2 DRAKE 26/7 ACSR'
            self.D = 28.12
            self.D1 = 10.4
            self.d = 4.44
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
            self.TotalS = 486.6
            self.CSteel20 = 481
            self.CAlum20 = 897
            self.BetaSteel20 = 1.00e-4
            self.BetaAlum20 = 3.80e-4
            self.mSteel = 0.5119
            self.mAlum = 1.116
            self.lambda_ertc = 0.7
        elif conductor == 'LA-180':
            self.Cstring = 'LA-180'
            self.D = 17.50
            self.D1 = 10.4
            self.d = 2.50
            self.TLO = 5.0
            self.THI = 85.0
            self.TCDRMAX = 101.0
            self.RLO = 0.21993/1000.0
            self.RHI = 0.25197/1000.0
            self.EMISS = 0.5
            self.ABSORP = 0.5
            self.HNH = 2
            self.HEATOUT = 379.81
            self.HEATCORE = 128.16
            self.TotalS = 486.6
            self.CSteel20 = 481
            self.CAlum20 = 897
            self.BetaSteel20 = 1.00e-4
            self.BetaAlum20 = 3.80e-4
            self.mSteel = 0.5119
            self.mAlum = 1.116
            self.lambda_ertc = 0.7
        elif conductor == 'LA-280':
            self.Cstring = 'LA-280'
            self.D = 21.80
            self.D1 = 10.4
            self.d = 3.44
            self.TLO = 5.0
            self.THI = 85.0
            self.TCDRMAX = 101.0
            self.RLO = 0.13384/1000.0
            self.RHI = 0.15707/1000.0
            self.EMISS = 0.5
            self.ABSORP = 0.5
            self.HNH = 2
            self.HEATOUT = 379.81
            self.HEATCORE = 128.16
            self.TotalS = 486.6
            self.CSteel20 = 481
            self.CAlum20 = 897
            self.BetaSteel20 = 1.00e-4
            self.BetaAlum20 = 3.80e-4
            self.mSteel = 0.5119
            self.mAlum = 1.116   
            self.lambda_ertc = 0.7 
        elif conductor == 'HERON':
            self.Cstring = 'HERON'
            self.D = 22.96
            self.D1 = 8.61
            self.d = 3.60
            self.TLO = 5.0
            self.THI = 85.0
            self.TCDRMAX = 100.0
            self.RLO = 0.1122/1000.0
            self.RHI = 0.1507/1000.0
            self.EMISS = 0.5
            self.ABSORP = 0.5
            self.HNH = 3
            self.HEATOUT = 623.0
            self.HEATCORE = 147.0
            self.TotalS = 486.6
            self.CSteel20 = 481
            self.CAlum20 = 897
            self.BetaSteel20 = 1.00e-4
            self.BetaAlum20 = 3.80e-4
            self.mSteel = 0.5119
            self.mAlum = 1.116
            self.lambda_ertc = 0.7                    
            
                                   
  
    
        if NSELECT == 2:
            self.TCDRPRELOAD = 101.1
            #self.TCDRMAX = 1000.0
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
        """Set the parameter <param> to value <value>

        :param param: Parameter.
        :type param: Depends on the parameter
        :return: 1 if the update is successful and 0 if the update is wrong
        :rtype: int
        """
        if param == 'D':
            self.D = value
   
    def print_ver( self):        
        """Returns the current version of this module

        :return: Current version of Cable module.
        :rtype: string

        """
        print("Cable. 30/3/2023. 23:16") 