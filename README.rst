.. image:: https://raw.githubusercontent.com/gteasoft/pypacity/master/docs/source/_images/pypacity_logo.png
   :alt: PyPacity
   :width: 300px
   :align: center


PyPacity
========

|docs-status| |pypi-version| |python-versions| |project-status| |license|

.. |docs-status| image:: https://github.com/gteasoft/pypacity/actions/workflows/docs.yml/badge.svg?branch=master
   :target: https://github.com/gteasoft/pypacity/actions/workflows/docs.yml?query=branch%3Amaster
   :alt: Documentation build status

.. |pypi-version| image:: https://img.shields.io/pypi/v/pypacity.svg
   :target: https://pypi.org/project/pypacity/
   :alt: PyPI version

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/pypacity.svg
   :target: https://pypi.org/project/pypacity/
   :alt: Supported Python versions

.. |project-status| image:: https://img.shields.io/pypi/status/pypacity.svg
   :target: https://pypi.org/project/pypacity/
   :alt: PyPI development status

.. |license| image:: https://img.shields.io/pypi/l/pypacity.svg
   :target: https://pypi.org/project/pypacity/
   :alt: Project license

**PyPacity** is a Python library for computing the ampacity of
overhead electrical conductors.

It implements the IEEE 738 and CIGRE TB 601 methods under
steady-state and transient conditions.

Requirements
------------

PyPacity requires Python 3.9 or newer.

Installation
------------

Install the latest release from PyPI:

.. code-block:: console

   python -m pip install pypacity

Alternatively, install the current development version from GitHub:

.. code-block:: console

   git clone https://github.com/gteasoft/pypacity.git
   cd pypacity
   python -m pip install .

Documentation
-------------

The `complete documentation <https://gteasoft.github.io/pypacity/>`_
includes the theoretical formulation, input and output parameters, and
application examples.

.. image:: https://raw.githubusercontent.com/gteasoft/pypacity/master/docs/source/_images/UC_logo.png
   :alt: Universidad de Cantabria
   :width: 200px
   :align: center
