pypacity
##########################

.. image:: https://github.com/shunsvineyard/python-sample-code/workflows/Test/badge.svg
    :target: https://github.com/shunsvineyard/python-sample-code/actions?query=workflow%3ATest

.. image:: https://github.com/shunsvineyard/python-sample-code/workflows/Linting/badge.svg 
    :target: https://github.com/shunsvineyard/python-sample-code/actions?query=workflow%3ALinting

.. image:: https://codecov.io/gh/shunsvineyard/python-sample-code/branch/main/graph/badge.svg?token=zLkKU6p7do
    :target: https://codecov.io/gh/shunsvineyard/python-sample-code
    
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


The **pypacity** is a Python library for ampacity computation. 

The library provides methods for the computation of IEEE 738 and CIGRE TB 601.

.. math::
    q_c + q_r = q_s + I^2 R(T_{avg})

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

Examples
--------

.. code-block:: python

    from cable import cable
    from case import case
    from ieee738 import ieee738
    import matplotlib.pyplot as plt 

    from importlib import reload
    reload(  cable)
    reload(  case)
    reload( ieee738)

    NSELECT = 3
    Cable1 = cable.Cable()
    Cable1.demo( NSELECT, conductor = '400 mm2 DRAKE 26/7 ACSR')
    #Cable1.print_ver()

    Case1 = case.Case()
    Case1.demo( NSELECT)
    #Case1.print_ver()

    X1 = ieee738.IEEE738()
    X1.set_cable( Cable1)
    X1.set_case( Case1)
    X1.ieee_738_2013()

    if NSELECT == 3:
        plt.plot( X1.Case1.TIME, X1.Case1.ATCDR)


