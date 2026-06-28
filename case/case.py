# -*- coding: utf-8 -*-
"""
Module: case.py

Description
-----------
Operating-case data model for PyPacity ampacity calculations.

Author
------
Mario Mañana

Copyright
---------
Copyright (c) 2026 Mario Mañana

License
-------
MIT License

Notes
-----
This module is part of the PyPacity project.

References
----------
- IEEE Std 738-2012, IEEE Standard for Calculating the Current-Temperature Relationship of Bare Overhead Conductors
- CIGRE Technical Brochure 601, Guide for Thermal Rating Calculations of Overhead Lines
- CIGRE Technical Brochure 207, Thermal Rating of Overhead Lines
"""


class Case():
    """Environmental and operational inputs for an ampacity study.

    Collects all inputs required by the IEEE 738 and CIGRE TB 601/207
    solvers and exposes the results once the solver completes. Inputs are
    set directly on the instance; results are read from the same object
    after the solver method returns.

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Simulation inputs</p>

    .. csv-table::
       :header: "Attribute", "Type", "Standard", "Description"
       :widths: 18, 8, 12, 62
       :align: center

       "``NSELECT``", "int", "Both", "Analysis mode: ``1`` steady-state conductor temperature, ``2`` steady-state ampacity, ``3`` transient conductor temperature, ``4`` transient thermal rating."
       "``TT``", "int", "Both", "Total simulation time. Units are controlled by ``SORM``."
       "``SORM``", "int", "Both", "Time unit selector: ``0`` for seconds, ``1`` for minutes."
       "``DELTIME``", "int", "Both", "Simulation time step in seconds."
       "``IORTPRELOAD``", "int", "IEEE 738", "Initial condition mode for transient analyses (``NSELECT = 3`` or ``4``): ``1`` computes ``TCDRPRELOAD`` from ``XIPRELOAD`` via iteration, ``2`` uses ``TCDRPRELOAD`` directly (only valid for ``NSELECT = 4``)."
       "``TCDRPRELOAD``", "float", "Both", "Initial or target steady-state conductor temperature in deg C."
       "``XIPRELOAD``", "float", "Both", "Initial (preload) current in amperes."
       "``XISTEP``", "float", "Both", "Final step current in amperes."
       "``TTfromST``", "int", "CIGRE", "Transient start mode: ``1`` starts from the steady-state temperature, ``0`` starts from ``TCDRinitial``. Defaults to ``1``."
       "``TCDRinitial``", "float", "CIGRE", "Initial conductor temperature in deg C when ``TTfromST = 0``."

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Environmental conditions</p>

    .. csv-table::
       :header: "Attribute", "Type", "Standard", "Description"
       :widths: 18, 8, 12, 62
       :align: center

       "``TAMB``", "float", "Both", "Ambient air temperature in deg C."
       "``VWIND``", "float", "Both", "Wind speed in m/s."
       "``DWIND_DEG``", "float", "Both", "Wind direction in degrees (compass bearing)."
       "``WINDANG_DEG``", "float", "Both", "Effective angle between wind direction and conductor axis in degrees. IEEE 738 and CIGRE TB 601 compute it automatically from ``DWIND_DEG`` and ``Z1_DEG``; CIGRE TB 207 reads it directly, so it must already be set when 207 runs standalone."
       "``CDR_ELEV``", "float", "Both", "Conductor elevation above sea level in meters."
       "``Z1_DEG``", "float", "Both", "Conductor direction clockwise from north in degrees."
       "``CDR_LAT_DEG``", "float", "Both", "Conductor latitude in degrees."
       "``beta``", "float", "CIGRE", "Conductor inclination to the horizontal in degrees. Defaults to ``0``."

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Solar settings</p>

    .. csv-table::
       :header: "Attribute", "Type", "Standard", "Description"
       :widths: 18, 8, 12, 62
       :align: center

       "``SUN_TIME``", "float", "Both", "Solar hour in the range 0-24. Set to ``99`` (or any value ``≥ 24``) to use ``SolarRadiation`` directly as the solar irradiance instead of computing it from position, date, and time."
       "``NDAY``", "int", "Both", "Day of year in the range 1 to 365."
       "``A3``", "int", "Both", "Atmospheric clarity selector: ``0`` for clear air, ``1`` for industrial atmosphere."
       "``Ns``", "float", "CIGRE", "Clearness ratio as defined in CIGRE TB 601. Defaults to ``1.0`` (clear sky)."
       "``SolarRadiation``", "float", "Both", "Measured solar radiation intensity in W/m2."
       "``ALBEDO``", "float", "CIGRE", "Ground reflectance coefficient. Defaults to ``0.0``."
       "``SOLAR``", "int", "CIGRE", "Solar source selector: ``0`` uses ``SolarRadiation``, ``1`` computes solar heat gain from date, time, and location."

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Results</p>

    .. csv-table::
       :header: "Attribute", "Type", "Standard", "Description"
       :widths: 18, 8, 12, 62
       :align: center

       "``TR``", "float", "Both", "Steady-state thermal rating in amperes. Populated after ``NSELECT = 2``."
       "``TCDRPRELOAD``", "float", "Both", "Also used as a result: steady-state conductor temperature in deg C populated after ``NSELECT = 1``."
       "``XISTEP``", "float", "Both", "Transient thermal rating current in amperes. Populated after ``NSELECT = 4``."
       "``ATCDR``", "list", "Both", "Transient conductor temperature trace in deg C. Populated after ``NSELECT = 3`` or ``4``."
       "``TIME``", "list", "Both", "Transient time trace in seconds. Populated after ``NSELECT = 3`` or ``4``."
       "``QS``", "float", "Both", "Solar heat gain rate in W/m."
       "``QR``", "float", "Both", "Radiative heat loss rate in W/m."
       "``QC``", "float", "Both", "Convective heat loss rate in W/m."
       "``QJ``", "float", "CIGRE", "Joule heating rate (I2 x Rac) in W/m."
       "``RAC``", "float", "CIGRE", "Conductor AC resistance at the operating temperature in ohm/m."
       "``KTIMEMAX``", "int", "IEEE 738", "Total number of time steps computed. Populated after ``NSELECT = 3`` or ``4``."

    .. note::
        The following attributes are internal solver variables used as
        intermediate working storage during iteration and should not be
        modified directly: ``XLO``, ``XHI``, ``W4``, ``R5``, ``Q1``,
        ``Q2``, ``T3``, ``T4``, ``T5``, ``U1``, ``P1``, ``K1``,
        ``YC``, ``WINDANG_RAD``, ``NFLAG``, ``AT``, ``TCDR``,
        ``XIDUMMY``, ``Bstring``, and others initialised in ``__init__``.
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
        self.SUN_TIME = None        # Solar hour (0-24), or ≥ 24 to use SolarRadiation as irradiance directly.
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
        """Populate the case with sensible default values for a quick-start study.

        Provides a baseline configuration drawn from the IEEE 738 standard
        sample calculations. The defaults can be used as-is with the IEEE 738
        solver or overridden by the caller before passing the case to a CIGRE
        solver. CIGRE-specific attributes (``Ns``, ``ALBEDO``, ``SOLAR``,
        ``beta``, ``TTfromST``, ``TCDRinitial``) are not set here and retain
        their ``__init__`` defaults; override them after calling this method if
        a CIGRE study requires non-default values. Solar heat input is taken
        from the measured ``SolarRadiation`` value (``SUN_TIME = 99``) instead
        of being computed from the Sun's position. The following base values
        are set for all modes:

        .. csv-table::
           :header: "Attribute", "Value", "Description"
           :widths: 20, 18, 62
           :align: center

           "``TAMB``", "40 °C", "Ambient temperature."
           "``VWIND``", "0.61 m/s", "Wind speed."
           "``DWIND_DEG``", "90°", "Wind direction."
           "``WINDANG_DEG``", "90°", "Wind perpendicular to conductor axis."
           "``CDR_LAT_DEG``", "43°", "Conductor latitude."
           "``CDR_ELEV``", "0 m", "Sea level."
           "``Z1_DEG``", "0°", "Conductor direction."
           "``NDAY``", "161", "Day of year (June 10)."
           "``SUN_TIME``", "99", "Use measured ``SolarRadiation`` as the irradiance instead of computing it."
           "``A3``", "0", "Clear atmosphere."
           "``SolarRadiation``", "708.6 W/m2", "Used as solar irradiance Q3 when ``SUN_TIME = 99``."
           "``IORTPRELOAD``", "1", "Preload temperature computed from ``XIPRELOAD``."
           "``TCDRPRELOAD``", "101.1 °C", "Initial conductor temperature."
           "``XIPRELOAD``", "1000 A", "Preload current."
           "``XISTEP``", "1000 A", "Step current."
           "``SORM``", "0", "Time expressed in seconds."
           "``TT``", "6000 s", "Total simulation time (100 min)."
           "``DELTIME``", "10 s", "Simulation time step."

        :param NSELECT: Analysis mode. ``NSELECT = 1`` and ``NSELECT = 2``
            use only the base values above. ``NSELECT = 3`` and
            ``NSELECT = 4`` apply the following overrides on top:

            - ``3`` (transient conductor temperature): ``XIPRELOAD = 400 A``,
              ``XISTEP = 1200 A``, ``SORM = 1``, ``TT = 7200``,
              ``DELTIME = 30 s``, ``HNH = 2``.
            - ``4`` (transient thermal rating): ``IORTPRELOAD = 2``,
              ``TCDRPRELOAD = 40 °C``, ``TCDRMAX = 150 °C``,
              ``SORM = 1``, ``TT = 1800``, ``DELTIME = 60 s``,
              ``HNH = 2``.

        :type NSELECT: int

        .. note::
            The base values listed above are overwritten on this instance.
            CIGRE-specific attributes and solver state variables retain
            their ``__init__`` defaults.
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
        """Print the module name and release date to standard output."""
        print("Case. 5/6/2026.")
