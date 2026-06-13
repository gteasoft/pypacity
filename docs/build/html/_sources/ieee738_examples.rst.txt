ieee738 examples
================

The following examples show how to use the :class:`~ieee738.ieee738.IEEE738`
class. Each example requires a :class:`~cable.cable.Cable` object with conductor
parameters and a :class:`~case.case.Case` object with environmental conditions.

Use :meth:`~cable.cable.Cable.set_cable` to load a conductor from the database
and :meth:`~case.case.Case.demo` to populate the case with built-in test values.
Assign both to the solver using :meth:`~ieee738.ieee738.IEEE738.set_cable` and
:meth:`~ieee738.ieee738.IEEE738.set_case` before calling
:meth:`~ieee738.ieee738.IEEE738.ieee_738_2013`.

Example 1 — Steady-state conductor temperature (NSELECT = 1)
-------------------------------------------------------------

Given a constant current, compute the resulting steady-state conductor
temperature. The result is stored in ``case.TCDRPRELOAD``.

.. code-block:: python

    from ieee738.ieee738 import IEEE738
    from cable.cable import Cable
    from case.case import Case

    solver = IEEE738()
    cable = Cable()
    case = Case()

    cable.set_cable(1, 'DRAKE')
    case.demo(1)

    solver.set_cable(cable)
    solver.set_case(case)
    solver.ieee_738_2013()

    print("Conductor temperature:", case.TCDRPRELOAD, "ºC")

Example 2 — Steady-state thermal rating (NSELECT = 2)
------------------------------------------------------

Given a maximum conductor temperature, compute the steady-state ampacity.
The result is stored in ``case.TR``.

.. code-block:: python

    from ieee738.ieee738 import IEEE738
    from cable.cable import Cable
    from case.case import Case

    solver = IEEE738()
    cable = Cable()
    case = Case()

    cable.set_cable(2, 'DRAKE')
    case.demo(2)

    solver.set_cable(cable)
    solver.set_case(case)
    solver.ieee_738_2013()

    print("Thermal rating:", case.TR, "A")

Example 3 — Transient conductor temperature (NSELECT = 3)
----------------------------------------------------------

Given a step change in current from ``XIPRELOAD`` to ``XISTEP``, compute the
conductor temperature over time. Results are stored in ``case.ATCDR``
(temperature trace) and ``case.TIME`` (time trace) and can be plotted directly.

.. code-block:: python

    import matplotlib.pyplot as plt
    from ieee738.ieee738 import IEEE738
    from cable.cable import Cable
    from case.case import Case

    solver = IEEE738()
    cable = Cable()
    case = Case()

    cable.set_cable(3, 'DRAKE')
    case.demo(3)
    case.ATCDR = []
    case.TIME = []

    solver.set_cable(cable)
    solver.set_case(case)
    solver.ieee_738_2013()

    plt.plot(case.TIME, case.ATCDR)
    plt.xlabel("Time (s)")
    plt.ylabel("Conductor temperature (ºC)")
    plt.show()
