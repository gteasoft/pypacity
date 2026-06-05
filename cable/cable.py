# -*- coding: utf-8 -*-
"""
Module: cable.py

Description
-----------
Cable data structures and cable database loading helpers for PyPacity
ampacity studies.

Author
------
Mario Manana

Copyright
---------
Copyright (c) 2026 Mario Manana

License
-------
MIT License

Notes
-----
This module is part of the PyPacity project.
"""


import pandas as pd
import os  


class Cable():
    """Electrical and thermal data for an overhead conductor.

    Attributes:
        Cstring (str): Conductor description.
        D (float): Outside conductor diameter in millimeters.
        D1 (float): Equivalent steel-core tube diameter in millimeters.
        d (float): Wire diameter in the outermost layer in millimeters.
        TLO (float): Low reference temperature for resistance in deg C.
        THI (float): High reference temperature for resistance in deg C.
        TCDRMAX (float): Maximum allowable conductor temperature in deg C.
        RLO (float): Conductor resistance at ``TLO`` in ohm/m.
        RHI (float): Conductor resistance at ``THI`` in ohm/m.
        EMISS (float): Surface emissivity coefficient.
        ABSORP (float): Solar absorptivity coefficient.
        HNH (int): Number of aluminum layers.
        HEATOUT (float): Aluminum heat capacity contribution in W.s/(m.deg C).
        HEATCORE (float): Steel-core heat capacity contribution in W.s/(m.deg C).
        Stranded (int): 1 for stranded conductors, 0 for smooth conductors.
        lambda_ertc (float): Effective radial thermal conductivity in W/(m.K).
    """
    
    def __init__(self):
        """Initialize an empty cable definition."""
        self.Cstring = None          # Conductor description.
        self.D = None                # Outside conductor diameter (mm).
        self.D1 = None               # Equivalent steel-core tube diameter (mm).
        self.d = None                # Wire diameter in the outermost layer (mm).
        self.TLO = None              # Low reference temperature for resistance (deg C).
        self.THI = None              # High reference temperature for resistance (deg C).
        self.TCDRMAX = None          # Maximum allowable conductor temperature (deg C).
        self.RLO = None              # Resistance at TLO (ohm/m).
        self.RHI = None              # Resistance at THI (ohm/m).
        self.EMISS = None            # Surface emissivity coefficient.
        self.ABSORP = None           # Solar absorptivity coefficient.
        self.HNH = None              # Number of aluminum layers.
        self.HEATOUT = None          # Aluminum heat capacity contribution (W.s/(m.deg C)).
        self.HEATCORE = None         # Steel-core heat capacity contribution (W.s/(m.deg C)).
        self.B = None
        self.B1 = None
        self.Stranded = 1            # 1 for stranded conductors, 0 for smooth conductors.
        self.CrossSection = None
        self.MASSCORE = None         # Steel mass per unit length (kg/m).
        self.MASSOUT = None          # Aluminum mass per unit length (kg/m).
        self.deltaTcTs_value = None  # Temperature difference between core and surface.
        self.lambda_ertc = None      # Effective radial thermal conductivity (W/(m.K)).
      
   
   
    def load_cable_db( self):
        """Load the cable database distributed with this package.

        Returns:
            tuple: ``(cable_db, error)`` where ``cable_db`` is a pandas
            dataframe and ``error`` is 0 when data is loaded or 1 when the
            database is empty.
        """
        filename = u'cable_db.csv'

        package_dir = os.path.dirname(__file__)
        data_file_path = os.path.join( package_dir, filename) 
             
        cable_db = pd.read_csv( data_file_path, sep=';')
        
        if len( cable_db) < 1:
            error = 1
        else:
            error = 0
   
        return cable_db, error

    
    def set_cable( self, NSELECT, conductor = 'Demo case' ):
        """Load one of the built-in conductor definitions.

        Args:
            NSELECT (int): Analysis mode used by the ampacity solver.
            conductor (str): Conductor ID. The default demo case is based on
                the 400 mm2 DRAKE 26/7 ACSR conductor.
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
            
                                   
  
        # Analysis-mode overrides used by the built-in examples.
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
        """Set a supported cable parameter.

        Args:
            param (str): Parameter name. Currently only ``D`` is supported.
            value: Value assigned to the selected parameter.
        """
        if param == 'D':
            self.D = value
   
    def print_ver( self):        
        """Print the current version of this module."""
        print("Cable. 05/6/2026.") 
