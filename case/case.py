# -*- coding: utf-8 -*-
"""
Module: case.py

Description
-----------
Operating-case data model for PyPacity ampacity calculations.

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


class Case():
    """Environmental and operational inputs for an ampacity study.

    Attributes:
        NSELECT (int): Analysis mode.

            1. Steady-state conductor temperature. Given current and weather
            conditions, the solver returns conductor temperature.
            2. Steady-state conductor current. Given conductor temperature and
            weather conditions, the solver returns current.
            3. Transient conductor temperature after a current step.
            4. Transient thermal rating to reach the maximum conductor
            temperature in the requested time.

        TT (int): Simulation time. Units are controlled by ``SORM``.
        SORM (int): Time unit selector, 0 for seconds and 1 for minutes.
        DELTIME (int): Simulation time step in seconds.
        TCDRPRELOAD (float): Initial steady-state conductor temperature.
        XIPRELOAD (float): Initial current in amperes.
        XISTEP (float): Final step current in amperes.
        TAMB (float): Ambient temperature in deg C.
        VWIND (float): Wind speed in m/s.
        DWIND_DEG (float): Wind direction in degrees.
        WINDANG_DEG (float): Angle between wind and conductor axis in degrees.
        CDR_ELEV (float): Conductor elevation above sea level in meters.
        Z1_DEG (float): Conductor direction clockwise from north in degrees.
        CDR_LAT_DEG (float): Conductor latitude in degrees.
        SUN_TIME (float): Solar hour. Use 99 when sun is not considered.
        NDAY (int): Day of year in the range 1 to 365.
        A3 (int): Air clarity selector, 0 for clear air and 1 for industrial.
        Ns (float): Clearness ratio from CIGRE TB601.
        SolarRadiation (float): Measured solar radiation in W/m2.
        ALBEDO (float): Ground reflectance coefficient.
        SOLAR (int): Solar source selector, 0 for measured and 1 for computed.
    """

    def __init__(self):
        """Initialize an empty ampacity case with default placeholders."""
        self.NCIRCUITS = 1          # Number of electrical circuits.
        self.NSELECT = None         # Analysis mode.
        self.IORTPRELOAD = None
        self.SORM = None            # Time unit selector: 0 seconds, 1 minutes.
        self.TT = None              # Simulation time.
        self.DELTIME = None         # Simulation time step (s).
        self.TCDRPRELOAD = None     # Steady-state conductor temperature (deg C).
        self.XIPRELOAD = None       # Initial current (A).
        self.XISTEP = None          # Final current after a step (A).
        self.TAMB = None            # Ambient temperature (deg C).
        self.T4 = None              # Ambient temperature (K).
        self.VWIND = None           # Wind speed (m/s).
        self.DWIND_DEG = None       # Wind direction (deg).
        self.WINDANG_DEG = None     # Angle between wind and conductor axis (deg).
        self.WINDANG_RAD = None     # Angle between wind and conductor axis (rad).
        self.CDR_ELEV = None        # Conductor elevation above sea level (m).
        self.Z1_DEG = None          # Conductor direction clockwise from north (deg).
        self.CDR_LAT_DEG = None     # Conductor latitude (deg).
        self.SUN_TIME = None        # Solar hour, or 99 when sun is ignored.
        self.NDAY = None            # Day of year.
        self.A3 = None              # Air clarity: 0 clear, 1 industrial.
        self.Ns = 1.0               # Clearness ratio, CIGRE TB601 page 19.
        self.SolarRadiation = None  # Measured solar radiation (W/m2).
        self.ATCDR = []             # Transient conductor temperature trace.
        self.TIME = []              # Transient time trace.
        self.TCDR = 50              # Expected conductor temperature (deg C).
        self.T3 = None              # Expected conductor temperature (K).
        self.ALBEDO = 0.0           # Ground reflectance coefficient.
        self.SOLAR = 0              # 0 uses measured radiation, 1 computes it.
        self.beta = 0               # Conductor inclination to the horizontal.
        self.B = None
        self.B1 = None

        # Legacy solver state and intermediate values used by translated routines.
        self.NFLAG = 0
        self.XLO = None
        self.XHI = None
        self.AT = None
        self.DIV = None
        self.ET = None
        self.Bstring = None
        self.T5 = None
        self.U1 = None
        self.P1 = None
        self.K1 = None
        self.QCF = None
        self.Q1 = None
        self.Q2 = None
        self.YC = None
        self.TR = None
        self.QS = None
        self.QR = None
        self.QC = None
        self.XLI = None
        self.XRI = None
        self.EPS = None
        self.IEND = None
        self.IER = None
        self.XL = None
        self.XR = None
        self.X = None
        self.TOL = None
        self.F = None
        self.TEMP = None
        self.FL = None
        self.FR = None
        self.I = None
        self.DA = None
        self.DX = None
        self.XM = None
        self.FM = None
        self.CHA = None
        self.FO = None
        self.NUM = None
        self.FF = None
        self.W4 = None
        self.R5 = None
        self.K = None
        self.KTIMEMAX = None
        self.RAC = None
        self.QJ = None              # Joule heating (W/m).
        self.TTfromST = 1           # 1 starts transient from steady-state temperature.
        self.TCDRinitial = None     # Initial transient temperature when TTfromST is 0.

    def demo(self, NSELECT):
        """Populate the case with built-in demo values.

        Args:
            NSELECT (int): Demo analysis mode. Valid values are 1, 2, 3 and 4.
        """
        self.NSELECT = NSELECT
        self.IORTPRELOAD = 1
        self.SORM = 0
        self.TT = 100*60
        self.DELTIME = 10
        self.TCDRPRELOAD = 101.1
        self.XIPRELOAD = 1000
        self.XISTEP = 1000
        self.TAMB = 40
        self.VWIND = 0.61
        self.DWIND_DEG = 90.0
        self.WINDANG_DEG = 90.0
        self.CDR_ELEV = 0.0
        self.Z1_DEG = 0.0
        self.CDR_LAT_DEG = 43.0
        self.SUN_TIME = 99
        self.NDAY = 161
        self.A3 = 0
        self.SolarRadiation = 708.6
        self.ATCDR = []
        self.TIME = []
        self.XIDUMMY = 0
        self.TR = None
        self.QS = 0
        self.TCDR = 50

        if NSELECT == 2:
            pass
        elif NSELECT == 3:
            self.XIPRELOAD = 400
            self.XISTEP = 1200
            self.SORM = 1
            self.TT = 7200
            self.DELTIME = 30
            self.HNH = 2
        elif NSELECT == 4:
            self.IORTPRELOAD = 2
            self.TCDRPRELOAD = 40
            self.TCDRMAX = 150
            self.SORM = 1
            self.TT = 1800
            self.DELTIME = 60
            self.HNH = 2

        if self.A3 == 0:
            self.Bstring = "CLEAR"
        else:
            self.Bstring = "INDUSTRIAL"

    def print_ver(self):
        """Print the current version of this module."""
        print("Case. 5/6/2026.")
