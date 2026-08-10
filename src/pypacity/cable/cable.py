# -*- coding: utf-8 -*-
"""
Module: cable.py

Description
-----------
Cable data structures and cable database loading helpers for PyPacity
ampacity studies.

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
- IEEE Std 738-2012, IEEE Standard for Calculating the Current-Temperature Relationship of Bare Overhead Conductors
- CIGRE Technical Brochure 601, Guide for Thermal Rating Calculations of Overhead Lines
- CIGRE Technical Brochure 207, Thermal Rating of Overhead Lines
"""


import pandas as pd
import os  


class Cable():
    """Electrical and thermal data for an overhead conductor.

    Stores the physical, electrical, and thermal properties of a bare overhead
    conductor. Properties are loaded from the built-in cable database via
    :meth:`set_cable` or assigned directly by the caller.

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Attributes</p>

    .. csv-table::
       :header: "Attribute", "Type", "Description"
       :widths: 20, 8, 72
       :align: center

       "``ID``", "str", "Conductor identifier."
       "``D``", "float", "Outside conductor diameter in millimeters."
       "``D1``", "float", "Equivalent steel-core tube diameter in millimeters."
       "``d``", "float", "Wire diameter in the outermost layer in millimeters."
       "``TLO``", "float", "Low reference temperature for resistance in deg C."
       "``THI``", "float", "High reference temperature for resistance in deg C."
       "``TCDRMAX``", "float", "Maximum allowable conductor temperature in deg C."
       "``RLO``", "float", "Conductor resistance at ``TLO`` in ohm/m."
       "``RHI``", "float", "Conductor resistance at ``THI`` in ohm/m."
       "``B``", "float", "Slope of the linear resistance-temperature equation in ohm/(m.deg C). Computed as ``(RHI - RLO) / (THI - TLO)``."
       "``B1``", "float", "Intercept of the linear resistance-temperature equation in ohm/m. Computed as ``RLO - B * TLO``."
       "``EMISS``", "float", "Surface emissivity coefficient."
       "``ABSORP``", "float", "Solar absorptivity coefficient."
       "``HNH``", "int", "Number of aluminum layers."
       "``Stranded``", "int", "1 for stranded conductors, 0 for smooth conductors."
       "``CrossSection``", "float", "Conductor cross-sectional area in mm²."
       "``MASSCORE``", "float", "Steel core mass per unit length in kg/m."
       "``MASSOUT``", "float", "Aluminum outer layer mass per unit length in kg/m."
       "``HEATOUT``", "float", "Aluminum heat capacity contribution in W.s/(m.deg C)."
       "``HEATCORE``", "float", "Steel-core heat capacity contribution in W.s/(m.deg C)."
       "``HEATCAP``", "float", "Total heat capacity per unit length in W.s/(m.deg C), equal to ``HEATOUT + HEATCORE``. Set by :meth:`set_cable`."
       "``deltaTcTs_value``", "float", "Temperature difference between conductor core and surface in deg C."
       "``CSteel20``", "float", "Steel specific heat at 20 deg C in J/(kg.K)."
       "``CAlum20``", "float", "Aluminum specific heat at 20 deg C in J/(kg.K)."
       "``BetaSteel20``", "float", "Steel specific-heat temperature coefficient."
       "``BetaAlum20``", "float", "Aluminum specific-heat temperature coefficient."
       "``mSteel``", "float", "Steel mass per unit length in kg/m."
       "``mAlum``", "float", "Aluminum mass per unit length in kg/m."
       "``lambda_ertc``", "float", "Effective radial thermal conductivity in W/(m.K)."
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

        Reads ``cable_db.csv`` from the same directory as this module. The
        file uses a semicolon separator and contains one row per conductor
        with the columns: ``ID``, ``D``, ``D1``, ``d``, ``TLO``, ``THI``,
        ``TCDRMAX``, ``RLO``, ``RHI``, ``HNH``, ``HEATOUT``, ``HEATCORE``.

        :return: A tuple ``(cable_db, error)`` where ``cable_db`` is a
            :class:`pandas.DataFrame` with one row per conductor, and
            ``error`` is ``0`` if at least one conductor was loaded or ``1``
            if the database file is empty.
        :rtype: tuple

        :raises FileNotFoundError: If ``cable_db.csv`` is not found in the
            package directory.
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

        Reads the conductor identified by ``conductor`` from ``cable_db.csv``,
        applies default material and surface properties, and then adjusts
        temperature limits and heat capacity values according to the analysis
        mode ``NSELECT``. Conductor matching is case-insensitive.

        :param NSELECT: Analysis mode selector:

            - ``1``: steady-state conductor temperature.
            - ``2``: steady-state ampacity; sets ``TCDRPRELOAD`` to 101.1 deg C.
            - ``3``: high-temperature transient; overrides ``HEATOUT``,
              ``HEATCORE``, and ``TCDRMAX``.
            - ``4``: limited-temperature transient; overrides ``TCDRMAX``,
              ``HEATOUT``, and ``HEATCORE``.

        :type NSELECT: int
        :param conductor: Conductor identifier as listed in ``cable_db.csv``.
            Defaults to ``'DRAKE'``.
        :type conductor: str

        :raises ValueError: If the cable database is empty or ``conductor``
            is not found in ``cable_db.csv``.

        .. note::
            Results are stored directly in the instance attributes (see class
            docstring) rather than returned. After this call, ``HEATCAP`` is
            set to ``HEATOUT + HEATCORE``.
        """
        data = self._get_cable_data(conductor)
        self._apply_cable_data(data)
        self._set_common_properties()
        self._apply_analysis_mode_overrides(NSELECT)
        self.HEATCAP = self.HEATCORE + self.HEATOUT

    def _get_cable_data(self, conductor):
        """Return the database row that matches a conductor ID.

        Strips leading and trailing whitespace from ``conductor`` before
        matching. Matching is case-insensitive, so ``drake``, ``DRAKE``,
        and ``Drake`` all select the same conductor.

        :param conductor: Conductor identifier to look up in ``cable_db.csv``.
        :type conductor: str

        :return: Row from ``cable_db.csv`` corresponding to the requested
            conductor.
        :rtype: pandas.Series

        :raises ValueError: If the cable database is empty, or if
            ``conductor`` is not found in ``cable_db.csv``. The error
            message lists the available conductor IDs when the conductor
            is unknown.
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

        Assigns the values from a single database row to the corresponding
        instance attributes. ``RLO`` and ``RHI`` are converted from ohm/km
        (as stored in ``cable_db.csv``) to ohm/m by dividing by 1000.

        :param data: Row from ``cable_db.csv`` for one conductor, as
            returned by :meth:`_get_cable_data`.
        :type data: pandas.Series

        .. note::
            Sets the following attributes: ``ID``, ``D``, ``D1``, ``d``,
            ``TLO``, ``THI``, ``TCDRMAX``, ``HEATOUT``, ``HEATCORE``,
            ``HNH``, ``RLO``, ``RHI``.
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
        """Set default material, surface, and thermal properties.

        Assigns the default values used by the built-in standard examples.
        These assumptions follow the IEEE 738 and CIGRE TB 601 reference
        cases and may be overwritten after :meth:`set_cable` if a study
        requires different conductor properties.

        .. note::
            Sets the following attributes with their default values:
            ``EMISS = 0.5``, ``ABSORP = 0.5``,
            ``CSteel20 = 481.0`` J/(kg.K), ``CAlum20 = 897.0`` J/(kg.K),
            ``BetaSteel20 = 1.00e-4``, ``BetaAlum20 = 3.80e-4``,
            ``mSteel = 0.5119`` kg/m, ``mAlum = 1.116`` kg/m,
            ``lambda_ertc = 0.7`` W/(m.K).
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

        Adjusts conductor temperature limits and heat capacity values
        according to the analysis mode before the solver runs. Values not
        covered by a given mode are left unchanged.

        :param NSELECT: Analysis mode selector. Recognised values:

            - ``2``: steady-state ampacity; sets ``TCDRPRELOAD`` to
              101.1 deg C.
            - ``3``: high-temperature transient; sets
              ``HEATOUT = 1066`` W.s/(m.deg C),
              ``HEATCORE = 243`` W.s/(m.deg C), and
              ``TCDRMAX = 1000`` deg C.
            - ``4``: limited-temperature transient; sets
              ``TCDRMAX = 150`` deg C,
              ``HEATOUT = 1066`` W.s/(m.deg C), and
              ``HEATCORE = 243`` W.s/(m.deg C).
            - Any other value: no overrides are applied.

        :type NSELECT: int

        .. note::
            For ``NSELECT = 3`` and ``NSELECT = 4``, the ``HEATOUT`` and
            ``HEATCORE`` values loaded from the database are replaced by
            fixed values from the IEEE 738 standard examples.
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
        """Print the module name and release date to standard output."""
        print("Cable. 05/6/2026.") 
