import pytest



def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import ubermagcalculatorbase
    ...
    >>> # ubermagcalculatorbase.test()

    """
    return pytest.main(
        ["-v", "--pyargs", "ubermagcalculatorbase", "-l"]
    )  # pragma: no cover
