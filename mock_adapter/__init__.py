"""
This subpackage provides an adapter package for the `mock_calculator`. Its purpose is
two-fold:

- It can be used as a template when writing a new adapter package for an additional
  calculator. It is based on a fake calculator `mock_calculator` that produces data
  similar to typical micromagnetic software but does not actually perform simulations.
  Therefore, the calculator's logic is very simple and it should be straight-forward to
  follow the communication logic between adapter and calculator.
- The `mock_adapter` is used to generate data for `micromagneticdata` and `ubermagtable`
  without the need to have an actual external calculator package.

THIS PACKAGE IS NOT INTENDED FOR UBERMAG USERS WHO WANT TO RUN MICROMAGNETIC SIMULATIONS!
"""
from .mock_driver import MinDriver as MinDriver, TimeDriver as TimeDriver
from .mock_runner import MockCalculatorRunner as MockCalculatorRunner
from .scripts import input_script as input_script

import pytest



def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import mock_adapter
    ...
    >>> # mmock_adapter.test()

    """
    return pytest.main(
        ["-v", "--pyargs", "mock_adapter", "-l"]
    )  # pragma: no cover
