import micromagneticdata as mdata
import micromagneticmodel as mm
import pytest
from micromagneticdata.testing.drive import *  # noqa: F403

import mock_adapter


@pytest.fixture(scope="session", params=["min_drive", "min_drive_steps", "time_drive"])
def _compute_drive(tmp_path_factory, request):
    system = mm.examples.macrospin()
    dirname = tmp_path_factory.mktemp(request.param)

    if request.param == "min_drive":
        md = mock_adapter.MinDriver()
        md.drive(system, dirname=dirname)
        reference = ("iteration", "mx", '"save_steps": false')
    elif request.param == "min_drive_steps":
        md = mock_adapter.MinDriver(save_steps=True)
        md.drive(system, dirname=dirname)
        reference = ("iteration", "mx", '"save_steps": true')
    elif request.param == "time_drive":
        td = mock_adapter.TimeDriver()
        td.drive(system, dirname=dirname, t=1e-9, n=10)
        reference = ("t", "mx", '"mode": "llg"')
    else:
        raise NotImplementedError(request.param)

    return system.name, system.drive_number - 1, dirname, reference


@pytest.fixture
def drive_with_reference(_compute_drive):
    name, number, dirname, reference = _compute_drive
    return mdata.Drive(name, number, dirname), reference


@pytest.fixture
def drive(_compute_drive):
    name, number, dirname, _ = _compute_drive
    return mdata.Drive(name, number, dirname)
