=======================
Lunar Club Tools README
=======================

.. image:: https://travis-ci.org/mareuter/lct-python.svg
   :target: https://travis-ci.org/mareuter/lct-python

.. _Astronomical League: http://www.astroleague.org
.. _Python: http://www.python.org
.. _PyQt: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _pyephem: http://pypi.python.org/pypi/pyephem

A tool to aid in completing the `Astronomical League`_'s Lunar and Lunar II observing clubs. 
It is written in `Python`_ using `PyQt`_ for the UI and the `pyephem`_ library for lunar 
calculations.

The program provides general information about the current lunar status. Based on the current 
location of the lunar terminator, the program determines the visibility of features required to 
complete the observing clubs. Certain requirements are based on the current lunar phase and the 
times to and from new moon. These are calculated and presented in a table with indicators that 
show when the requirement is occurring (not necessarily visible).   
