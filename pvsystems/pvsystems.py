# -*- coding: utf-8 -*-

import math
import numpy as np


class PVSystems:
    """Class PVSystems.
        
    Implement several tools for solar computation.
        
    Attributes:
        :version (str): Version of the PVSystems module.
        :vdate (str): Date of current version.
        :Gsc (float): The solar constant (Gsc) is a flux density measuring mean solar electromagnetic radiation (total solar irradiance) per unit area. Value adopted by Duffie-Beckman [SOLAR ENG. of THERMAL PROCESSES. pg. 10].
        :SolarDistance (float): 1.495e11 m. Distance between the Sun and the Earth [meters].
        :EarthDiameter (float): 1.27e7 m. Return: Earth diameter [meters].
        :SunDiameter (float): 1.39e9 m. Return: Sun diameter [meters].
        :Location (str): Description of the location.
        :Country (str): Country.
        :Lat (float): Latitude.
        :Lon (float): Longitude.
    """
        
    def __init__(self, Location='Santander', Country='Spain', Latitude=43.46, Longitude=-3.8):
        """_summary_

        :param Location: _description_. Defaults to 'Santander'.
        :type Location: str, optional.
        :param Country: _description_. Defaults to 'Spain'.
        :type Country: str, optional.
        :param Latitude: _description_. Defaults to 43.46.
        :type Latitude: float.
        :param Longitude: _description_. Defaults to -3.8.
        :type Longitude: float.
        """

        self.version = '1.0'
        self.vdate = u'8/Apr/2023'
        self.Gsc=1367.0  # Value adopted by Duffie-Beckman [SOLAR ENG. of THERMAL PROCESSES. pg. 10]
        self.SolarDistance=1.495e11 # Distance between the Sun and the Earth [meters]
        self.EarthDiameter=1.27e7 # Return: Earth diameter [meters]
        self.SunDiameter=1.39e9 # Return: Sun diameter [meters]
        self.Location=Location
        self.Country=Country
        self.Lat=Latitude
        self.Lon=Longitude

    def Gon(self, day):
        """Computes the solar radiation for a specific <day>.
                
        :param day: Day of the year [1 365].
        :type day: int.
        
        :return: Extraterrestrial radiation [W/m^2].
        :rtype float: float...
        """
        # input: day .- Day of the year [1, 365]
        # return: Gon .- Extraterrestrial radiation [W/m^2]
        Gon=self.Gsc*(1.0+0.033*math.cos(360.0*day*math.pi/(365.0*180.0)))
        return Gon
    
    def DayOfYear(self, day, month):
        """Computes the day of the year with the month and the day of the month.

        :param day: day of the month [1, 31].
        :type day: int
        :param month: month of the year [1, 12].
        :type month: int

        :return: Day of the year [1 365]
        :rtype: int
        """
        # input: day .- Day of the month [1,31]
        #        month .- Month [1,12] 
        # return: Day of year [1,365]
        offset=[0,0,31,59,90,120,151,181,212,243,273,304,334]
        DoY=offset[month]+day
        return DoY

    def Declination(self, day):
        """ Computes the declination of the Earth (degree).
        
        :param day: Day of the year [1, 365]
        :type day: int
        
        :return: Declination of the Earth (degrees).
        :rtype: float
        """
        # input: day .- Day of the year [1,365]
        # return: Declination of the Earth [degrees]
        delta=23.45*math.sin( (284.0+day)*360.0*math.pi/(365.0*180.0))
        return delta

    def LongStd(self):
        """ 
        Computes de normalized Longitude using the self parameter <Lon>. The input value is defined in degrees and the output is 15n with n in {1,2,3,...}.
                
        :return:  Longitude of the close [ceil aprox.] 15n with n {1,2,3,...}.
        :rtype: int
        """
        # input: Long .- Longitude in degrees [0, 360º] East direction
        # return: Longitude of the close [ceil aprox.] 15n with n {1,2,3,...}
        LongStd=15*math.ceil( self.Lon/15.0)
        return LongStd
   
    def ET(self, dayofyear):
        """ 
        Computes de time difference between solar and sideral time in minutes.
        
        :param dayofyear: Day of the year [1, 365]
        :type dayofyear: int
        
        :return: Time diference between solar and sideral time in minutes.
        :rtype: float
        """
        # input: day .- day of the year [1,365]
        # return: ET .- Time difference between solar and sideral time [minutes]
        B=(dayofyear-1)*360.0/365.0
        B=B*math.pi/180.0
        a=0.001868*math.cos(B)
        b=0.032077*math.sin(B)
        c=0.014615*math.cos(2*B)
        d=0.04089*math.sin(2*B)
        ET=229.2*(0.000075+a-b-c-d)
        return ET
    
    def HMtoStandardTime(self, day, month, hour, minutes):
        """  
        Computes the standard time in minutes.
        
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12].
        :type month: int
        :param hour: hour of the day [0, 23]
        :type hour: int
        :param minutes: Minutes of the hour [0, 59]
        :type minutes: int
    
        """
        # Standard time. Daylight Saving Time is taken into account
        # input: day .- day of the month [1,31]
        #        month .- month of the year [1,12]
        #        hour .- hour of day [0,23]
        #        minutes .- minute of hour [0,59]
        # return: Standard Time [minutes]
        DoY=self.DayOfYear( day, month)
        if self.Country=='Spain':
            start=self.DayOfYear( 27, 3)
            end=self.DayOfYear( 30, 10)
            if (DoY>=start) and (DoY<end):
                if hour >= 1:
                    hour=hour-1
                else:
                    hour=23
                    day=day-1
        StdTime=hour*60+minutes
        return StdTime

    def StandardTimetoSolarTime(self, day, month, hour, minutes):
        """ 
        Computes the solar time in minutes.
        
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12].
        :type month: int
        :param hour: Hour standard time [0, 23].
        :type hour: int
        :param minutes: Minutes standard time [0, 59].
        :type minutes: int
        
        :return: Solar time in minutes.
        :rtype: float
        """
        # input: day .- Day of the month [1,31]
        #        month .- Month of the year [1,12]
        #        hour .- Hour std time [0,23]
        #        minutes .- Minutes std time [0,59]
        #        Long .- Longitude in degrees [0,360] East
        # return: Solar time [minutes]
        LStd=self.LongStd()
        DoY=self.DayOfYear( day, month)
        E=self.ET( DoY)
        StdTime=self.HMtoStandardTime( day, month, hour, minutes)           
        STime=round(StdTime+4.0*(LStd-self.Lon)+E,2)
        return STime

    def SolarTimetoStandardTime(self, day, month, solartime):
        """ 
        Computes the standard time.
        
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12].
        :type month: int
        :param solartime: Solartime [minutes].
        :type solartime: float
        
        :return: Standard time in minutes.
        :rtype: float
        
        """
        # input: day .- Day of the month [1,31]
        #        month .- Month of the year [1,12]
        #        hour .- Hour std time [0,23]
        #        minute .- Minute std time [0,59]
        #        Long .- Longitude in degrees (+ West; - East)
        # return: Standard Time [min]
        LStd=self.LongStd( self.Lon)
        DoY=self.DayOfYear( day, month)
        E=self.ET( DoY)
        StdTime=solartime-4.0*(LStd-self.Lon)-E
        return StdTime

    def SolarTimetoHourAngle(self, SolarTime):
        """ 
        Computes the hour angle in degrees.
        
        :param SolarTime: Solar time in minutes past midnight.
        :type SolarTime: float
        
        :return: Omega in degrees.
        :rtype: float
        
        """
        # Input: SolarTime .- Solar time in minutes past midnight [minutes]
        # return: omega [degrees]
        omega=(SolarTime-720.0)/4.0
        return omega
    
    def StandardTimetoHM(self, standardtime, day, month):
        """ 
        Computes de hour and minutes of the day from the standard time in minutes.
        
        :param standardtime: Standard time in minutes.
        :type standardtime: float
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12].
        :type month: int
        
        :return: Array of two elements:
            H[0].- Hour.
            H[1].- Minutes.
        :rtype: array of int
        
        """
        # Input: hourangle .- Solar time in minutes past midnight [minutes]
        #        day .- day of the month [1,31]
        #        month .- month of the year [1,12]
        # Return: H[0] .- hour; H[1] .- minutes
        H=[0,0]
        hour=math.floor( standardtime/60.0)
        minutes=round(standardtime-hour*60.0,0)
        DoY=self.DayOfYear( day, month)
        if self.Country=='Spain':
            start=self.DayOfYear( 27, 3)
            end=self.DayOfYear( 30, 10)
            if (DoY>=start) and (DoY<end):
                hour=hour+2
            else:
                hour=hour+1
        H[0]=hour
        H[1]=minutes
        return H    

    def HourAngletoSolarTime(self, HourAngle):
        """ 
        Computes the solar time in minutes.
        
        :param HourAngle: Hour Angle in degrees.
        :type HourAngle: float
        
        :return: Solar time in minutes.
        :rtype: float
        
        """
        # Input: HourAngle [degrees]
        # Return: solar time [minutes]
        ST=HourAngle*4.0+720
        return ST

    def Theta(self, day, month, hour, minutes, Azimuth, beta):
        """ 
        Computes the solar angle.
        
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12].
        :type month: int
        :param hour: Hour solar time [0, 23].
        :type hour: int
        :param minutes: Minutes of the hour [0, 59].
        :type minutes: int
        :param Azimuth: Azimuth of solar panel in degrees.
        :type Azimuth: float
        :param beta: slope of the PV panel in degrees.
        :type beta: float
        
        :return: Solar angle theta in degrees.
        :rtype: float
        """
        # Input: day .- Day of the month [1,31]
        #        month .- Month of the year [1,12]
        #        hour .- Solar time hour [0,23]
        #        minute .- Solar time minutes [0,59]
        #        Long .- Longitude in degrees [0,360] East [degrees]
        #        Lat .- Latitude in degree [-90,90] [degrees] 
        #        Azimuth .- azimuth of solar panel [degrees]
        #        beta .- slope of the pv panel [degrees]
        # Return: theta [degrees]
        DtR=math.pi/180.0 # Deg to Rad
        DoY=self.DayOfYear( day, month)
        delta=self.Declination( DoY)
        ST=hour*60.0+minutes
        omega=self.SolarTimetoHourAngle( ST)
        phi=self.Lat
        gamma=Azimuth
        A=math.sin(delta*DtR)*math.sin(phi*DtR)*math.cos(beta*DtR)
        B=math.sin(delta*DtR)*math.cos(phi*DtR)*math.sin(beta*DtR)*math.cos(gamma*DtR)
        C=math.cos(delta*DtR)*math.cos(phi*DtR)*math.cos(beta*DtR)*math.cos(omega*DtR)
        D1=math.cos(delta*DtR)*math.sin(phi*DtR)*math.sin(beta*DtR)
        D=D1*math.cos(gamma*DtR)*math.cos(omega*DtR)    
        E=math.cos(delta*DtR)*math.sin(beta*DtR)*math.sin(gamma*DtR)*math.sin(omega*DtR)
        cos_theta=A-B+C+D+E
        theta=math.acos( cos_theta)/DtR
        return theta

    def Azimuth( self, day, month, hour, minutes ):
        """  
        Return de solar azimuth
        
        :param day: Day of the month [1, 31].
        :type day: int
        :param month: Month of the year [1, 12]
        :type month: int
        :param hour: Hour solar time [0, 23]
        :type hour: int
        :param minutes: Minutes solar time [0, 59]
        :type minutes: int
        
        :return: azimuth angle in degrees
        :rtype: float
                
        """
        # Input: day .- day of the month
        #        month .- month
        #        hour .- Solar time hour [0,23]
        #        minute .- Solar time minutes [0,59]
        DtR=math.pi/180.0 # Deg to Rad
        RtD=180.0/math.pi # Rad to Deg
        DoY=self.DayOfYear( day, month)
        delta=self.Declination( DoY)
        ST=hour*60.0+minutes
        omega=self.SolarTimetoHourAngle( ST)
        phi=self.Lat
        azimuth=0
        beta=0
        theta_z=self.Theta(day, month, hour, minutes, azimuth, beta)
        delta=self.Declination( DoY)
        ST=hour*60.0+minutes
        omega=self.SolarTimetoHourAngle( ST)
        angle=math.cos(theta_z*DtR)*math.sin(phi*DtR)-math.sin(delta*DtR)/(math.sin(theta_z*DtR)*math.cos(phi*DtR))
        gamma_s=np.sign(omega)*math.acos(angle)*RtD
        return gamma_s


    def SunsetHourAngle(self, declination):
        """ 
        Computes the sunset hour angle in degrees
        
        :param declination: Declination angle in degrees.
        :type declination: float
        
        :return: Sunset hour angle in degrees.
        :rtype: float
                
        """
        # Input: declination [degrees]
        #        lat .- latitude [degrees]
        # Return: omega_s .- sunset hour angle [degrees]
        DtR=math.pi/180.0 # Deg to Rad
        aux1=math.sin(DtR*declination)*math.sin(DtR*self.Lat)
        cos_omega_s=-(aux1)/(math.cos(DtR*declination)*math.cos(DtR*self.Lat))
        omega_s=math.acos( cos_omega_s)/DtR
        return omega_s
    
    def GetLocation(self):
        """ 
        Return de Location.
        
        :return: Location.
        :rtype: str
        
        """
        return self.Location
 
    def GetLatitude(self):
        """ 
        Return de Latitude in degrees.
        
        :return: Latitude in degrees.
        :rtype: float
        
        """
        return self.Lat
    
    def GetLongitude(self):
        """ 
        Return the Longitude in degrees.
        
        :return: Longitude in degrees.
        :rtype: float
        
        """
        return self.Lon
    
    def print_ver( self):
        """ 
        Print module version
        
        :return: module version
        :rtype: str
        
        """
        ver = "PVSystems module. Version: " + str(self.version) + ". Last update: " + str(self.vdate)
        return ( ver)
        
        
        print("PVSystems. 8/4/2023. 18:30") 