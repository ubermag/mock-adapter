import re
import sys

from mock_adapter import MockCalculatorRunner


def test_name():
    assert MockCalculatorRunner().package_name == "Ubermag Mock Calculator"


def test_call_dry_run():
    runner = MockCalculatorRunner()

    cmd = runner._call("input.json", dry_run=True)
    assert cmd == f"{sys.executable} -m mock_calculator input.json"


def test_call():
    runner = MockCalculatorRunner()
    # call the calculator with a non-existing input file; the simulation will fail and
    # we can check return code and reason for the error
    res = runner._call("inputfile.does-not-exist")
    assert res.returncode == 1
    assert "FileNotFoundError" in res.stderr.decode("utf-8")
    assert re.search(
        "No such file or directory:.*inputfile.does-not-exist",
        res.stderr.decode("utf-8"),
    )
