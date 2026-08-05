# -*- coding: utf-8 -*-
"""
Module: solar

Description
-----------
Solar geometry and time-conversion utilities for PyPacity ampacity
calculations. Provides methods for computing extraterrestrial radiation,
solar declination, hour angle, solar azimuth, and the conversions between
standard clock time and solar time. Designed to support the solar
heat-gain calculations required by CIGRE TB 601 and CIGRE TB 207 overhead
line ampacity models.

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
- CIGRE Technical Brochure 601, Guide for Thermal Rating Calculations of Overhead Lines
- CIGRE Technical Brochure 207, Thermal Rating of Overhead Lines
- J. A. Duffie and W. A. Beckman, Solar Engineering of Thermal Processes, Wiley
"""


import math
import numpy as np


class SolarGeometry():
    """Solar geometry and time-conversion toolkit.

    Computes solar declination, hour angle, azimuth, extraterrestrial
    radiation, and standard-to-solar time conversions. Accepts a geographic
    location at construction time and uses it in all subsequent method calls.

    .. raw:: html

       <p style="text-align:center; font-weight:bold; text-decoration:underline;">Attributes</p>

    .. csv-table::
       :header: "Attribute", "Type", "Role", "Description"
       :widths: 18, 8, 12, 62
       :align: center

       "``Location``", "str", "Parameter", "Name of the location. Defaults to ``'Santander'``."
       "``Country``", "str", "Parameter", "Country name. Used to determine the local daylight saving time offset. Defaults to ``'Spain'``."
       "``Lat``", "float", "Parameter", "Geographic latitude in degrees (constructor parameter ``Latitude``). Defaults to ``43.46``."
       "``Lon``", "float", "Parameter", "Geographic longitude in degrees (constructor parameter ``Longitude``). Defaults to ``-3.8``."
       "``version``", "str", "Variable", "Module version string."
       "``vdate``", "str", "Variable", "Release date of the current version."
       "``Gsc``", "float", "Variable", "Solar constant in W/m² (1367.0 W/m²)."
       "``SolarDistance``", "float", "Variable", "Mean Sun–Earth distance in meters (1.495×10¹¹ m)."
       "``EarthDiameter``", "float", "Variable", "Earth diameter in meters (1.27×10⁷ m)."
       "``SunDiameter``", "float", "Variable", "Sun diameter in meters (1.39×10⁹ m)."
    """
        
    def __init__(self, Location='Santander', Country='Spain', Latitude=43.46, Longitude=-3.8):
        """Initialise instance attributes from the constructor parameters."""

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
        """Compute the extraterrestrial solar radiation for a given day of the year.

        :param day: Day of the year in the range [1, 365].
        :type day: int

        :return: Extraterrestrial radiation in W/m².
        :rtype: float
        """
        # input: day .- Day of the year [1, 365]
        # return: Gon .- Extraterrestrial radiation [W/m^2]
        Gon=self.Gsc*(1.0+0.033*math.cos(360.0*day*math.pi/(365.0*180.0)))
        return Gon
    
    def DayOfYear(self, day, month):
        """Compute the day of the year from the day of the month and the month.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int

        :return: Day of the year in the range [1, 365].
        :rtype: int

        .. note::
            Uses a fixed monthly offset table and does not apply a leap-year
            correction. For leap-year-aware computation from a
            :class:`datetime.datetime` object use :meth:`DatetimetoDayOfYear`.
        """
        # input: day .- Day of the month [1,31]
        #        month .- Month [1,12] 
        # return: Day of year [1,365]
        offset=[0,0,31,59,90,120,151,181,212,243,273,304,334]
        DoY=offset[month]+day
        return DoY

    def Declination(self, day):
        """Compute the solar declination for a given day of the year.

        :param day: Day of the year in the range [1, 365].
        :type day: int

        :return: Solar declination in degrees.
        :rtype: float
        """
        # input: day .- Day of the year [1,365]
        # return: Declination of the Earth [degrees]
        delta=23.45*math.sin( (284.0+day)*360.0*math.pi/(365.0*180.0))
        return delta

    def LongStd(self):
        """Compute the standard meridian nearest to ``Lon`` (ceiling to the next multiple of 15°).

        :return: Standard meridian longitude in degrees (multiple of 15).
        :rtype: int
        """
        # input: Long .- Longitude in degrees [0, 360º] East direction
        # return: Longitude of the close [ceil aprox.] 15n with n {1,2,3,...}
        LongStd=15*math.ceil( self.Lon/15.0)
        return LongStd
   
    def ET(self, dayofyear):
        """Compute the equation of time — the difference between solar and sidereal time.

        :param dayofyear: Day of the year in the range [1, 365].
        :type dayofyear: int

        :return: Equation of time in minutes.
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
        """Convert a clock time to standard time in minutes past midnight.

        Applies a daylight saving time correction when applicable for the
        configured country.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int
        :param hour: Hour of the day in the range [0, 23].
        :type hour: int
        :param minutes: Minutes of the hour in the range [0, 59].
        :type minutes: int

        :return: Standard time in minutes past midnight.
        :rtype: int
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
        """Convert standard clock time to solar time in minutes past midnight.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int
        :param hour: Hour in standard time in the range [0, 23].
        :type hour: int
        :param minutes: Minutes in standard time in the range [0, 59].
        :type minutes: int

        :return: Solar time in minutes past midnight.
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
        """Convert solar time to standard time in minutes past midnight.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int
        :param solartime: Solar time in minutes past midnight.
        :type solartime: float

        :return: Standard time in minutes past midnight.
        :rtype: float
        """
        # input: day .- Day of the month [1,31]
        #        month .- Month of the year [1,12]
        #        hour .- Hour std time [0,23]
        #        minute .- Minute std time [0,59]
        #        Long .- Longitude in degrees (+ West; - East)
        # return: Standard Time [min]
        LStd=self.LongStd()
        DoY=self.DayOfYear( day, month)
        E=self.ET( DoY)
        StdTime=solartime-4.0*(LStd-self.Lon)-E
        return StdTime

    def SolarTimetoHourAngle(self, SolarTime):
        """Convert solar time to the hour angle omega.

        :param SolarTime: Solar time in minutes past midnight.
        :type SolarTime: float

        :return: Hour angle omega in degrees (negative before solar noon,
            positive after).
        :rtype: float
        """
        # Input: SolarTime .- Solar time in minutes past midnight [minutes]
        # return: omega [degrees]
        omega=(SolarTime-720.0)/4.0
        return omega
    
    def StandardTimetoHM(self, standardtime, day, month):
        """Convert standard time in minutes to a ``[hour, minutes]`` list.

        Applies a daylight saving time correction when applicable for the
        configured country.

        :param standardtime: Standard time in minutes past midnight.
        :type standardtime: float
        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int

        :return: Two-element list ``[hour, minutes]`` in official local time.
        :rtype: list
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
        """Convert the hour angle to solar time in minutes past midnight.

        :param HourAngle: Hour angle in degrees.
        :type HourAngle: float

        :return: Solar time in minutes past midnight.
        :rtype: float
        """
        # Input: HourAngle [degrees]
        # Return: solar time [minutes]
        ST=HourAngle*4.0+720
        return ST

    def Theta(self, day, month, hour, minutes, Azimuth, beta):
        """Compute the angle of incidence of solar radiation on a tilted surface.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int
        :param hour: Solar time hour in the range [0, 23].
        :type hour: int
        :param minutes: Solar time minutes in the range [0, 59].
        :type minutes: int
        :param Azimuth: Surface azimuth angle in degrees.
        :type Azimuth: float
        :param beta: Surface tilt angle from the horizontal in degrees.
        :type beta: float

        :return: Angle of incidence theta in degrees.
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

    def Azimuth(self, day, month, hour, minutes):
        """Compute the solar azimuth angle.

        :param day: Day of the month in the range [1, 31].
        :type day: int
        :param month: Month of the year in the range [1, 12].
        :type month: int
        :param hour: Solar time hour in the range [0, 23].
        :type hour: int
        :param minutes: Solar time minutes in the range [0, 59].
        :type minutes: int

        :return: Solar azimuth angle in degrees.
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
        """Compute the sunset hour angle in degrees.

        :param declination: Solar declination in degrees.
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
        """Return the location name.

        :return: Location name.
        :rtype: str
        """
        return self.Location
 
    def GetLatitude(self):
        """Return the latitude in degrees.

        :return: Latitude in degrees.
        :rtype: float
        """
        return self.Lat
    
    def GetLongitude(self):
        """Return the longitude in degrees.

        :return: Longitude in degrees.
        :rtype: float
        """
        return self.Lon
    
    def print_ver(self):
        """Print and return the module name, version, and last update date.

        :return: Module name, version, and last update date.
        :rtype: str
        """
        ver = "PVSystems module. Version: " + str(self.version) + ". Last update: " + str(self.vdate)
        print(ver)
        return ver
        
        
    def DatetimetoDayOfYearNative(self, dt):
        """Compute the day of the year from a datetime object using Python's built-in calendar.

        Delegates to :func:`datetime.datetime.timetuple` so leap years are
        handled automatically.

        :param dt: Date and time.
        :type dt: datetime.datetime

        :return: Day of the year in the range [1, 365/366].
        :rtype: int
        """
        DoY=dt.timetuple().tm_yday
        return DoY


    def DatetimetoSolarTime(self, dt):
        """Compute the solar time in minutes from a datetime object.

        :param dt: Date and time in official local time.
        :type dt: datetime.datetime

        :return: Solar time in minutes past midnight.
        :rtype: float
        """
        # input: dt .- datetime object in official local time
        # return: Solar time [minutes]
        day=dt.day
        month=dt.month
        hour=dt.hour
        minutes=dt.minute+dt.second/60.0+dt.microsecond/(60.0*1e6)

        STime=self.StandardTimetoSolarTime(day, month, hour, minutes)

        return STime


    def DatetimetoSolarHour(self, dt):
        """Compute the solar time in decimal hours from a datetime object.

        :param dt: Date and time in official local time.
        :type dt: datetime.datetime

        :return: Solar time in decimal hours in the range [0, 24).
        :rtype: float
        """
        # input: dt .- datetime object in official local time
        # return: Solar time [hours]
        STime=self.DatetimetoSolarTime(dt)

        SolarHour=(STime/60.0)%24.0

        return SolarHour
        
    def DatetimetoDayOfYear(self, dt):
        """Compute the day of the year from a datetime object using an explicit offset table.

        Uses a monthly offset table with an explicit Gregorian leap-year
        correction. See also :meth:`DatetimetoDayOfYearNative` for an
        equivalent implementation that delegates to Python's built-in calendar.

        :param dt: Date and time.
        :type dt: datetime.datetime

        :return: Day of the year in the range [1, 365/366].
        :rtype: int
        """
        offset=[0,0,31,59,90,120,151,181,212,243,273,304,334]

        year=dt.year
        month=dt.month
        day=dt.day

        DoY=offset[month]+day

        # leap year correction
        if ( (year%4==0 and year%100!=0) or (year%400==0) ):
            if month>2:
                DoY=DoY+1

        return DoY