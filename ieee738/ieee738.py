# -*- coding: utf-8 -*-
import numpy as np
import sys
from cable import cable
from case import case
from importlib import reload
reload( cable)
reload( case)

class IEEE738():
    """Implementation of the IEEE 738:2012.
    
    
    """
    #DEG_TO_RAD = np.pi/180
     
    
    def __init__(self):
        self.Cable1 = cable.Cable()
        self.Case1 = case.Case()
        self.Debug = 1 # 1 print intermediate values
        self.Debug_Dec = 3 # number of decimal value for printing debug info

    
    def set_cable( self, Cable):
        """Set the cable characteristics for a specific IEEE 738 analysis.

        Args:
            Cable (class Cable): Object of type Cable with information about the cable.
        """
        self.Cable1 = Cable
        return
        

    def set_case( self, Case):
        """Set the case characteristics for a specific IEEE 738 analysis.
        
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
     
       
    
    # 10 REM *****************************************************************
    # 20 REM * IEEE METHOD - TRANSIENT OR STEADY STATE CALCULATION
    # 30 REM * OF BARE OVERHEAD CONDUCTOR TEMPERATURE OR THERMAL RATING
    # 40 REM *
    # 50 REM *
    # 60 REM *
    # 70 REM * ASSUMES SI UNITS FOR INPUT
    # 80 REM *
    # 90 REM *
    # 240 REM * IN COMPARISON WITH THE 1986 VERSION OF THIS PROGRAM, PROVIDED
    # 250 REM * BY THE IEEE, THE 1993 VERSION ADDED THE FOLLOWING FEATURES:
    # 260 REM *
    # 290 REM * - INITIAL CONDUCTOR TEMP OR CURRENT CAN BE USED IN
    # 300 REM * TRANSIENT CALCULATIONS
    # 330 REM * - VERY SHORT DURATION "FAULT" CURRENTS AS LARGE AS 1E6
    # 340 REM * AMPERES FOR TIMES AS SHORT AS 0.01 SEC CAN BE USED
    # 350 REM * - THE ORIGINAL NUMERICAL ITERATION METHOD HAS BEEN
    # 360 REM * REPLACED WITH A MUCH MORE EFFICIENT METHOD
    # 370 REM * - FOR ACSR CONDUCTOR, THE HEAT CAPACITY OF THE STEEL CORE
    # 380 REM * AND THE OUTER ALUM STRANDS ARE ENTERED SEPARATELY.
    # 390 REM *
    # 392 REM * THIS VERSION IS CONSISTENT WITH IEEE 738-2012
    # 394 REM * - THE SOLAR MODEL ALLOWS ANY HOUR AND LATITUDE
    # 396 REM * - THE AIR PROPERTIES ARE CALCULATED WITH CLOSED FORM EQUATIONS
    # 398 REM * - THIS PROGRAM AND EQUATIONS USE SI UNITS
    # 400 REM **************************************************************
    def ieee_738_2013( self, out = False):
        """Implementation of IEEE 738:2013.
        
        
        """
        # 590 REM *******************************
        # 600 REM * START REPEAT CALCULATION HERE
        # 610 REM *******************************
        # for KI=0:999 #para 1000 elementos
        #     data['ATCDR'][KI] = 0
        #     data['TIME'[KI] = 0
        # end
        self.Case1.ATCDR.append(0)
        self.Case1.TIME.append(0)
        self.Case1.NFLAG=0
        PIANG=np.pi/180
    
        # 1120 REM *****************************************
        # 1130 REM * CALCULATE SOLAR HEAT INPUT TO CONDUCTOR
        # 1140 REM *****************************************
        self.solar()
    
        #1160 REM **************************************************************
        #1170 REM * CALCULATE THERMAL COEF OF RESISTANCE & WIND ANGLE CORRECTION
        #1180 REM **************************************************************
        self.thermal()
    
        #1200 REM ********************************
        #1210 REM * SELECT THE CALCULATION DESIRED
        #1220 REM ********************************
        #1230 ON NSELECT GOTO 1500, 1240, 1460, 1460
        #no switch/case in python. Use if/elif/elif... instead    
        if self.Case1.NSELECT == 1:    #STEADY-STATE TEMP
            #1470 REM ********************************************
            #1480 REM * CALCULATE TCDR GIVEN XIDUMMY = XIPRELOAD *
            #1490 REM ********************************************
            self.Case1.XIDUMMY = self.Case1.XIPRELOAD
            self.Case1.NFLAG = 0
            self.mueller()
            self.Case1.TCDRPRELOAD = self.Case1.TCDR
            #1540 REM ***************************************************************
            #1550 REM * FOR NSELECT = 1 THE PROGRAM HAS FOUND THE STEADY STATE CONDUCTOR
            #1560 REM * TEMPERATURE (TCDRPRELOAD) CORRESPONDING TO THE GIVEN STEADY STATE
            #1570 REM * CURRENT (XIPRELOAD)
            #1580 REM **********************************************
        elif self.Case1.NSELECT == 2: #STEADY-STATE RATING
            #1240 REM ********************************************************************
            #1250 REM * FOR NSELECT = 2
            #1260 REM * GO TO AMPACITY SUBROUTINE TO CALCULATE THE STEADY STATE
            #1270 REM * CURRENT (TR) GIVEN THE STEADY STATE CONDUCTOR TEMPERATURE (TCDR)
            #1280 REM * THE CONDUCTOR TEMPERATURE IS GIVEN SO ONLY ONE PASS THROUGH
            #1290 REM * THE SUBROUTINE IS REQUIRED.
            #1300 REM ********************************************************************
            self.Case1.TCDR = self.Case1.TCDRPRELOAD
            self.thermal_rating()
        elif self.Case1.NSELECT == 3: #TRANSIENT TEMP
            #1360 REM ********************************************************************
            #1370 REM * FOR NSELECT = 1,3,OR 4
            #1380 REM * GO TO AMPACITY SUBROUTINE REPEATEDLY IN ORDER TO CALCULATE
            #1390 REM * THE STEADY STATE CURRENT (TR) CORRESPONDING TO TRIAL VALUES OF
            #1400 REM * CONDUCTOR TEMPERATURE (TCDR). IF T=1 THEN THE OUTPUT OF THE
            #1410 REM * SUBROUTINE, TR, IS THE STEADY STATE CURRENT FOR
            #1420 REM * WHICH A STEADY STATE TEMPERATURE WAS TO BE FOUND.
            #1430 REM * IF T=3 OR 4 AND IORTPRELOAD=1, THEN TR IS THE INITIAL PRE-STEP
            #1440 REM * CHANGE CURRENT FOR WHICH AN INITIAL TEMPERATURE WAS TO BE CALCULATED.
            #1450 REM *********************************************************************
            #1460 ON IORTPRELOAD GOTO 1500, 1650
            if self.Case1.IORTPRELOAD == 1:
                #1470 REM ********************************************
                #1480 REM * CALCULATE TCDR GIVEN XIDUMMY = XIPRELOAD *
                #1490 REM ********************************************
                self.Case1.XIDUMMY = self.Case1.XIPRELOAD
                self.Case1.NFLAG = 0
                self.mueller()
                self.Case1.TCDRPRELOAD = self.Case1.TCDR    
                #1540 REM ***************************************************************
                #1550 REM * FOR NSELECT = 1 THE PROGRAM HAS FOUND THE STEADY STATE CONDUCTOR
                #1560 REM * TEMPERATURE (TCDRPRELOAD) CORRESPONDING TO THE GIVEN STEADY STATE
                #1570 REM * CURRENT (XIPRELOAD) AND CONTROL IS PASSED TO THE PRINTOUT SECTION
                #1580 REM ***************************************************************
                #1590 IF NSELECT = 1 THEN 1730
                #1600 REM *****************************************************************
                #1610 REM * FOR NSELECT = 3 OR 4, THE PROGRAM HAS DETERMINED (IORTPRELOAD=1) OR BEEN
                #1620 REM * GIVEN (IORTPRELOAD=2) THE INITIAL STEADY STATE CONDUCTOR TEMPERATURE
                #1630 REM * AND CONTROL PASSES TO FURTHUR TRANSIENT CALCULATIONS
                #1640 REM *****************************************************************
                #1650 IF NSELECT = 4 THEN GOSUB 10000
                #1660 REM *************************************************************
                #1670 REM * BEGIN CALCULATION OF CONDUCTOR TEMP AS A FUNCTION OF TIME
                #1680 REM * FOR A STEP INCREASE IN ELECTRICAL CURRENT, NSELECT = 3
                #1690 REM *************************************************************
                self.Case1.ET = 3600
                self.Case1.XISTEP = self.Case1.XISTEP ######    data['XISTEP'] = data['XISTEP']
                self.TCDR_vs_TIME()
            else:
                    pass
            
        elif self.Case1.NSELECT == 4: #TRANSIENT RATING
            #1360 REM ********************************************************************
            #1370 REM * FOR NSELECT = 1,3,OR 4
            #1380 REM * GO TO AMPACITY SUBROUTINE REPEATEDLY IN ORDER TO CALCULATE
            #1390 REM * THE STEADY STATE CURRENT (TR) CORRESPONDING TO TRIAL VALUES OF
            #1400 REM * CONDUCTOR TEMPERATURE (TCDR). IF T=1 THEN THE OUTPUT OF THE
            #1410 REM * SUBROUTINE, TR, IS THE STEADY STATE CURRENT FOR
            #1420 REM * WHICH A STEADY STATE TEMPERATURE WAS TO BE FOUND.
            #1430 REM * IF T=3 OR 4 AND IORTPRELOAD=1, THEN TR IS THE INITIAL PRE-STEP
            #1440 REM * CHANGE CURRENT FOR WHICH AN INITIAL TEMPERATURE WAS TO BE CALCULATED.
            #1450 REM *********************************************************************
            #1460 ON IORTPRELOAD GOTO 1500, 1650
            if self.Case1.IORTPRELOAD  == 1:
                #1470 REM ********************************************
                #1480 REM * CALCULATE TCDR GIVEN XIDUMMY = XIPRELOAD *
                #1490 REM ********************************************
                self.Case1.XIDUMMY = self.Case1.XIPRELOAD
                self.Case1.NFLAG = 0
                self.mueller()
                self.Case1.TCDRPRELOAD = self.Case1.TCDR            
            
                #1540 REM ***************************************************************
                #1550 REM * FOR NSELECT = 1 THE PROGRAM HAS FOUND THE STEADY STATE CONDUCTOR
                #1560 REM * TEMPERATURE (TCDRPRELOAD) CORRESPONDING TO THE GIVEN STEADY STATE
                #1570 REM * CURRENT (XIPRELOAD) AND CONTROL IS PASSED TO THE PRINTOUT SECTION
                #1580 REM ***************************************************************
                #1590 IF NSELECT = 1 THEN 1730
            else:
                #1600 REM *****************************************************************
                #1610 REM * FOR NSELECT = 3 OR 4, THE PROGRAM HAS DETERMINED (IORTPRELOAD=1) OR BEEN
                #1620 REM * GIVEN (IORTPRELOAD=2) THE INITIAL STEADY STATE CONDUCTOR TEMPERATURE
                #1630 REM * AND CONTROL PASSES TO FURTHUR TRANSIENT CALCULATIONS
                #1640 REM *****************************************************************
                #1650 IF NSELECT = 4 THEN GOSUB 10000
                self.starting_ci()
                #1660 REM *************************************************************
                #1670 REM * BEGIN CALCULATION OF CONDUCTOR TEMP AS A FUNCTION OF TIME
                #1680 REM * FOR A STEP INCREASE IN ELECTRICAL CURRENT, NSELECT = 3
                #1690 REM *************************************************************
                self.Case1.ET = 3600
                self.Case1.XISTEP = self.Case1.XISTEP
                self.TCDR_vs_TIME()
            
        if out == True:
            self.output()
        #20000 REM /////////////////////
        #20010 REM / COMMENTS ON PROGRAM
        #20020 REM /////////////////////
        #20030 REM *
        #20040 REM * THE PROGRAM DOES NOT CALCULATE ANY INTERNAL RADIAL OR AXIAL
        #20050 REM * TEMPERATURE GRADIENTS. THIS IS NORMALLY NOT A SOURCE OF
        #20060 REM * SIGNIFICANT ERROR EXCEPT FOR INTERNALLY COMPLEX CONDUCTORS
        #20070 REM * SUCH AS FIBER-OPTIC SHIELD WIRE AND FOR NON-HOMOGENEOUS CONDUCTORS
        #20080 REM * FOR FAULT CURRENTS OF LESS THAN 1 MINUTE. THE PROGRAM DOES NOT
        #20090 REM * APPLY TO INTERNALLY COMPLEX CONDUCTORS, IT DOES CALCULATE A WORST
        #20100 REM * CASE ESTIMATE OF TEMPERATURE/RATING FOR ACSR OR ACSR/AW BY NEGLECTING
        #20110 REM * THE HEAT STORAGE CAPACITY OF THE RELATIVELY POORLY CONDUCTING CORE
        #20120 REM * FOR STEP CURRENTS WHICH PERSIST FOR LESS THAN ONE MINUTE.
        #20130 REM * THE VARIATION IN SPECIFIC HEAT WITH TEMPERATURE IS NEGLECTED.
        #20140 REM * ADDED COMMENTS 7/97 DAD
        #20150 REM * ADDED SI FORMULAS, SOLAR EQUATIONS, AND CHANGED AIR PARAMETERS
        return 
        
        #End Function ieee_738           
    
    
    
    ########################################################################
    # Conductor solar heat gain (QS)
    # 5000 REM /////////////////////////////////////////////////////////
    # 5010 REM / SUBROUTINE TO CALCULATE CONDUCTOR SOLAR HEAT GAIN (QS)
    # 5020 REM /////////////////////////////////////////////////////////
    ########################################################################
    def solar( self):
        """Compute the conductor solar heat gain (QS).
        
        :return: Value of solar heat gain QS in W/m.
        """
        DEG_TO_RAD = np.pi/180
        #self.CDR_LAT_RAD = self.Case1.CDR_LAT_DEG*self.DEG_TO_RAD
        CDR_LAT_RAD = self.Case1.CDR_LAT_DEG*DEG_TO_RAD # Conductor latitude in radians
   
    
        #5060 REM * SOLAR DECLINATION
        #data['DECL_DEG'] = 23.4583*np.sin(((284 + data['NDAY'])/365)*2*np.pi)
        #data['DECL_RAD'] = data['DECL_DEG']*data['DEG_TO_RAD']
        DECL_DEG = 23.4583*np.sin(((284 + self.Case1.NDAY)/365)*2*np.pi)
        DECL_RAD = DECL_DEG*DEG_TO_RAD     
        
    
        #5090 REM * SOLAR ANGLE RELATIVE TO NOON
        #data['HOUR_ANG_DEG'] = (data['SUN_TIME']-12)*15
        #data['HOUR_ANG_RAD'] = data['HOUR_ANG_DEG']*data['DEG_TO_RAD']
        HOUR_ANG_DEG = (self.Case1.SUN_TIME-12)*15
        HOUR_ANG_RAD = HOUR_ANG_DEG*DEG_TO_RAD
    
        #5120 REM * FIND SOLAR ALTITUDE - H3
        #data['H3ARG'] = (np.cos(data['CDR_LAT_RAD'])*np.cos(data['DECL_RAD'])*np.cos(data['HOUR_ANG_RAD'])
        #                +np.sin(data['CDR_LAT_RAD'])*np.sin(data['DECL_RAD']))
        #data['H3_RAD'] = np.arctan(data['H3ARG']/np.sqrt(1-data['H3ARG']**2))
        #data['H3_DEG'] = data['H3_RAD']/data['DEG_TO_RAD']
        H3ARG = (np.cos(CDR_LAT_RAD)*np.cos(DECL_RAD)*np.cos(HOUR_ANG_RAD) \
                     +np.sin(CDR_LAT_RAD)*np.sin(DECL_RAD))
        
        H3_RAD = np.arctan(H3ARG/np.sqrt(1-(H3ARG)**2))
        H3_DEG = H3_RAD/DEG_TO_RAD
  
        if self.Case1.A3 == 1:
        #5260 REM *****************************************************************
        #5270 REM * SOLAR HEAT (Q3) AT EARTH SURFACE (W/M2) IN INDUSTRIAL AIR (P6)
        #5280 REM *****************************************************************
            Q3 = 53.1821 + 14.211*H3_DEG + 0.66138*(H3_DEG)**2 
            Q3 += -0.031658*(H3_DEG)**3 + 5.4654E-04*(H3_DEG)**4
            Q3 += -4.3446E-06*(H3_DEG)**5 + 1.3236E-08*(H3_DEG)**6
            self.Bstring = 'INDUSTRIAL'
        elif self.Case1.A3 == 0:
        #5180 REM ***************************************************************
        #5190 REM * SOLAR HEATING (Q3) AT EARTH SURFACE (W/M2) IN CLEAR AIR (P6)
        #5200 REM ***************************************************************
            Q3 = -42.2391 + 63.8044*H3_DEG - 1.922*(H3_DEG)**2
            Q3 += 0.034692*(H3_DEG)**3 - 3.6112E-04*(H3_DEG)**4
            Q3 += 1.9432E-06*(H3_DEG)**5 - 4.0761E-09*(H3_DEG)**6
            self.Bstring = 'CLEAR'
    
        #5330 REM * CALCULATE SOLAR AZIMUTH VARIABLE, CHI
        auxi1 = (np.sin(CDR_LAT_RAD)*np.cos(HOUR_ANG_RAD) \
              - np.cos(CDR_LAT_RAD)*np.tan(DECL_RAD))
        CHI = np.sin(HOUR_ANG_RAD)/auxi1
    
        #5360 REM * CALCULATE SOLAR AZIMUTH CONSTANT, CAZ
        if (HOUR_ANG_DEG < 0) and (CHI >= 0):
            CAZ = 0
        elif (HOUR_ANG_DEG >= 0) and (CHI < 0):
            CAZ = 360
        else:
            CAZ = 180
    
        #Set QS if solar measurement available
        if ( self.Case1.SUN_TIME >= 24) or (self.Case1.SUN_TIME == 99):
            Q3 = self.Case1.SolarRadiation
    
        #5400 REM * CALCULATE SOLAR AZIMUTH IN DEGREES, Z4.DEG
        Z4_DEG = CAZ + np.arctan(CHI)
        Z4_RAD = Z4_DEG*DEG_TO_RAD
        Z1_RAD = self.Case1.Z1_DEG*DEG_TO_RAD
        E1 = np.cos(H3_RAD)*np.cos(Z4_RAD-Z1_RAD)
        E2_RAD = np.arctan(np.sqrt(1/(E1)**2 - 1))
        QS = (self.Cable1.ABSORP*Q3*np.sin(E2_RAD)*self.Cable1.D/1000*(1 \
            + 0.0001148*self.Case1.CDR_ELEV-1.108E-08*(self.Case1.CDR_ELEV)**2))
    
        if QS < 0:
            QS = 0.0
    
        self.Case1.QS = QS
        #print("Solar Radiation QS: ", self.Case1.QS, " W/m")
        return 
   #End Function ieee_738_2013_solar

    
    ########################################################################
    # Thermal coeficient of Rac & heatcap & wind correction
    #9000 REM //////////////////////////////////////////////////////////////
    #9010 REM / SUBROUTINE TO CALCULATE THERM COEF OF RAC & HEATCAP & WIND CORRECTION
    #9020 REM //////////////////////////////////////////////////////////////
    ########################################################################
    def thermal( self):
        """Compute thermal Coefficient of RAC, HeatCap and Wind Correction.
        
        """
        #9030 REM **********************************************************
        #9040 REM * SETUP LINEAR CONDUCTOR RESISTANCE EQ AS FUNCTION OF TEMP
        #9042 REM * B IN OHM/M-C AND B1 IN OHM/M
        #9050 REM **********************************************************
        self.Cable1.B =  (self.Cable1.RHI - self.Cable1.RLO)/(self.Cable1.THI - self.Cable1.TLO)
        self.Cable1.B1 = self.Cable1.RLO - self.Cable1.B*self.Cable1.TLO
    
        #9080 REM *****************************************************
        #9090 REM * SET UP LINEAR HEAT CAPACITY EQS AS FUNCTION OF TEMP
        #9100 REM *****************************************************
        #9110 REM ***************************************************
        #9120 REM * CORRECTION FACTOR (YC) FOR NON-PERPENDICULAR WIND
        #9130 REM ***************************************************
        PIANG = np.pi/180;
        self.Case1.WINDANG_RAD = 1.570796 - self.Case1.WINDANG_DEG * PIANG;
        self.Case1.YC = (1.194 - np.sin(self.Case1.WINDANG_RAD) - 0.194*np.cos(2.0*self.Case1.WINDANG_RAD) \
            + 0.368*np.sin(2.0*self.Case1.WINDANG_RAD))
        return     


        
    ########################################################################
    #
    #13000 REM ////////////////////////////////////////////////////////////////////
    #13010 REM / SUBROUTINE RTMI MUELLER-S ITERATION METHOD SELECTS A CURRENT /
    #13020 REM / WHICH JUST RAISES TCDR TO TCDMAX IN THE TIME TT. THIS CURRENT /
    #13030 REM / IS THE TRANSIENT RATING OF THE CONDUCTOR. IT DOES THIS BY /
    #13040 REM / REPEATEDLY GUESSING A CURRENT - XISTEP - CALCULATING TCDR AT TT /
    #13050 REM / AND COMPARING THE CALCULATED TCDR TO TCDRMAX. ROUTINE SUPPLIED /
    #13060 REM / COURTESY OF BILL HOWINGTON. /
    def mueller( self):
        """Function that implements an iteration method that selects a current which just raises self.Case1.TCDR to its maximum value in the time TT.
       
        """
   
        #13070 REM ///////////////////////////////////////////////////////////////////
        #13080 REM * START BY PREPARING TO ITERATE
        #13090 REM *******************************
        self.Case1.XLI = 0
        self.Case1.XRI = 0
        self.Case1.EPS = 0.049
        self.Case1.IEND = 20
        self.Case1.X = 0
        
        self.initial_bounds()
        
        self.Case1.IER = 0
        self.Case1.XL = self.Case1.XLI 
        self.Case1.XR = self.Case1.XRI  
        self.Case1.X = self.Case1.XLO
        self.Case1.TOL = self.Case1.X 
        
        self.find_TCDR()
       
        self.Case1.F = self.Case1.TEMP
        if (self.Case1.XLI == self.Case1.XRI) or (self.Case1.F == 0):
            return
        
        self.Case1.FL = self.Case1.F
        self.Case1.X = self.Case1.XR    
        self.Case1.TOL = self.Case1.X
       
        self.find_TCDR()
       
        self.Case1.F = self.Case1.TEMP
        if self.Case1.F == 0:
            return
       
        self.Case1.FR = self.Case1.F

        if (np.sign( self.Case1.FL) + np.sign( self.Case1.FR)) !=0:
            if self.Case1.XHI != self.Case1.XLO:
                self.Case1.IER = 2
                JK = 0
                print("Number of iterations= ", JK)
                print("ITERATION ROUTINE CONDITION CODE,IER= ", self.Case1.IER)
                if self.Case1.IER == 2:
                    print("TCDR OUT OF TEMPERATURE RANGE")
                elif self.Case1.IER == 1:
                    print("NO CONVERGENCE IN SUBROUTINE TRANS")
            
                sys.exit(0) #stop program
            else:
                return        

        #13190 REM ************************************************
        #13200 REM BASIC ASSUMPTION FL*FR LESS THAN 0 IS SATISFIED.
        #13210 REM ************************************************
        self.Case1.I = 0
 
        #13230 REM ********************
        #13240 REM START ITERATION LOOP
        #13250 REM ********************
        while (True):
            bfor = 0
            self.Case1.I = self.Case1.I + 1        
        
            #13270 REM ********************
            #13280 REM START BISECTION LOOP
            #13290 REM ********************
            JK=0 #initialize loop counter.
            while (JK <= (self.Case1.IEND -1)):            
                self.Case1.X  = 0.5 * (self.Case1.XL + self.Case1.XR)
                self.Case1.TOL = self.Case1.X 
                self.find_TCDR()

                self.Case1.F = self.Case1.TEMP 
    
                if self.Case1.F == 0 :
                    return

                if (np.sign( self.Case1.F ) + np.sign( self.Case1.FR )) == 0: 
                    #13340 REM ***************************************************************
                    #13350 REM INTERCHANGE XL AND XR IN ORDER TO GET THE SAME SIGN IN F AND FR
                    #13360 REM ***************************************************************
                    self.Case1.TOL = self.Case1.XL
                    self.Case1.XL = self.Case1.XR
                    self.Case1.XR = self.Case1.TOL
                    self.Case1.TOL = self.Case1.FL
                    self.Case1.FL = self.Case1.FR
                    self.Case1.FR = self.Case1.TOL
           
           
                self.Case1.TOL = self.Case1.F - self.Case1.FL
                self.Case1.DA = self.Case1.F * self.Case1.TOL
                self.Case1.DA = self.Case1.DA + self.Case1.DA 

                if ( self.Case1.DA - self.Case1.FR * (self.Case1.FR - self.Case1.FL)) >= 0:
                    pass
                else:
                    if (self.Case1.I - self.Case1.IEND) <= 0:
                        bfor = 1
                        break

                self.Case1.XR = self.Case1.X
                self.Case1.FR = self.Case1.F
    
                #13420 REM ***********************************************
                #13430 REM TEST ON SATISFACTORY ACCURACY IN BISECTION LOOP
                #13440 REM ***********************************************
                self.Case1.TOL = self.Case1.EPS
        
                if (np.abs( self.Case1.FR - self.Case1.FL) - self.Case1.TOL) <= 0:
                    return 
                JK=JK+1

            #JK starts at 0 so the value of JK after increasing the counter is the number of
            #finished cicles
    
            if bfor == 0:
                #13480 REM *****************************************************************
                #13490 REM END OF BISECTION LOOP - NO CONVERGENCE AFTER IEND ITERATION STEPS
                #13500 REM FOLLOWED BY IEND SUCCESSIVE STEPS OF BISECTION
                #13510 REM *****************************************************************
                self.Case1.IER =1
                
                print("Number of iterations= ", JK)
                print("ITERATION ROUTINE CONDITION CODE,IER= ", self.Case1.IER)
                if self.Case1.IER == 2:
                    print("TCDR OUT OF TEMPERATURE RANGE")
                elif self.Case1.IER == 1:
                    print("NO CONVERGENCE IN SUBROUTINE TRANS")
            
                sys.exit(0) #stop program

            #13540 REM ******************************************************************
            #13550 REM COMPUTATION OF ITERATED X-VALUE BY INVERSE PARABOLIC INTERPOLATION
            #13560 REM ******************************************************************
            self.Case1.DA = self.Case1.FR - self.Case1.F
            self.Case1.DX = ((self.Case1.X - self.Case1.XL) * self.Case1.FL * (1 + self.Case1.F * (self.Case1.DA - self.Case1.TOL) 
                                                                               / (self.Case1.DA * (self.Case1.FR - self.Case1.FL))) / self.Case1.TOL)
            self.Case1.XM = self.Case1.X
            self.Case1.FM = self.Case1.F
            self.Case1.X = self.Case1.XL - self.Case1.DX
            self.Case1.TOL = self.Case1.X
            
            self.find_TCDR()
            
            self.Case1.F = self.Case1.TEMP
    
            if self.Case1.F == 0:
                return 
    
            #13610 REM ***********************************************
            #13620 REM TEST ON SATISFACTORY ACCURACY IN ITERATION LOOP
            #13630 REM ***********************************************
            self.Case1.TOL = self.Case1.EPS
            if (abs( self.Case1.F) - self.Case1.TOL) <= 0:
                return

            #13660 REM **********************************
            #13670 REM PREPARATION OF NEXT BISECTION LOOP
            #13680 REM **********************************
            if (np.sign( self.Case1.F) + np.sign( self.Case1.FL)) == 0:
                self.Case1.XR = self.Case1.X
                self.Case1.FR = self.Case1.F
            else:
                self.Case1.XL = self.Case1.X
                self.Case1.FL  = self.Case1.F
                self.Case1.XR = self.Case1.XM
                self.Case1.FR = self.Case1.FM
        
           #13720 REM ****************************************
            #13730 REM END OF ITERATION LOOP
        
        return


    
    ########################################################################
    #14000 REM ////////////////////////////////////////////////////////////
    #14010 REM / SUBROUTINE GUESS TO DETERMINE INITIAL BOUNDS FOR ITERATION
    #14020 REM ////////////////////////////////////////////////////////////
    ########################################################################
    def initial_bounds( self):
        """Computes initial bounds for iteration.
        """
        if self.Case1.NFLAG == 0:
            self.Case1.XLO = self.Case1.TAMB
            self.Case1.XHI = 1000
            self.Case1.DIV = 10
        elif self.Case1.NFLAG == 1:
            self.Case1.XLO = 0
            self.Case1.XHI = 10*self.Case1.AT
            self.Case1.DIV = 10        
    
        self.Case1.CHA = (self.Case1.XHI - self.Case1.XLO) / self.Case1.DIV
        self.Case1.NUM = np.floor( self.Case1.DIV)
        self.Case1.X = self.Case1.XLO
        
        self.find_TCDR()

        self.Case1.FO = self.Case1.TEMP
    
        JK=0
        while (JK <=( self.Case1.NUM - 1)):
            self.Case1.X = self.Case1.XLO + (JK+1) * self.Case1.CHA
            self.find_TCDR()
        
            self.Case1.FF = self.Case1.TEMP
        
            if (np.sign( self.Case1.FF) + np.sign( self.Case1.FO)) == 0:
                self.Case1.XRI = self.Case1.X
                self.Case1.XLI = self.Case1.X - self.Case1.CHA
                return 
        
            self.Case1.FO = self.Case1.FF
            JK=JK+1
    
    
        self.Case1.XLI  = self.Case1.XLO
        self.Case1.XRI = self.Case1.XHI
        return 
            


    #12000 REM ////////////////////////////////////////////////////
    #12010 REM / SUBROUTINE ITERATES TO FIND CONDUCTOR TEMPERATURE
    #12020 REM / GIVEN THE CONDUCTOR CURRENT
    #12030 REM ////////////////////////////////////////////////////
    def find_TCDR( self):
        """Obtain conductor temperature given the conductor current.
        
        :return: The computed value is returned in 
            self.Case1.TEMP (float): Conductor temperature in [DEG C].
        """
        if self.Case1.NFLAG == 0:
            self.Case1.TCDR = self.Case1.X
            self.thermal_rating()
            self.Case1.TEMP = self.Case1.XIDUMMY - self.Case1.TR
            return 
        elif self.Case1.NFLAG == 1:
            self.Case1.XISTEP = self.Case1.X
            self.TCDR_vs_TIME()
    
        if self.Case1.TCDRPRELOAD <= self.Cable1.TCDRMAX: 
            self.Case1.TEMP = self.Cable1.TCDRMAX - self.Case1.TCDR
        else:
            self.Case1.TEMP = self.Case1.TCDR - self.Cable1.TCDRMAX
        return 


    #15000 REM /////////////////////////////////////////////////////////////////
    #15010 REM / SUBROUTINE T0 CALCULATE THERMAL RATING GIVEN A CDR TEMP (TCDR),
    #15020 REM / AND CONDUCTOR PARAMETERS AND WEATHER CONDITIONS
    #15030 REM /////////////////////////////////////////////////////////////////
    #15040 REM PRINT USING "TRYING A TCDR OF ####.### DEG C"; TCDR
    def thermal_rating( self):
        """Computes the thermal rating of the cable given a conductor temperature.
        
        :Args:
            self.Case1.TCDR (float): conductor temperature [DEG C].
            
        :return:
            self.Case1.TR (float): ampacity [A]
                
        
        """ 
        #print('thermal_rating()')
        #15050 REM *********************************************************
        #15060 REM * CALC CONDUCTOR HEAT LOSS (QR) BY RADIATION (WATTS/M)
        #15070 REM *********************************************************
        self.Case1.T3 = self.Case1.TCDR + 273
        self.Case1.T4 = self.Case1.TAMB + 273
        self.Case1.QR = 0.0178 * self.Cable1.EMISS * self.Cable1.D * ((self.Case1.T3 / 100)**4 - (self.Case1.T4 / 100)**4)
        
        #print("Radiation QR: ", self.Case1.QR, " W/m")
    
        #15110 REM ******************************************************************
        #15120 REM * CALC CONDUCTOR HEAT LOSS BY CONVECTION (WATTS/M)
        #15125 REM * NOTE CONVECTION EQUATIONS FORM IS DIFFERENT THAN IN BODY OF 738
        #15128 REM * BUT THE RESULTS OF CALCULATION ARE THE SAME
        #15130 REM ******************************************************************
        self.Case1.T5 = (self.Case1.TCDR + self.Case1.TAMB) / 2
        self.Case1.U1 = 1.458E-06 * (self.Case1.T5 + 273)**1.5 / (self.Case1.T5 + 383.4)
        self.Case1.P1 = ((1.2932 - 0.0001525 * self.Case1.CDR_ELEV + 6.379E-09 * self.Case1.CDR_ELEV**2) 
                      / (1 + 0.00367 * self.Case1.T5))
        self.Case1.K1 = 0.02424 + 7.477E-05 * self.Case1.T5 - 4.407E-09 * self.Case1.T5**2
 
        #15182 REM ******************************************************************
        #15184 REM * CALC CONDUCTOR HEAT LOSS (QC) BY NATURAL CONVECTION (WATTS/M)
        #15186 REM ******************************************************************
        if (self.Case1.TCDR - self.Case1.TAMB) < 0:
            self.Case1.TCDR = self.Case1.TAMB + 0.1
    
        self.Case1.QC = 0.0205*(self.Case1.P1**0.5)*(self.Cable1.D**0.75)*( self.Case1.TCDR - self.Case1.TAMB)**1.25
    
        if self.Case1.VWIND != 0:
            #15194 REM *****************************************************************
            #15196 REM * CALC CONDUCTOR HEAT LOSS (QCF) BY FORCED CONVECTION (WATTS/M)
            #15198 REM *****************************************************************
            self.Cable1.Z = self.Cable1.D * self.Case1.P1 * self.Case1.VWIND / self.Case1.U1
            self.Case1.Q1 = 0.0119 * (self.Cable1.Z**0.6) * self.Case1.K1 * (self.Case1.TCDR - self.Case1.TAMB)
            self.Case1.Q2 = (1.01 + 0.0372 * (self.Cable1.Z**0.52)) * self.Case1.K1 * (self.Case1.TCDR - self.Case1.TAMB)
    
            if ( self.Case1.Q1 - self.Case1.Q2) > 0:
                self.Case1.QCF = self.Case1.Q1
            else:
                self.Case1.QCF = self.Case1.Q2
       
            self.Case1.QCF = self.Case1.QCF * self.Case1.YC
    
            #15370 REM ***********************************************************
            #15380 REM * SELECT LARGER OF CONVECTIVE HEAT LOSSES (QC VERSUS QCF)
            #15390 REM ***********************************************************
            if self.Case1.QCF >= self.Case1.QC: 
                self.Case1.QC = self.Case1.QCF
                
            #15420 REM ***************************************
            #15430 REM * CALC SUM OF STEADY STATE HEAT FLOWS
            #15440 REM ***************************************
            self.Case1.R5 = -self.Case1.QS + self.Case1.QC + self.Case1.QR
    
            #15460 REM ************************************************
            #15470 REM * CALC SQRT OF CONDUCTOR RESISTANCE IN OHMS/M
            #15480 REM ************************************************
            self.Case1.W4 = np.sqrt( self.Cable1.B1 + self.Cable1.B * self.Case1.TCDR)
    
            if self.Case1.R5 <= 0: 
                self.Case1.TR = 0
                return 
            else:
                self.Cable1.R4 = self.Case1.R5**0.5
                #15520 REM **************************************************
                #15530 REM * CALCULATE THERMAL RATING (AMPACITY) IN AMPERES
                #15540 REM **************************************************
                self.Case1.TR = self.Cable1.R4 / self.Case1.W4
        
        #print("QC: ", self.Case1.QC, " W/m")
        return
        
    #11000 REM ///////////////////////////////////////////////////////////
    #11010 REM / SUBROUTINE CALCS CDR TEMP VS TIME FOR STEP CHANGE CURRENT
    #11020 REM ///////////////////////////////////////////////////////////
    def  TCDR_vs_TIME( self):
        """Computes the transient evolution of conductor temperature.

        """
        
        if self.Case1.NSELECT == 4:
            #print("Trying a current of ", data['XISTEP'], " Amps")
            pass
    
        self.Cable1.FLAG = 0
    
        bflag1 = 1
        bflag2 = 1
        while(bflag1):
            #print("bflag1")
            self.Case1.ATCDR[0] = self.Case1.TCDRPRELOAD
            self.Case1.TCDR = self.Case1.ATCDR[0]
            self.thermal_rating()
                
            self.Case1.K = 1
            salto = 0
            
            while(bflag2):
                #print("bflag2")     
                self.Case1.ATCDR.insert( self.Case1.K,(self.Case1.TCDR + (self.Case1.W4**2 * self.Case1.XISTEP**2 
                    + self.Case1.QS - self.Case1.QR - self.Case1.QC) * self.Case1.DELTIME / self.Cable1.HEATCAP))
                self.Case1.TIME.insert( self.Case1.K, (self.Case1.TIME[(self.Case1.K-1)] + self.Case1.DELTIME))
                self.Case1.TCDR = self.Case1.ATCDR[ self.Case1.K]
    
                #11115 IF NSELECT = 4 GOTO 11130
                if self.Case1.NSELECT != 4:
                    #11120 PRINT "TIME = "; TIME(K + 1) " SECONDS / "; "CDR TEMP = "; TCDR; "DEG C"
                    #print("Time = ", self.Case1.TIME[ self.Case1.K], "  seconds / CDR TEMP = ", self.Case1.TCDR, " DEG C")
                    pass
    
                #11130 IF NSELECT = 3 AND TCDR > TCDRMAX THEN 11280
                salto = 0
                if ( self.Case1.NSELECT == 3) and ( self.Case1.TCDR > self.Cable1.TCDRMAX):
                    salto = 1
                    break

                #11140 REM ********************************************************************
                #11150 REM *
                #11160 REM ********************************************************************
                self.thermal_rating()
                self.Case1.K = self.Case1.K + 1
        
                #11190 IF K = 3000 THEN PRINT "TIME INTERVAL TOO SMALL. ARRAY OUT OF
                #BOUNDS ": GOTO 1880
                if self.Case1.K == 3000:
                    print("TIME INTERVAL TOO SMALL. ARRAY OUT OF BOUNDS")
                    sys.exit(0)
            
                #11200 IF TIME(K) < TT THEN 11090
                if self.Case1.TIME[( self.Case1.K - 1)] >= self.Case1.TT:
                    #print("11200: time > tt")
                    break
       
            if salto == 0:
                #11210 IF XISTEP = 0 AND TCDR > TCDRMAX THEN 11220 ELSE 11250
                if ( self.Case1.XISTEP == 0) and ( self.Case1.TCDR > self.Cable1.TCDRMAX):
                    #11220 PRINT "EVEN IF THE CURRENT IS REDUCED TO ZERO AMPS, THE CONDUCTOR"
                    print("Even if the current is reduced to zero amps, the conductor")
                    #11230 PRINT USING "TEMPERATURE WILL NOT DECREASE TO ####.# DEG C IN ####.#
                    print("temperature will no decrease to ", self.Cable1.TCDRMAX, " in ", self.Cable1TT/60, " minutes")
                    #MINUTES"; TCDRMAX; TT / 60
                    #11240 GOTO 1880
                    sys.exit(0)
        
            #11250 REM **********************************
            #11260 REM * CHECK FOR SHORT DURATION FAULTS
            #11270 REM **********************************
            if ( self.Case1.TIME[self.Case1.K - 1] >= 60) or ( self.Cable1.FLAG == 1) or ( self.Cable1.HEATCORE == 0) or (self.Case1.TT < 60):
                break
        
                self.Cable1.HEATCAP = self.Cable1.HEATOUT
                self.Cable1.FLAG = 1
                #11310 GOTO 11050
                
    
    
        self.Case1.KTIMEMAX = self.Case1.K
        return

    #10000 REM ///////////////////////////////////////////////////////////////
    #10010 REM / SUBROUTINE TO CALCULATE STARTING VALUE FOR CURRENT ITERATION
    #10020 REM / BY ASSUMING ADIABATIC HEATING DURING TIME TT
    #10030 REM ///////////////////////////////////////////////////////////////
    #10040 TCDR = (TCDRMAX + TAMB) / 2
    def starting_ci( self):
        """Compute the starting value for current iteration by assuming adiabatic heating during transient.
        
        """
  
        self.Case1.TCDR = (self.Cable1.TCDRMAX + self.Case1.TAMB) / 2
    
        #10050 IF TT < 60 THEN HEATCAP = HEATOUT ELSE HEATCAP = HEATOUT + HEATCORE
        if self.Case1.TT < 60:
            self.Cable1.HEATCAP = self.Cable1.HEATOUT
        else:
            self.Cable1.HEATCAP = self.Cable1.HEATOUT + self.Cable1.HEATCORE
    
        #10060 GOSUB 15000
        self.thermal_rating()
    
        #10070 AT = SQR(HEATCAP * (TCDRMAX - TAMB) / TT) / W4
        self.Case1.AT = np.sqrt( self.Cable1.HEATCAP * (self.Cable1.TCDRMAX - self.Case1.TAMB) / self.Case1.TT) / self.Case1.W4
    
        #10080 TCDR = TCDRPRELOAD
        self.Case1.TCDR = self.Case1.TCDRPRELOAD
    
        #10090 NFLAG = 1
        self.Case1.NFLAG = 1
    
        #10100 GOSUB 13000
        self.mueller()
    
        #10110 RETURN
        return
  
  
    def output( self):
        """Print detailed results.
        
        """
        #6070 PRINT
        #6080 PRINT X$
        print("*******************************************************************")
        print("*******************************************************************")
        #6090 PRINT " IEEE STD 738-2006 METHOD OF CALCULATION"
        print("IEEE STD 738-2013 METHOD OF CALCULATION")
        #6100 PRINT
        print("*******************************************************************")
        
        print("NSELECT = ", self.Case1.NSELECT)
        if self.Case1.NSELECT == 1:
            print("Steady-state conductor Temperature Calculation (SI units)")
            print('Given the constant current the function computes the conductor')
            print('temperature')
            print("*******************************************************************")
        elif self.Case1.NSELECT == 2:
            print("Steady-state conductor Thermal Rating Calculation (SI units)")
            print('Given a maximum conductor temperature the function computes')
            print('the steady state thermal rating in amps')
            print("*******************************************************************")
    
        print("The conductor is a ", self.Cable1.Cstring)
    
        #6110 PRINT "AIR TEMPERATURE = "; TAMB; " DEG C &";
        print("Air temperature = ", self.Case1.TAMB," ºC")
    
        #6130 PRINT "WIND SPEED IS "; VWIND; " M / SEC"
        print("Wind speed = ", self.Case1.VWIND," m/s")
    
        #6140 PRINT USING "THE ANGLE BETWEEN WIND AND CONDUCTOR IS ### DEG"; WINDANG.DEG
        print("The angle between wind and conductor is = ", self.Case1.WINDANG_DEG, " DEG")
    
        #6150 PRINT USING "THE CONDUCTOR IS #####. M ABOVE SEA LEVEL;"; CDR.ELEV
        print("The conductor is = ", self.Case1.CDR_ELEV, " m above sea level")
    
        #6160 PRINT USING "AND ###.# DEG FROM NORTH; AT A LATITUDE OF ###.# DEG"; Z1.DEG; CDR.LAT
        print( self.Case1.Z1_DEG, " DEG from North; at a latitude of ", self.Case1.CDR_LAT_DEG," DEG")
    
        #6170 PRINT "THE SUN TIME IS "; SUN.TIME; "HOURS &"; " THE ATMOSPHERE IS "; B$
        print("The sun time is = ", self.Case1.SUN_TIME, " hours & The atmosphere is ", self.Case1.Bstring)
    
        #6180 PRINT
        #6240 PRINT "CONDUCTOR DIAMETER IS "; D; " MM"
        print("The conductor diameter is = ", self.Cable1.D, " mm")
            
        #6250 PRINT USING "CONDUCTOR RESISTANCE IS ##.#### OHMS/KM AT #### DEG C"; RLO * 1000; TLO
        print("The conductor resistance is = ", self.Cable1.RLO*1000," ohms/km at ", self.Cable1.TLO," ºC")
    
        #6260 PRINT USING " AND ##.#### OHMS/KM AT #### DEG C"; RHI * 1000; THI
        print("and ", self.Cable1.RHI*1000," ohms/km at ", self.Cable1.THI," ºC")
    
        #6270 PRINT "COEF OF EMISSIVITY = "; EMISS; " & COEF OF ABSORPTIVITY = "; ABSORP
        print("The Coef. of emissivity is = ", self.Cable1.EMISS," & Coef. of absorptivity is = ", self.Cable1.ABSORP)
    
        #6280 IF NSELECT = 3 OR NSELECT = 4 GOTO 6490
        #6290 PRINT
        #6350 PRINT USING "SOLAR HEAT INPUT IS ####.### WATTS PER CONDUCTOR METER"; QS
        print("Solar Heat input is = ", self.Case1.QS," W/m")
    
        #6360 PRINT USING "RADIATION COOLING IS ####.### WATTS PER CONDUCTOR METER"; QR
        print("Radiation cooling is = ", self.Case1.QR," W/m")
    
        #6370 PRINT USING "CONVECTIVE COOLING IS ####.### WATTS PER CONDUCTOR METER"; QC
        print("Convective cooling is = ", self.Case1.QC," W/m")
    
        #6380 PRINT
        #6390 IF NSELECT = 1 THEN GOTO 6440
    
        #6420 GOSUB 7000
        #6430 RETURN
        #6440 IF XIPRELOAD = 1.111 THEN XIPRELOAD = 0
    
        if self.Case1.NSELECT == 1:
            #6450 PRINT USING "GIVEN A CONSTANT CURRENT OF #####.# AMPERES,"; XIPRELOAD
            print("Given a constant current of = ", self.Case1.XIPRELOAD," A")
    
            #6460 PRINT USING "THE CONDUCTOR TEMPERATURE IS ####.# DEG C"; TCDRPRELOAD
            print("The conductor temperature is = ", self.Case1.TCDRPRELOAD," ºC")
            
        elif self.Case1.NSELECT == 2:
            #6400 PRINT USING "GIVEN A MAXIMUM CONDUCTOR TEMPERATURE OF #####.# DEG C,"; TCDRPRELOAD
            print("Given a maximum conductor temperature of = ", self.Case1.TCDRPRELOAD," ºC")    
            #6410 PRINT USING "THE STEADY STATE THERMAL RATING IS ######.# AMPERES"; TR
            print("The steady-state thermal rating is = ", self.Case1.TR," Amperes")    
            
        elif self.Case1.NSELECT == 3:
            #6500 PRINT " ******* TRANSIENT THERMAL CALCULATIONS *******"
            print("******* TRANSIENT THERMAL CALCULATIONS *******")
    
            #6510 PRINT USING "INITIAL STEADY STATE CONDUCTOR TEMP = ###.# DEG C"; TCDRPRELOAD
            print("Initial steady-state conductor temp is = ", self.Case1.TCDRPRELOAD," ºC")    
        
            #6520 IF IORTPRELOAD = 1 THEN PRINT USING "FOR A PRE-STEP STEADY STATE CURRENT = #####.# AMPERES"; XIPRELOAD
            if self.Case1.IORTPRELOAD == 1:
                print("for a PRE-STEP steady-state current = ", self.Case1.XIPRELOAD," Amperes")    
        
        
            #6530 IF HNH = 2 THEN GOTO 6610
            if self.Cable1.HNH == 1:
                #6550 PRINT USING " HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATCAP
                print("Heat capacity = ", self.Cable1.HEATCAP," W.s/mºC")    
            elif self.Cable1.HNH == 2:
                #6610 PRINT USING " CORE HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATCORE
                print("Core heat capacity = ", self.Cable1.HEATCORE," W.s/m.ºC")    
                #6620 PRINT USING " OUTER STRAND LAYERS HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATOUT
                print("Outer strand layers heat capacity = ", self.Cable1.HEATOUT," W.s/m.ºC")    
        
    
            #6640 PRINT "THE TOTAL TIME OF INTEREST AFTER THE CURRENT"
            print("The total time of interest after the current ")    
        
            #6650 IF SORM = 0 THEN PRINT USING "INCREASES TO #######.# AMPS = ####.#### SECONDS"; XISTEP; TT
            #6660 IF SORM = 1 THEN PRINT USING "INCREASES TO #######.# AMPS = ####.#### MINUTES"; XISTEP; TT / 60
            if self.Case1.SORM == 0:
                print("increases to ", self.Case1.XISTEP," A .-. ", self.Case1.TT," secs")    
            elif self.Case1.SORM == 1:
                print("increases to ", self.Case1.XISTEP," A .-. ", self.Case1.TT/60," min")    
        
            #6670 PRINT USING "CALCULATION TIME INTERVAL = ###.#### SECONDS"; DELTIME
            print("calculation time interval = ", self.Case1.DELTIME," s")    
      
            if ((self.Case1.ATCDR[1] - self.Case1.TAMB) / (self.Case1.ATCDR[( self.Case1.KTIMEMAX-1)] - self.Case1.TAMB)) >= 0.05:
                #6680 IF ((ATCDR(2) - TAMB) / (ATCDR(KTIMEMAX) - TAMB)) < .05 THEN GOTO 6710
                #6690 PRINT " CALCULATION ACCURACY WOULD IMPROVE IF THIS TIME INTERVAL WERE REDUCED "
                print("CALCULATION ACCURACY WOULD IMPROVE IF THIS TIME INTERVAL WERE REDUCED ")
        
            #6710 IF FLAG = 0 OR HEATCORE = 0 THEN 6730
            if self.Cable1.FLAG == 0 or self.Cable1.HEATCORE == 0:
                pass
            else:
                #6720 PRINT "CORE HEAT CAPACITY IS IGNORED SINCE STEP DURATION LESS THAN 60 SEC"
                print("CORE HEAT CAPACITY IS IGNORED SINCE STEP DURATION LESS THAN 60 SEC")
    
            if self.Case1.NSELECT == 4: #6730 IF NSELECT = 4 GOTO 6870
                pass
            else:
                #6740 IF ATCDR(KTIMEMAX) < TCDRMAX THEN GOTO 6780
                if self.Case1.ATCDR[( self.Case1.KTIMEMAX-1)] >= self.Cable1.TCDRMAX:
                    #6750 PRINT USING "IT TAKES ####.#### SEC (####.#### MIN) "; TIME(KTIMEMAX) TIME(KTIMEMAX) / 60!
                    print("it takes ", self.Case1.TIME[( self.Cable1KTIMEMAX-1)]," seconds (", self.Case1.TIME[( self.Case1.KTIMEMAX-1)]/60," minutes)")            
                    #6760 PRINT "TO REACH THE MAXIMUM ALLOWABLE CONDUCTOR TEMPERATURE "
                    print("TO REACH THE MAXIMUM ALLOWABLE CONDUCTOR TEMPERATURE")    
                    #6770 PRINT USING "OF ####.# DEGREES C"; TCDRMAX
                    print("of ", self.Cable1.TCDRMAX," DEG C")    
            
                K=0
                while(K<=( self.Case1.KTIMEMAX-1)):
                    #6790 FOR K = 1 TO KTIMEMAX
                    #6800 IF SORM = 0 THEN PRINT USING "TIME=#####.#### SEC CDRTEMP= ####.# DEG C"; TIME(K) ATCDR(K)
                    #6810 IF SORM = 1 THEN PRINT USING "TIME=#####.#### MIN CDRTEMP= ####.# DEG C"; TIME(K) / 60; ATCDR(K)
                    if self.Case1.SORM == 0:
                        print("time = ", self.Case1.TIME[K]," sec / CDRTEMP = ", self.Case1.ATCDR[K]," ºC")            
                    elif self.Case1.SORM == 1:
                        print("time = ", self.Case1.TIME[K]/60," min / CDRTEMP = ", self.Case1.ATCDR[K]," ºC")                        
                    K=K+1
                    #6820 IF K <> 20 AND K <> 40 AND K <> 60 AND K <> 80 THEN GOTO 6840
                    #6840 NEXT K
            
            #6850 IF KTIMEMAX < 20 THEN GOSUB 7000
            #6860 RETURN
               
        elif self.Case1.NSELECT == 4: #6630 IF NSELECT = 4 THEN 6670        
    
            #6500 PRINT " ******* TRANSIENT THERMAL CALCULATIONS *******"
            print("******* TRANSIENT THERMAL CALCULATIONS *******")
    
            #6510 PRINT USING "INITIAL STEADY STATE CONDUCTOR TEMP = ###.# DEG C"; TCDRPRELOAD
            print("Initial steady-state conductor temp is = ", self.Case1.TCDRPRELOAD," ºC")    
        
            #6520 IF IORTPRELOAD = 1 THEN PRINT USING "FOR A PRE-STEP STEADY STATE CURRENT = #####.# AMPERES"; XIPRELOAD
            if self.Case1.IORTPRELOAD == 1:
                print("for a PRE-STEP steady-state current = ", self.Case1.XIPRELOAD," Amperes")    
            else:
                pass
            
            #6530 IF HNH = 2 THEN GOTO 6610
            if self.Cable1.HNH == 1:
                #6550 PRINT USING " HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATCAP
                print("Heat capacity = ", self.Cable1.HEATCAP," W.s/mºC")    
            elif self.Cable1.HNH == 2:
                #6610 PRINT USING " CORE HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATCORE
                print("Core heat capacity = ", self.Cable1.HEATCORE," W.s/mºC")    
                #6620 PRINT USING " OUTER STRAND LAYERS HEAT CAPACITY = ####.# WATTS-SEC/M-C"; HEATOUT
                print("Outer strand layers heat capacity = ", self.Cable1.HEATOUT," W.s/mºC")    
            
            #6670 PRINT USING "CALCULATION TIME INTERVAL = ###.#### SECONDS"; DELTIME
            print("Calculation time interval = ", self.Case1.DELTIME," seconds")    
            
            #6680 IF ((ATCDR(2) - TAMB) / (ATCDR(KTIMEMAX) - TAMB)) < .05 THEN GOTO 6710
            if (( self.Case1.ATCDR[1] - self.Case1.TAMB) / ( self.Case1.ATCDR[( self.Case1.KTIMEMAX - 1)] - self.Case1.TAMB)) >= 0.05:
                #6690 PRINT " CALCULATION ACCURACY WOULD IMPROVE IF THIS TIME INTERVAL WERE REDUCED "
                print("Calculation accuracy would improve if this time interval were reduced")
            
            #6710 IF FLAG = 0 OR HEATCORE = 0 THEN 6730
            if (( self.Cable1.FLAG != 0) and ( self.Cable1.HEATCORE != 0)):
                #6720 PRINT "CORE HEAT CAPACITY IS IGNORED SINCE STEP DURATION LESS THAN 60 SEC"        
                print("Core heat capacity is ignored since step duration less than 60 sec")
            
            
            #6870 PRINT USING "THE TRANSIENT THERMAL RATING = ########.# AMPERES"; XISTEP
            print("the transient thermal rating = ", self.Case1.XISTEP," A")    
        
            #6880 PRINT "THAT IS, WITH THIS CURRENT, THE CDR TEMPERATURE JUST REACHES "
            print("that is, with this current, the CDR temperature just reaches")    
    
            #6890 IF TT > 60 THEN PRINT USING "THE MAXIMUM OF ####.# DEG C IN ##.#### MINUTES"; TCDRMAX; TT / 60!
            #6900 IF TT <= 60 THEN PRINT USING "THE MAXIMUM OF ####.# DEG C IN ###.#### SECONDS"; TCDRMAX; TT 
            if self.Case1.TT > 60:
                print("the maximum of = ", self.Cable1.TCDRMAX," ºC in ", self.Case1.TT/60," minutes")    
            else:
                print("the maximum of = ", self.Cable1.TCDRMAX," ºC in ", self.Case1.TT," seconds")            



        print("*******************************************************************")
        print("*******************************************************************")

        return 


    def str_round( self, valuex):
        """Obtain the rounded value of <valuex> acording the variable <self.Debug_Dec>.

        :Args:
            valuex (float): value to be rounded according the number of decimal values defined by <self.Debug_Dec>.
        
        """
        return str( round( valuex, self.Debug_Dec))

    def outputs( self):
        """Print a summary of intermediate results.
            
        """
        print("*******************************************************************")
        print("*******************************************************************")
        print("IEEE 738")
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



    def ampacidad( self):
        """Not yet implemented.
    
        """      
        #Analysis choice (variable data['NSELECT'])
        #1.- CALCULATE THE STEADY STATE CONDUCTOR TEMPERATURE (TCDRPRELOAD) 
        #CORRESPONDING TO THE GIVEN STEADY STATE CURRENT (XIPRELOAD)
        
        #2.- CALCULATE THE STEADY STATE CURRENT (TR) GIVEN THE STEADY STATE 
        #CONDUCTOR TEMPERATURE (TCDR)
    
        #3.- TRANSIENT CONDUCTOR TEMPERATURE CALCULATION
        #    PRE AND POST CURRENT VALUES MUST BE DEFINED
        #    Mode 3 requires IORTPRELOAD=1
    
        #4.- TRANSIENT CONDUCTOR THERMAL RATING CALCULATION
        #    PRE AND POST TEMPERATURE VALUES MUST BE DEFINED
        #    Mode 4 requires IORTPRELOAD=2
        #    EL MODO 4 REQUIERE UN 2 para que NFLAG cambie a 1. El valor original de IORTPRELOAD es 1
    
        
    
    
    def print_ver( self):
        """Print current version.
        """
        
        print("IEEE738. 30/3/2023. 23:15") 