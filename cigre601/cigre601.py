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
        self.Debug_Dec = 3 # number of decimal value for printing debug info
        self.Tolerance = 1 # Tolerance for temperature estimation
        self.MaxIterations = 400 # Maximum number of iteration
        self.error = 0 # 0 no error


    def set_error( self, error):
        """Set error value"""
        self.error = error
        return
    
    
    def get_error( self):
        """Get error value"""
        return( self.error)
    

    def set_cable( self, Cable):
        """Set the cable characteristics for a specific CIGRE TB601 analysis.

        Args:
            Cable (class Cable): Object of type Cable with information about the cable.
        """
        self.Cable1 = Cable
        return
        

    def set_case( self, Case):
        """Set the case characteristics for a specific CIGRE TB601 analysis.
        
        Args:
            Case (class Case): Object of type Case with information about the environmental and other physical conditions to consider in the dynamic operation of the cable.
        """
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
        """Computes the sin of angle [deg].
        
        Args:
            angle (float): angle in deg.
        """
        DEG_TO_RAD = np.pi/180
        return ( np.sin(DEG_TO_RAD*angle))
    
    def cosd( self, angle):
        """Computes the cos of angle [deg].
        
        Args:
            angle (float): angle in deg.
        """        
        DEG_TO_RAD = np.pi/180
        return( np.cos(DEG_TO_RAD*angle))    
  
    def solar( self):
        """Solar heating. Section 3.3 TB601. Pag. 18..
        
        """

        if self.Debug == 1:
            print("****************************************")
            print("Solar heating")
        
        DEG_TO_RAD = np.pi/180.0
        RAD_TO_DEG = 180.0/np.pi
             
        # 3.3 Pag. 18. Eq (8)
        if self.Case1.SolarRadiation != None:
            Psm = self.Cable1.ABSORP*self.Case1.SolarRadiation*self.Cable1.D/1000.0 
            if self.Debug == 1:
                print("Measured solar heating: " + self.str_round(Psm) + " W/m")
    
        # Z Hour angle of the Sun
        Z = -15*(12-self.Case1.SUN_TIME)
        if self.Debug == 1:
            print("Hour angle Z: " + self.str_round(Z) + " deg")
       
        # Declination
        deltas = 23.3*np.sin((2*np.pi*(284+self.Case1.NDAY))/365)
        if self.Debug == 1:
            print("Declination: " + self.str_round(deltas) + " deg")
       
        # Solar Altitude
        Hs = RAD_TO_DEG*np.arcsin( self.sind(self.Case1.CDR_LAT_DEG)*self.sind(deltas)+
                                  self.cosd(self.Case1.CDR_LAT_DEG)*self.cosd(deltas)*self.cosd(Z))
        if self.Debug == 1:
            print("Solar Altitude Hs: " + self.str_round(Hs) + " deg")
        
        # Azimuth of the Sun
        gammas = -RAD_TO_DEG*np.arcsin((self.cosd(deltas)*self.sind(Z))/(self.cosd(Hs)))
        if self.Debug == 1:
            print("gammas: " + self.str_round(gammas) + " deg")
            
        # Albedo
        if self.Debug == 1:
            print("Albedo F: " + self.str_round( self.Case1.ALBEDO))

        # IB(0) Pag. 19. Eq (10)
        IB0 = self.Case1.Ns*(1280*self.sind(Hs))/(self.sind(Hs)+0.314) 
        if self.Debug == 1:
            print("IB0: " + self.str_round(IB0) + " W/m^2")
        
        # IB(y) Pag. 19. Eq (11)
        IBy = IB0*(1 + 1.4e-4*self.Case1.CDR_ELEV*((1367/IB0)-1))
        if self.Debug == 1:
            print("IBy: " + self.str_round(IBy) + " W/m^2")
        
        # Id Difuse solar radiation Pag. 20. Eq (13)
        Id = (430.5 - 0.3288*IBy)*self.sind(Hs)
        if self.Debug == 1:
            print("Id: " + self.str_round(Id) + " W/m^2")
        
        # eta Pag. 20. Eq (14)
        eta = RAD_TO_DEG*np.arccos(self.cosd(Hs)*self.cosd(gammas - self.Case1.Z1_DEG))
        if self.Debug == 1:
            print("eta: " + self.str_round(eta) + " deg")
        
        # Computed solar heating. Pag. 18. Eq (9)
        # Global solar radiation
        IT = (IBy*(self.sind(eta) + (np.pi/2)*self.Case1.ALBEDO*self.sind(Hs)) + Id*(1+(np.pi/2*self.Case1.ALBEDO)))
        if self.Debug == 1:
            print("Global solar radiation IT: " + self.str_round(IT) + " W/m^2")
        Psc = self.Cable1.ABSORP*(self.Cable1.D/1000)*IT
        if self.Debug == 1:
            print("Computed solar heating: " + self.str_round(Psc) + " W/m")
           
        if self.Case1.SOLAR == 0:
            Ps = Psm
        else:
            Ps = Psc

        if self.Debug == 1:
            print("Ps: " + self.str_round(Ps) + " W/m")
        
        return Ps


    def radiation( self):
        """Computes the radiative cooling of conductor in W/m. 
        
        """
        # Pr Pag. 30. Eq (27).
        # sigmaB. Stefan-Boltzmann constant        
        sigmaB = 5.6697e-8 # W.m^(-2).K^(-4)
        
        Pr = np.pi*(self.Cable1.D/1000.0)*sigmaB*self.Cable1.EMISS*(pow(self.Case1.TCDR + 273,4)-pow(self.Case1.TAMB + 273,4))
        if self.Debug == 1:
            print("****************************************")
            print("Radiative cooling: " + self.str_round(Pr) + " W/m")
            
        return Pr
        

    def joule( self):
        """Computes the Joule heating of conductor in W/m.
        
        """
        Rac = self.Rac()
        
        if self.Case1.NSELECT == 1:
            I = self.Case1.XIPRELOAD
        elif self.Case1.NSELECT == 2:
            I = self.Case1.TR 
        elif self.Case1.NSELECT == 3:
            I = self.Case1.XISTEP
        elif self.Case1.NSELECT == 4:
            I = self.Case1.XISTEP 
        
        
        PJ =(Rac)*(I**2)
        self.Case1.QJ = PJ
        return PJ



    def convection( self):
        """Computes de convective cooling of conductor in W/m.
        
        """
        if self.Debug == 1:
            print("****************************************")
            print('Natural convection')
        
        # Film temperature
        Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        if self.Debug == 1:
            print("Tfilm Tf: " + self.str_round(Tf) + " ºC")
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        cf = 1006 
        if self.Debug == 1:
            print("Specific air heat capacity cf: " + self.str_round(cf) + " J/kg.ºK")
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        if self.Debug == 1:
            print("Thermal conductivity of the air lambdaf: " + self.str_round(lambdaf) + " W/ºK.m")
        # Dynamic viscosity [kg/m.s]
        muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6
        if self.Debug == 1:
            print("Dynamic viscosity muf: %.4e kg/m.s" %(muf))
        # Prandtl number, Pr = cf . muf / lambdaf   W/m
        Pr = cf*muf/lambdaf        
        if self.Debug == 1:
            print('Prandtl: ' + self.str_round(Pr)) 
            

        # Air density
        gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        if self.Debug == 1:
            print("Air density gamma: " + self.str_round(gamma) + " kg/m^3")

        # Kinematic viscosity
        vf = muf / gamma 
        if self.Debug == 1:
            print("Kinematic viscosity vf: %.4e m^2/s" %(vf))
        # Grashof number
        Gr = ((self.Cable1.D/1000)**3)*(self.Case1.TCDR - self.Case1.TAMB)*9.81/((Tf+273)*vf**2)
        if self.Debug == 1:
            print('Grashof: ' + self.str_round(Gr))
        
        # Table 5. Pg. 28
        GrPr = Gr*Pr
        if  GrPr < 1e2:
            A = 1.02
            m = 0.148
        elif (GrPr >= 1e2) and (GrPr < 1e4):
            A = 0.85
            m = 0.188
        elif (GrPr >= 1e4) and (GrPr < 1e7):
            A = 0.48
            m = 0.25
        elif GrPr >=1e7:
            A = 0.125
            m = 0.333

        Nunat = A*(GrPr)**m 
       
        if self.Cable1.Stranded == 1: # stranted conductor
            Nubeta = Nunat*(1 - 1.76e-6*(self.Case1.beta**2.5))
        else: # smooth conductor
            Nubeta = Nunat*(1 - 1.58e-4*(self.Case1.beta**1.5))
        
        Pcnat = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nunat
        if self.Debug == 1:
            print('Pc,nat: ' + self.str_round(Pcnat) + ' W/m')
        
        
        if self.Debug == 1:
            print("****************************************")
            print('Forced convection')

        # Film temperature
        #Tf = 0.5*(self.Case1.TCDR + self.Case1.TAMB)
        
        # Specific ¿air? heat capacity   [J/kg.K]      
        #cf = 1006 
        # Thermal conductivity of the air. Pag. 24. Eq (18) [W/k.m]
        #lambdaf = 2.368e-2 + 7.23e-5*Tf - 2.763e-8*(Tf**2)
        # Dynamic viscosity [kg/m.s]
        #muf = (17.239 + 4.635e-2*Tf - 2.03e-5*(Tf**2))*1e-6        
        # Air density
        #gamma = (1.293 - 1.525e-4*self.Case1.CDR_ELEV + 6.379e-9*(self.Case1.CDR_ELEV**2))/(1 + 0.00367*Tf)
        # Kinematic viscosity
        #vf = muf / gamma 
        
        # Reynolds number. Pag. 25
        Rey = self.Case1.VWIND*(self.Cable1.D/1000)/vf
        if self.Debug == 1:
            print("Reynolds number: " +self.str_round(Rey))
        
        # Roughness of the conductor        
        Rs = self.Cable1.d/(2*(self.Cable1.D - self.Cable1.d))
        if self.Debug == 1:
            print("Roughness of the conductor: " + self.str_round(Rs))
        
        if self.Cable1.Stranded == 1: # Stranded conductor
            if Rs <= 0.05:
                if Rey < 2650:
                    B = 0.641
                    n = 0.471
                else:
                    B = 0.178
                    n = 0.633
            else:
                if Rey < 2650:
                    B = 0.641
                    n = 0.471
                else:
                    B = 0.048
                    n = 0.8
        else: # Smooth conductor
            if Rey < 5000:
                B = 0.583
                n = 0.471
            elif (Rey >= 5000) and (Rey < 50000):
                B = 0.148
                n = 0.633
            else:
                B = 0.0208
                n = 0.814
        
        
        Nu90 = B*(Rey**n)
        if self.Debug == 1:
            print("Nu90: " + self.str_round(Nu90))
        
        if self.Cable1.Stranded == 1:
            if self.Case1.WINDANG_DEG <= 24:
                Nudelta = Nu90*(0.42 + 0.68*( self.sind(self.Case1.WINDANG_DEG)**1.08)) 
            else:
                Nudelta = Nu90*(0.42 + 0.58*( self.sind(self.Case1.WINDANG_DEG)**0.90)) 
        else:
            Nudelta = Nu90*(self.sind(self.Case1.WINDANG_DEG)**2 + 0.0169*self.cosd(self.Case1.WINDANG_DEG)**2)**0.225

        if self.Debug == 1:
            print("Nudelta: " + self.str_round(Nudelta))

        Pcfor = np.pi*lambdaf*(self.Case1.TCDR - self.Case1.TAMB)*Nudelta
        if self.Debug == 1:
            print("Pc forced: " + self.str_round(Pcfor) + " W/m")

        Pc = max( Pcnat, Pcfor)
        if self.Debug == 1:
            print("-----------------")
            print("Pconvective: " + self.str_round(Pc) + " W/m")
            
        return Pc


    def Rac( self):
        """Computes the equivalente conductor resistance [ohm/m] at operation temperature. 
        
        """
        
        alpha = (self.Cable1.RHI - self.Cable1.RLO)/(self.Cable1.THI - self.Cable1.TLO)
        if self.Debug == 1:
            print("****************************************")
            print("Rac(Tamb)")
            print("Conductor resistance temperature coefficient: %.4e ohm/m.ºC" %(alpha))
        
        Rac = self.Cable1.RLO + (self.Case1.TCDR - self.Cable1.TLO)*alpha
        if self.Debug == 1:
            print("Rac(TCDR): %.4e ohm/m" %(Rac) )
            
        return Rac



    def cigre601( self):
        """ 
        
        """

        if self.Case1.NSELECT == 1:
            #print("NSELECT == 1")
            self.conductor_temperature() 
        elif self.Case1.NSELECT == 2:
            self.Case1.TCDR = self.Case1.TCDRPRELOAD
            self.thermal_rating()
        elif self.Case1.NSELECT == 3:
            self.TCDR_vs_time() 
        elif self.Case1.NSELECT == 4:
            pass

        return
    

    def conductor_temperature( self):
        """Computes the conductor temperature 
        
        """
        
        TCDR = self.Cable1.TCDRMAX + 100
        Niterations = 0
        deltaI = 1
        
        
        # abs(balance) > self.Tolerance) 
        while (deltaI > 0) and (Niterations < self.MaxIterations):
            self.Case1.TCDRPRELOAD = TCDR 
            self.Case1.TCDR = self.Case1.TCDRPRELOAD         
            #TCDRold = TCDR 
            self.thermal_rating()
            #balance = self.Case1.QS + self.Case1.RAC*(self.Case1.XIPRELOAD**2) - self.Case1.QC - self.Case1.QR
            
            deltaI = self.Case1.TR - self.Case1.XIPRELOAD 

            if self.Debug == 1:
                print("Iteration: ", Niterations, "; DeltaI: ", deltaI, "; TCDR: ", TCDR, " ;Current: ", self.Case1.TR)

            if  deltaI > 0:
               TCDRold = TCDR
               TRold = self.Case1.TR
               TCDR -= 0.5
            else:
                TCDRx = TCDR + ((TCDRold - TCDR)/(TRold - self.Case1.TR))*(self.Case1.XIPRELOAD - self.Case1.TR)
                if self.Debug == 1:
                    print("Current: ", self.Case1.XIPRELOAD, " ; TCDR: ", TCDRx)
                 
            Niterations += 1
            
        
        self.Case1.TCDRPRELOAD = TCDRx   
            
    


    def TCDR_vs_time( self):
        """Computes the transient evolution of conductor temperature.
        
        """        
        t = 0
        Tc = 0
        time = []
        temp = []
        # starting point I = self.Case1.XIPRELOAD
        
        if self.Case1.TTfromST == 0:
            Tc = self.Case1.TCDRinitial
        elif self.Case1.TTfromST == 1:
            self.conductor_temperature()
            Tc = self.Case1.TCDRPRELOAD
       
        
        if self.Debug == 1:
            print("Starting point")
            print("Initial current: ", self.Case1.XIPRELOAD, " ; Initial temperature: ", self.Case1.TCDRPRELOAD)
            
        
        time.append(t)
        temp.append( Tc)
        
        
        # ma.ca
        maca = self.Cable1.mAlum*self.Cable1.CAlum20*(1+self.Cable1.BetaAlum20*(self.Case1.TCDRPRELOAD - 20.0))
        
        # mscs
        mscs = self.Cable1.mSteel*self.Cable1.CSteel20*(1+self.Cable1.BetaSteel20*(self.Case1.TCDRPRELOAD - 20.0))
        
        # mc
        mc = maca + mscs
        
        # Rac
        Rac = self.Rac()
        
        # PJ
        PJ = (Rac)*(self.Case1.XIPRELOAD**2)
        self.Case1.QJ = PJ
        
        # DeltaTime (update to use loaded values from IEEE case)
        deltaTime = 60.0
        # DeltaTemperature CIGRE601 Pag 86
        deltaT = (self.Case1.QJ + self.Case1.QS - self.Case1.QR - self.Case1.QC)*deltaTime/(mc)
        
        if self.Case1.SORM == 1:
            tend = self.Case1.TT*60
        else:
            tend = self.Case1.TT
            
        steps = int(tend/self.Case1.DELTIME)
        print("steps: ", steps)
        for i in range(steps):
            print("Tinitial: ", Tc, " ; dT: ", deltaT) 
            t += deltaTime
            Tc += deltaT
            time.append( t)
            temp.append( Tc)
            self.Case1.TCDR = Tc
            Pj = self.joule() 
            Ps = self.solar()
            Pr = self.radiation()
            Pc = self.convection()
            deltaT = (Pj + Ps - Pr - Pc)*deltaTime/(mc)
            
            
        self.Case1.TIME = time
        self.Case1.ATCDR = temp              
        
        


   
    def thermal_rating( self):
        """Implementation of CIGRE TB601.
        

        """ 

        # Solar heating
        Ps = self.solar()
        self.Case1.QS = Ps
       
        # Radiation cooling 
        Pr = self.radiation()
        self.Case1.QR = Pr
    
        # Convective cooling
        Pc = self.convection()
        self.Case1.QC = Pc
        
        # Rac
        Rac = self.Rac()
        self.Case1.RAC = Rac
        
        interm = Pr + Pc - Ps
        if interm < 0:
            self.error = 100 # no thermal balance
            interm *= (-1)
            print('CIGRE inconsistency -> Ps: %.2f; Pr:%.2f; Pc:%.2f' %(Ps, Pr, Pc))
            print('VWIND: %.2f; WINDANG_DEG: %.2f; SolarRadiation: %.2f' %(self.Case1.VWIND, self.Case1.WINDANG_DEG, self.Case1.SolarRadiation))
        I = np.sqrt((interm)/(Rac))
        self.Case1.TR = I
        if self.Debug == 1:
            print("Dynamic Current Rating: " + self.str_round(I) + " A")
    
        return I       


    def str_round( self, valuex):
        """Obtain the rounded value of <valuex> acording the variable <self.Debug_Dec>. 
               
        Args:
            valuex (float): value to be rounded according the number of decimal values defined by <self.Debug_Dec>.
        """
        return str( round( valuex, self.Debug_Dec))

    
    def output( self):
        """Print a summary of intermediate results
            
        """
        print(" ")
        print(" ")
        print("*******************************************************************")
        print("*******************************************************************")
        print("CIGRE TB601 ")
        print("*******************************************************************") 
            

        if self.Case1.NSELECT == 1:
            print("INPUT -> Steady-state current: ", self.Case1.XIPRELOAD, " A")
            print("OUTPUT -> Steady-state temperature: ", self.str_round( self.Case1.TCDRPRELOAD), " ºC")    
        
        elif self.Case1.NSELECT == 2:
            print("INPUT -> Steady-state temperature: ", self.Case1.TCDRPRELOAD, " ºC")
            print("OUTPUT -> Steady-state current: ", self.str_round( self.Case1.TR), " A" )

        print("Solar heating:  ", self.str_round( self.Case1.QS), " W/m")
        print("Radiation cooling: ", self.str_round( self.Case1.QR), " W/m")
        print("Convection cooling: ", self.str_round( self.Case1.QC), " W/m")   
   
   
   
    
    def print_ver( self):
        """Print version of cigre601 module.
        
        """
        print("CIGRE TB601. 12/4/2023. 19:12") 