# -*- coding: utf-8 -*-
import numpy as np
from cable import cable
from importlib import reload
reload(  cable)


class Case():
    """Case"""
    
    def __init__(self):
        pass
    

class IEEE738():
    """Implementation of the IEEE 738:2012."""
    
    
    def __init__(self):
        self.C1 = cable.Cable()
      
    
    def set_cable( self, Cable):
        self.C1 = Cable
    
    ########################################################################
    # Conductor solar heat gain (QS)
    # 5000 REM /////////////////////////////////////////////////////////
    # 5010 REM / SUBROUTINE TO CALCULATE CONDUCTOR SOLAR HEAT GAIN (QS)
    # 5020 REM /////////////////////////////////////////////////////////
    ########################################################################
    def solar( self):
        """
        Compute the conductor solar heat gain (QS)
        
        :return: Value of solar heat gain QS in W/m^2
        """
        data['DEG_TO_RAD'] = np.pi/180
        data['CDR_LAT_RAD'] = data['CDR_LAT_DEG']*data['DEG_TO_RAD']
    
        #5060 REM * SOLAR DECLINATION
        data['DECL_DEG'] = 23.4583*np.sin(((284 + data['NDAY'])/365)*2*np.pi)
        data['DECL_RAD'] = data['DECL_DEG']*data['DEG_TO_RAD']
    
        #5090 REM * SOLAR ANGLE RELATIVE TO NOON
        data['HOUR_ANG_DEG'] = (data['SUN_TIME']-12)*15
        data['HOUR_ANG_RAD'] = data['HOUR_ANG_DEG']*data['DEG_TO_RAD']
    
        #5120 REM * FIND SOLAR ALTITUDE - H3
        data['H3ARG'] = (np.cos(data['CDR_LAT_RAD'])*np.cos(data['DECL_RAD'])*np.cos(data['HOUR_ANG_RAD'])
        +np.sin(data['CDR_LAT_RAD'])*np.sin(data['DECL_RAD']))
        data['H3_RAD'] = np.arctan(data['H3ARG']/np.sqrt(1-data['H3ARG']**2))
        data['H3_DEG'] = data['H3_RAD']/data['DEG_TO_RAD']
   
        if data['A3'] == 1:
        #5260 REM *****************************************************************
        #5270 REM * SOLAR HEAT (Q3) AT EARTH SURFACE (W/M2) IN INDUSTRIAL AIR (P6)
        #5280 REM *****************************************************************
            data['Q3'] = 53.1821 + 14.211*data['H3_DEG'] + 0.66138*data['H3_DEG']**2
            data['Q3'] = data['Q3'] - 0.031658*data['H3_DEG']**3 + 5.4654E-04*data['H3_DEG']**4
            data['Q3'] = data['Q3'] - 4.3446E-06*data['H3_DEG']**5 + 1.3236E-08*data['H3_DEG']**6
            data['Bstring'] = 'INDUSTRIAL'
        elif data['A3'] == 0:
        #5180 REM ***************************************************************
        #5190 REM * SOLAR HEATING (Q3) AT EARTH SURFACE (W/M2) IN CLEAR AIR (P6)
        #5200 REM ***************************************************************
            data['Q3'] = -42.2391 + 63.8044*data['H3_DEG'] - 1.922*data['H3_DEG']**2
            data['Q3'] = data['Q3'] + 0.034692*data['H3_DEG']**3 - 3.6112E-04*data['H3_DEG']**4
            data['Q3'] = data['Q3'] + 1.9432E-06*data['H3_DEG']**5 - 4.0761E-09*data['H3_DEG']**6
            data['Bstring'] = 'CLEAR'
    
         #5330 REM * CALCULATE SOLAR AZIMUTH VARIABLE, CHI
        data['CHI_DENOM'] = (np.sin(data['CDR_LAT_RAD'])*np.cos(data['HOUR_ANG_RAD']) 
            - np.cos(data['CDR_LAT_RAD'])*np.tan(data['DECL_RAD']))
        data['CHI'] = np.sin(data['HOUR_ANG_RAD'])/data['CHI_DENOM']
    
        #5360 REM * CALCULATE SOLAR AZIMUTH CONSTANT, CAZ
        if (data['HOUR_ANG_DEG'] < 0) and (data['CHI >= 0']):
            data['CAZ'] = 0
        elif (data['HOUR_ANG_DEG'] >= 0) and (data['CHI'] < 0):
            data['CAZ'] = 360
        else:
            data['CAZ'] = 180
    
        #Set QS if solar measurement available
        if (data['SUN_TIME'] >= 24) or (data['SUN_TIME'] == 99):
            data['Q3'] = data['SolarRadiation']
    
        #5400 REM * CALCULATE SOLAR AZIMUTH IN DEGREES, Z4.DEG
        data['Z4_DEG'] = data['CAZ'] + np.arctan(data['CHI'])
        data['Z4_RAD'] = data['Z4_DEG']*data['DEG_TO_RAD']
        data['Z1_RAD'] = data['Z1_DEG']*data['DEG_TO_RAD']
        data['E1'] = np.cos(data['H3_RAD'])*np.cos(data['Z4_RAD']-data['Z1_RAD'])
        data['E2_RAD'] = np.arctan(np.sqrt(1/data['E1']**2 - 1))
        data['QS'] = (data['ABSORP']*data['Q3']*np.sin(data['E2_RAD'])*data['D']/1000*(1 
                                 + 0.0001148*data['CDR_ELEV']-1.108E-08*data['CDR_ELEV']**2))
    
        if data['QS'] < 0:
            data['QS']=0.0
    
        #return data
        return (self.C1.DELTIME)
   #End Function ieee_738_2013_solar

    def print_ver( self):
        print("IEEE738. 10/1/2023. 0:45") 