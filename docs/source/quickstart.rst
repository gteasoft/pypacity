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

Input parameters
^^^^^^^^^^^^^^^^

.. tabularcolumns:: |p{4cm}|p{10cm}|p{10cm}|

.. csv-table::
   :file: files/thermal_rating_input.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1
   :align: center

Output parameters
^^^^^^^^^^^^^^^^^

.. tabularcolumns:: |p{4cm}|p{10cm}|p{10cm}|

.. csv-table::
   :file: files/thermal_rating_output.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1
   :align: center

Example
^^^^^^^

The following example selects a DRAKE conductor, defines the ambient and
operating conditions, and computes its thermal rating according to IEEE 738
and CIGRE TB 601.

.. code-block:: python

   from cable import cable
   from case import case
   from ieee738 import ieee738
   from cigre601 import cigre601
   from pvsystems import pvsystems

   NSELECT = 2

   # Conductor data
   cable_1 = cable.Cable()
   cable_db, error = cable_1.load_cable_db()
   cable_1.set_cable(NSELECT, conductor="DRAKE")
   cable_1.EMISS = 0.8
   cable_1.ABSORP = 0.8

   # Environmental and operating conditions
   pv_1 = pvsystems.PVSystems()
   case_1 = case.Case()
   case_1.demo(NSELECT)

   case_1.TAMB = 40.0
   case_1.CDR_LAT_DEG = 30
   case_1.ALBEDO = 0.1
   case_1.beta = 0
   case_1.CDR_ELEV = 0
   case_1.TCDR = 100.0
   case_1.WINDANG_DEG = 60
   case_1.Z1_DEG = 90
   case_1.Ns = 1.0
   case_1.SUN_TIME = 11
   case_1.NDAY = pv_1.DayOfYear(10, 6)  # 10 June

   print("NDAY:", case_1.NDAY)

   # IEEE 738
   ieee_model = ieee738.IEEE738()
   ieee_model.Debug = 0
   ieee_model.set_cable(cable_1)
   ieee_model.set_case(case_1)
   ieee_model.Case1.ITCDRPRELOAD = 40
   ieee_model.Case1.TT = 60 * 15
   ieee_model.Case1.SORM = 1

   ieee_model.ieee_738_2013()
   ieee_model.outputs()

   # CIGRE TB 601
   cigre_model = cigre601.CIGRE601()
   cigre_model.Debug = 0
   cigre_model.set_cable(cable_1)
   cigre_model.set_case(case_1)

   cigre_model.cigre601()
   cigre_model.outputs()

Notes
^^^^^

* The paths in the ``csv-table`` directives assume that this file is stored
  as ``docs/source/quickstart.rst`` and that the CSV files are stored in
  ``docs/source/files``.
* The import statements reproduce the current module structure of the example.
  They should be updated if the package is reorganized to use imports such as
  ``from pypacity...``.
