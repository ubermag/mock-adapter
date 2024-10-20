import datetime
import json

import discretisedfield as df
import pytest

import micromagneticmodel as mm


def test_driver():
    driver = MyDriver()
    assert driver.drive(system=5) == 5
    assert driver._x == "independent_variable"


def test_external_driver(tmp_path):
    system = mm.examples.macrospin()
    driver = MyExternalDriver(arg1="a", arg2="b")
    assert driver._x == "x"

    driver.drive(system, dirname=str(tmp_path))
    m_out = df.Field.from_file(tmp_path / system.name / "drive-0" / "output.omf")
    assert system.m.allclose(m_out)
    assert system.m.allclose(-mm.examples.macrospin().m)
    assert (tmp_path / system.name / "drive-0" / "info.json").exists()

    with open(tmp_path / system.name / "drive-0" / "info.json") as f:
        info = json.load(f)

    assert info["adapter"] == "micromagneticmodel"
    assert info["driver"] == "MyExternalDriver"
    assert info["drive_number"] == 0

    info_time = datetime.datetime.fromisoformat(f"{info['date']}T{info['time']}")
    now = datetime.datetime.now()
    # assumption: this test runs in under one minute
    assert (now - info_time).total_seconds() < 60

    with pytest.raises(FileExistsError):
        driver.drive(system, dirname=str(tmp_path), append=False)

    # There is no scheduling system available for the tests. Instead we use 'python'
    # because we know that this is always an executable. The created schedule script
    # contains only Python comments so nothing is actually happening.
    driver.schedule(system, "python", "#Schedule header", dirname=str(tmp_path))
    assert (tmp_path / system.name / "drive-1" / "macrospin.input").exists()
    assert (tmp_path / system.name / "drive-1" / "info.json").exists()
    assert (tmp_path / system.name / "drive-1" / "job.sh").exists()

    # Schedule header from file and runtime error during schedule.
    with (tmp_path / "header.sh").open("wt", encoding="utf-8") as f:
        f.write("import sys\nsys.exit(1)")
    with pytest.raises(RuntimeError):
        driver.schedule(
            system, "python", str(tmp_path / "header.sh"), dirname=str(tmp_path)
        )
        assert (tmp_path / system.name / "drive-2" / "macrospin.input").exists()
        assert (tmp_path / system.name / "drive-2" / "info.json").exists()
        assert (tmp_path / system.name / "drive-2" / "job.sh").exists()

    assert len(list((tmp_path / system.name).glob("drive*"))) == 3
