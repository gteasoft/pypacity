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
        ID (str): Conductor identifier.
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
        CSteel20 (float): Steel specific heat at 20 deg C in J/(kg.K).
        CAlum20 (float): Aluminum specific heat at 20 deg C in J/(kg.K).
        BetaSteel20 (float): Steel specific-heat temperature coefficient.
        BetaAlum20 (float): Aluminum specific-heat temperature coefficient.
        mSteel (float): Steel mass per unit length in kg/m.
        mAlum (float): Aluminum mass per unit length in kg/m.
        lambda_ertc (float): Effective radial thermal conductivity in W/(m.K).
    """
    
    def __init__(self):
        """Initialize an empty cable definition."""
        self.ID = None               # Conductor identifier.
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
        self.CSteel20 = None         # Steel specific heat at 20 deg C (J/(kg.K)).
        self.CAlum20 = None          # Aluminum specific heat at 20 deg C (J/(kg.K)).
        self.BetaSteel20 = None      # Steel specific-heat temperature coefficient.
        self.BetaAlum20 = None       # Aluminum specific-heat temperature coefficient.
        self.mSteel = None           # Steel mass per unit length (kg/m).
        self.mAlum = None            # Aluminum mass per unit length (kg/m).
        self.lambda_ertc = None      # Effective radial thermal conductivity (W/(m.K)).
      
   
   
    def load_cable_db(self):
        """Load the cable database distributed with this package.

        Returns:
            tuple: ``(cable_db, error)`` where ``cable_db`` is a pandas
            dataframe and ``error`` is 0 when data is loaded or 1 when the
            database is empty.
        """
        filename = u'cable_db.csv'

        package_dir = os.path.dirname(__file__)
        data_file_path = os.path.join(package_dir, filename) 
             
        cable_db = pd.read_csv(data_file_path, sep=';')
        
        if len(cable_db) < 1:
            error = 1
        else:
            error = 0
   
        return cable_db, error

    
    def set_cable(self, NSELECT, conductor='DRAKE'):
        """Load one conductor definition from the cable database.

        Args:
            NSELECT (int): Analysis mode used by the ampacity solver.
            conductor (str): Conductor ID.
        """
        data = self._get_cable_data(conductor)
        self._apply_cable_data(data)
        self._set_common_properties()
        self._apply_analysis_mode_overrides(NSELECT)
        self.HEATCAP = self.HEATCORE + self.HEATOUT

    def _get_cable_data(self, conductor):
        """Return the database row that matches a conductor ID.

        Matching is case-insensitive, so ``drake``, ``DRAKE``, and ``Drake``
        all select the same conductor if it exists in ``cable_db.csv``.

        Args:
            conductor (str): Conductor ID requested by the caller.

        Returns:
            pandas.Series: Row from ``cable_db.csv`` for the selected
            conductor.

        Raises:
            ValueError: If the database is empty or the conductor ID is
            unknown.
        """
        # Normalize user input before comparing it with database IDs.
        conductor_id = str(conductor).strip()

        cable_db, error = self.load_cable_db()
        if error:
            raise ValueError("Cable database is empty.")

        # Match conductor IDs without depending on upper/lower case.
        row = cable_db.loc[
            cable_db['ID'].astype(str).str.upper() == conductor_id.upper()
        ]
        if row.empty:
            # Include available IDs in the error message to help users fix typos.
            available = ', '.join(cable_db['ID'].astype(str))
            raise ValueError(
                "Unknown conductor '%s'. Available conductors: %s"
                % (conductor_id, available)
            )

        # There should be only one matching row for each conductor ID.
        return row.iloc[0]

    def _apply_cable_data(self, data):
        """Copy conductor-specific database values to this cable object.

        Args:
            data (pandas.Series): Row from ``cable_db.csv`` for one conductor.
        """
        self.ID = data['ID']

        for param in (
            'D', 'D1', 'd', 'TLO', 'THI', 'TCDRMAX', 'HEATOUT', 'HEATCORE'
        ):
            setattr(self, param, float(data[param]))

        self.HNH = int(data['HNH'])

        self.RLO = float(data['RLO']) / 1000.0 # ohm/m
        self.RHI = float(data['RHI']) / 1000.0 # ohm/m

    def _set_common_properties(self):
        """Set default properties shared by the built-in conductors.

        These values are assumptions used by the standard examples. They may
        be overwritten after ``set_cable()`` if a study requires different
        material, surface, or thermal properties.
        """
        self.EMISS = 0.5          # Default surface emissivity.
        self.ABSORP = 0.5         # Default solar absorptivity.
        self.CSteel20 = 481.0     # Steel specific heat at 20 deg C.
        self.CAlum20 = 897.0      # Aluminum specific heat at 20 deg C.
        self.BetaSteel20 = 1.00e-4
        self.BetaAlum20 = 3.80e-4
        self.mSteel = 0.5119      # Default steel mass per unit length.
        self.mAlum = 1.116        # Default aluminum mass per unit length.
        self.lambda_ertc = 0.7    # Effective radial thermal conductivity.

    def _apply_analysis_mode_overrides(self, NSELECT):
        """Apply mode-specific overrides for built-in ampacity examples.

        Different ``NSELECT`` values represent different study cases. These
        overrides intentionally change temperature limits or heat capacity
        values before the solver runs.
        """
        if NSELECT == 2:
            # Preload case: define the initial/preload conductor temperature.
            self.TCDRPRELOAD = 101.1

        elif NSELECT == 3:
            # High-temperature transient case using fixed heat capacity values.
            self.HEATOUT = 1066
            self.HEATCORE = 243
            self.TCDRMAX = 1000  

        elif NSELECT == 4:
            # Limited-temperature case using the same fixed heat capacity values.
            self.TCDRMAX = 150
            self.HEATOUT = 1066
            self.HEATCORE = 243
        
    def print_ver(self):        
        """Print the current version of this module."""
        print("Cable. 05/6/2026.") 
