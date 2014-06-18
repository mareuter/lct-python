=======================
Lunar Club Tools README
=======================

.. image:: https://travis-ci.org/mareuter/lct-python.svg
   :target: https://travis-ci.org/mareuter/lct-python

.. _Astronomical League: http://www.astroleague.org
.. _Python: http://www.python.org
.. _PyQt: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _pyephem: http://pypi.python.org/pypi/pyephem
.. _pip: https://pip.pypa.io/en/latest/installing.html
.. _homebrew: http://brew.sh/

A tool to aid in completing the `Astronomical League`_'s Lunar and Lunar II observing clubs. 
It is written in `Python`_ using `PyQt`_ for the UI and the `pyephem`_ library for lunar 
calculations.

The program provides general information about the current lunar status. Based on the current 
location of the lunar terminator, the program determines the visibility of features required to 
complete the observing clubs. Certain requirements are based on the current lunar phase and the 
times to and from new moon. These are calculated and presented in a table with indicators that 
show when the requirement is occurring (not necessarily visible).   

Installing
----------

Requirements
############

- Python 2.7
- PyQt >= 4.8 (not 5)
- pyephem >= 3.7.4.1
- tzlocal >= 1.1.1
- QDarkStyle >= 1.9

Linux
^^^^^

The correct version of `Python`_ should already be install on your system. If not, get the 2.7 version 
via the appropriate package manager. You will then need to install `PyQt`_ libraries and build tools 
packages. The names vary between OS flavors. Next, follow the installation instructions for `pip`_ 
appropriate to Linux. Once that is complete, run the following::
 
 pip install lct

OSX
^^^

The correct version of `Python`_ should already be install on your system. To get `PyQt`_, the best 
way is via `homebrew`_::
 
 brew install pyqt

Then, follow the installation instructions for `pip`_ appropriate to OSX. Once that is complete, 
run the following::
 
 pip install lct

Windows
^^^^^^^

Download the correct version from `Python`_. Be sure you note if you install the 64-bit or 32-bit 
version of Python. Download the correct associated version of `PyQt`_ from their site and install. 
Next, download the correct associated version of `pyephem`_ and install. Then, follow the installation 
instructions for `pip`_ appropriate to Windows. Once that is complete, run the following::

 pip install lct

Alternatively, you can download the associated version of the Lunar Club Tools here. However, you 
will need to install two other packages via `pip`_::

 pip install tzlocal
 pip install qdarkstyle

Running
-------

As long as the installation directory for `Python`_ scripts is in your PATH, the program is run via 
the following::

 lunar_club_tools.py
 