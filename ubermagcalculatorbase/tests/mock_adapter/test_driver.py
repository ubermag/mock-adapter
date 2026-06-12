from ubermagcalculatorbase import mock_adapter
import numpy as np
import sys

def test_min_drive(system, tmp_path):
    md = mock_adapter.MinDriver()
    md.drive(system, dirname=tmp_path)

    ref = np.zeros((2, 2, 2, 3))
    ref[..., 2] = 1e5
    np.testing.assert_allclose(system.m.array, ref)

    assert len(system.table.data) == 1
    assert system.table.xmax == 10


def test_min_drive_save_steps(system, tmp_path):
    md = mock_adapter.MinDriver(save_steps=True)
    md.drive(system, dirname=tmp_path)

    assert len(system.table.data) == 10
    assert system.table.xmax == 10


def test_time_drive(system, tmp_path):
    td = mock_adapter.TimeDriver()
    td.drive(system, t=20e-9, n=5, dirname=tmp_path)

    ref = np.zeros((2, 2, 2, 3))
    ref[..., 2] = 1
    np.testing.assert_allclose(system.m.orientation.array, ref, atol=1e-8)
    np.testing.assert_allclose(system.m.norm.array, 1e5)

    assert len(system.table.data) == 5
    assert system.table.xmax == 20e-9


def test_min_schedule(system, tmp_path):
    md = mock_adapter.MinDriver()
    md.schedule(system, dirname=tmp_path, cmd="python", header="#SBATCH --time 1:00")

    job_script = (tmp_path / system.name / "drive-0" / "job.sh").read_text()
    assert f"{sys.executable} -m ubermagcalculatorbase.mock_calculator {system.name}.input.json" in job_script

    assert '"mode": "min"' in (tmp_path / system.name / "drive-0" / "test.input.json").read_text()

def test_time_schedule(system, tmp_path):
    td = mock_adapter.TimeDriver()
    td.schedule(system, t=25e-12, n=10, dirname=tmp_path, cmd="python", header="#SBATCH --time 1:00")

    job_script = (tmp_path / system.name / "drive-0" / "job.sh").read_text()
    assert f"{sys.executable} -m ubermagcalculatorbase.mock_calculator {system.name}.input.json" in job_script

    assert '"mode": "llg"' in (tmp_path / system.name / "drive-0" / "test.input.json").read_text()
