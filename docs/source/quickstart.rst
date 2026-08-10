Quick start
===========

This section presents a basic steady-state thermal-rating calculation using
both the IEEE 738 and CIGRE TB 601 methods implemented in **PyPacity**.

Thermal rating: :math:`I_{CDR}=f(T_{CDR})`
------------------------------------------------

The objective is to calculate the steady-state conductor current for a
specified steady-state conductor temperature. The thermal equilibrium is
expressed as

.. math::

   q_c + q_r = q_s + I^2 R(T_{avg}),

where :math:`q_c` is the convective heat loss, :math:`q_r` is the radiative
heat loss, :math:`q_s` is the solar heat gain, and :math:`R(T_{avg})` is the
conductor resistance evaluated at its average temperature.



Example
^^^^^^^

The following example selects a DRAKE conductor, defines the ambient and
operating conditions, and computes its thermal rating according to IEEE 738
and CIGRE TB 601.

.. code-block:: python

   from pypacity.cable import cable
   from pypacity.case import case
   from pypacity.ieee738 import ieee738
   from pypacity.cigre601 import cigre601
   from pypacity.utils import solar

   import matplotlib.pyplot as plt 
   from datetime import datetime

   print("*******************************************************************")  
   print("*******************************************************************")
   print("CIGRE TB 601 - Thermal rating of power cables")
   print("Example A: Page 79")
   print("*******************************************************************")  

   NSELECT = 2 
   Cable1 = cable.Cable()
   c_db, error = Cable1.load_cable_db()
   Cable1.set_cable( NSELECT, conductor = 'DRAKE')
   Cable1.EMISS = 0.8
   Cable1.ABSORP = 0.8

   # Case 1
   dt1 = datetime(2026, 6, 10, 11, 00)
   print("Date and time: " + str(dt1))
   SG1 = solar.SolarGeometry()
   Case1 = case.Case()
   Case1.demo( NSELECT)
   # Ambient conditions
   Case1.TAMB = 40.0
   Case1.CDR_LAT_DEG = 30
   Case1.ALBEDO = 0.1
   Case1.beta = 0
   Case1.CDR_ELEV = 0
   Case1.TCDRPRELOAD = 100
   Case1.VWIND = 0.61
   Case1.DWIND_DEG = 60
   Case1.Z1_DEG = 0
   Case1.SOLAR = 1
   Case1.Ns = 1.0
   Case1.SUN_TIME = round(SG1.DatetimetoSolarHour(dt1),3)
   print("SUN_TIME: " + str(Case1.SUN_TIME)) # SUN_TIME > 24 => Measurement available. 
   Case1.NDAY = SG1.DatetimetoDayOfYear(dt1) 
   print("NDAY: " + str(Case1.NDAY))

   Case1TB601 = cigre601.CIGRE601()
   Case1TB601.Debug = 0
   Case1TB601.set_cable( Cable1)
   Case1TB601.set_case( Case1)
   Case1TB601.cigre601()
   Case1TB601.output()

   Case1IEEE738 = ieee738.IEEE738()
   Case1IEEE738.Debug = 0
   Case1IEEE738.set_cable( Cable1)
   Case1IEEE738.set_case( Case1)
   Case1IEEE738.ieee_738_2013()
   Case1IEEE738.output()

   print(" ")
   print(" ")
   print("*******************************************************************")  
   print("*******************************************************************")
   print("CIGRE TB 601 - Thermal rating of power cables")
   print("Example B: Page 79")
   print("*******************************************************************")  

   NSELECT = 2 
   Cable2 = cable.Cable()
   c_db, error = Cable1.load_cable_db()
   Cable2.set_cable( NSELECT, conductor = 'DRAKE')
   Cable2.EMISS = 0.9
   Cable2.ABSORP = 0.9

   # Case 1
   dt2 = datetime(2026, 10, 3, 14, 00)
   print("Date and time: " + str(dt2))
   SG2 = solar.SolarGeometry()
   Case2 = case.Case()
   Case2.demo( NSELECT)
   # Ambient conditions
   Case2.TAMB = 20.0
   Case2.CDR_LAT_DEG = 50
   Case2.ALBEDO = 0.15
   Case2.beta = 10
   Case2.CDR_ELEV = 500
   Case2.TCDRPRELOAD = 100
   Case2.VWIND = 1.66
   Case2.DWIND_DEG = 80
   Case2.Z1_DEG = 0
   Case2.SOLAR = 1
   Case2.Ns = 0.5
   Case2.SUN_TIME = round(SG2.DatetimetoSolarHour(dt2),3)
   print("SUN_TIME: " + str(Case2.SUN_TIME))
   Case2.NDAY = SG2.DatetimetoDayOfYear(dt2) 
   print("NDAY: " + str(Case2.NDAY))

   Case2TB601 = cigre601.CIGRE601()
   Case2TB601.Debug = 0
   Case2TB601.set_cable( Cable2)
   Case2TB601.set_case( Case2)
   Case2TB601.cigre601()
   Case2TB601.output()

   Case2IEEE738 = ieee738.IEEE738()
   Case2IEEE738.Debug = 0
   Case2IEEE738.set_cable( Cable2)
   Case2IEEE738.set_case( Case2)
   Case2IEEE738.ieee_738_2013()
   Case2IEEE738.output()


