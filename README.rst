pypacity 
##########################



.. image:: docs/images/pypacity_logo.png
   :alt: Pypacity
   :align: center

   <br>

.. raw:: html
    .. image:: pypacity_logo.png   

.. raw:: html
    .. image:: https://github.com/shunsvineyard/python-sample-code/workflows/Linting/badge.svg 
        :target: https://github.com/shunsvineyard/python-sample-code/actions?query=workflow%3ALinting

.. raw:: html
    .. image:: https://codecov.io/gh/shunsvineyard/python-sample-code/branch/main/graph/badge.svg?token=zLkKU6p7do
        :target: https://codecov.io/gh/shunsvineyard/python-sample-code

.. raw:: html
    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black


The **pypacity** is a Python library for ampacity computation. 

The library provides methods for the computation of IEEE 738 and CIGRE TB 601 in both static and transient conditions.

.. math::
    q_c + q_r = q_s + I^2 R(T_{avg})


**pypacity** is a joint development of the GTEA research group of the Department of Electrical and Energy Engineering, Universidad de Cantabria, Spain.



Requirements
------------

The **pypacity** requires Python 3.9 or newer.

Installation
------------

Install from Github

.. code-block:: text

    git clone https://github.com/mmanana/pypacity.git
    cd pypacity
    pip install .


Quick Start
--------------


Thermal Rating. I_CDR = f(T_CDR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Calculate the steady-state current (Case.TR) given the steady-state conductor temperature (Case.TCDR)

.. raw:: html

   <p style="text-align:center; font-weight:bold; text-decoration:underline;">Input Parameters</p>

.. tabularcolumns:: |p{4cm}|p{10cm}|p{10cm}|

.. csv-table::
    :file: files/thermal_rating_input.csv
    :header-rows: 1
    :class: longtable
    :widths: 1 1 1
    :align: center



.. raw:: html

   <p style="text-align:center; font-weight:bold; text-decoration:underline;">Output Parameters</p>

.. tabularcolumns:: |p{4cm}|p{10cm}|p{10cm}|

.. csv-table::
    :file: files/thermal_rating_output.csv
    :header-rows: 1
    :class: longtable
    :widths: 1 1 1
    :align: center


**Example**


.. code-block:: python

    from cable import cable
    from case import case
    from ieee738 import ieee738
    from cigre601 import cigre601
    from pvsystems import pvsystems
    import matplotlib.pyplot as plt 

    NSELECT = 2 
    Cable1 = cable.Cable()
    c_db, error = Cable1.load_cable_db()
    Cable1.set_cable( NSELECT, conductor = 'DRAKE')
    Cable1.EMISS = 0.8
    Cable1.ABSORP = 0.8

    PV1 = pvsystems.PVSystems()
    Case1 = case.Case()
    Case1.demo( NSELECT)
    # Ambient conditions
    Case1.TAMB = 40.0
    Case1.CDR_LAT_DEG = 30
    Case1.ALBEDO = 0.1
    Case1.beta = 0
    Case1.CDR_ELEV = 0
    Case1.TCDR = 100.0
    Case1.WINDANG_DEG = 60
    Case1.Z1_DEG = 90
    Case1.Ns = 1.0
    Case1.SUN_TIME = 11
    Case1.NDAY = PV1.DayOfYear( 10, 6) # 10th June
    print("NDAY: " + str(Case1.NDAY))

    # IEEE 738
    X1 = ieee738.IEEE738()
    X1.Debug = 0
    X1.set_cable( Cable1)
    X1.set_case( Case1)
    X1.Case1.ITCDRPRELOAD = 40
    #X1.Case1.TCDRMAX = 150
    X1.Case1.TT = 60*15
    X1.Case1.SORM = 1

    X1.ieee_738_2013()
    X1.outputs()

    # CIGRE TB601
    X2 = cigre601.CIGRE601()
    X2.Debug = 0
    X2.set_cable( Cable1)
    X2.set_case( Case1)

    X2.cigre601()
    X2.outputs()


.. raw:: html
    .. image:: _images/50UC_RGB.svg   
        :width: 200px


.. image:: docs/images/UC_logo.png
   :alt: Universidad de Cantabria
   :align: center
