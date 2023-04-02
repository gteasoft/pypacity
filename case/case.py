# -*- coding: utf-8 -*-

class Case():
    """Case"""
    
    def __init__(self):
        self.NSELECT = None        # Analysis Mode
        self.IORTPRELOAD = None    #
        self.SORM = None           # Unit of time for output print. 0: seconds; 1: minutes
        self.TT = None             # Simulation time in seconds
        self.DELTIME = None        # Delta t in seconds
        self.TCDRPRELOAD = None    # Steady-state conductor temperature
        self.XIPRELOAD = None      # Initial current
        self.XISTEP = None         # Final current
        self.TAMB = None           # Ambient temperature in DEG C
        self.T4 = None # Ambient temperature in KELVIN
        self.VWIND = None          # Wind speed (m/s)
        self.WINDANG_DEG = None    # Angle between wind & conductor axis in DEG
        self.WINDANG_RAD = None  # Angle between wind & conductor axis in RAD
        self.CDR_ELEV = None       # CDR ELEV ABOVE SEA LEVEL IN METERS
        self.Z1_DEG = None         # CDR DIRECTION CW RELATIVE TO NORTH
        self.CDR_LAT_DEG = None    # CDR LATITUDE IN DEGREES
        self.SUN_TIME = None       # SOLAR HOUR 14 = 2PM OR 99(NO SUN)
        self.NDAY = None           # DAY OF THE YEAR
        self.A3 = None             # AIR CLARITY - CLEAR(0), INDUST(1)
        self.SolarRadiation = None # Solar Radiation
        self.ATCDR = []          # Inicialization
        self.TIME = []           # Inicialization
        self.TCDR = 50 # EXPECTED CONDUCTOR TEMPERATURE IN CELSIUS
        self.T3 = None  # EXPECTED CONDUCTOR TEMPERATURE IN KELVIN
        self.B = None
        self.B1 = None
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
        
    

        


    def demo( self, NSELECT):
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
        self.WINDANG_DEG = 90.0
        self.CDR_ELEV = 0.0
        self.Z1_DEG = 45.0
        self.CDR_LAT_DEG = 43.0
        self.SUN_TIME = 12
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
            self.ITCDRPRELOAD = 40
            self.TCDRMAX = 150
            self.SORM = 1
            self.TT = 1800
            self.DELTIME = 60
            self.HNH = 2
           
       
        if self.A3 == 0:
            self.Bstring = "CLEAR"
        else:
            self.Bstring = "INDUSTRIAL"

 
    def print_ver( self):
        print("Case. 30/3/2023. 23:15") 