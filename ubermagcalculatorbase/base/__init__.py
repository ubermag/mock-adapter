"""
This moduule provides base classes for Driver and Runner for adapter packages that
integrate external calculators into the Ubermag framework.

Driver is the main object which users of the adapter package will interact. The most
common interaction is using the ``drive`` method. The overall steps of triggering a
simulation are implemented in the base class. Derived classes must implement a number
of abstract methods, which provide calculator-specific details.

The Runner object is a lower-level object that is responsible for the communication with
the external software. Users of Ubermag do generally not directly interact with it.
"""
from .driver import ExternalDriver as ExternalDriver
from .evolver import Evolver as Evolver
from .runner import ExternalRunner as ExternalRunner
