import micromagneticmodel as mm
import pytest
from ubermagtable.testing.table import *  # noqa: F403

import mock_adapter
from mock_adapter.plugins import table_from_file


@pytest.fixture(scope="session")
def min_drive(tmp_path_factory):
    dirname = tmp_path_factory.mktemp("min_drive")
    # in this implementation we compute table data on the fly; for more expensive
    # calculations pre-computed test samples can be committed
    system = mm.examples.macrospin()
    md = mock_adapter.MinDriver()
    md.drive(system, dirname=dirname)
    return dirname, system.name


@pytest.fixture(scope="session")
def time_drive(tmp_path_factory):
    dirname = tmp_path_factory.mktemp("min_drive")
    system = mm.examples.macrospin()
    td = mock_adapter.TimeDriver()
    td.drive(system, t=25e-12, n=10, dirname=dirname)
    return dirname, system.name


def _table_factory(dirname, name):
    def _inner(**kwargs):
        return table_from_file(dirname / name / "drive-0" / "output.csv", **kwargs)

    return _inner


@pytest.fixture
def table_llg_factory(time_drive):
    """LLG tables."""
    dirname, name = time_drive
    return _table_factory(dirname, name)


@pytest.fixture
def table_minimisation_factory(min_drive):
    dirname, name = min_drive
    return _table_factory(dirname, name)


@pytest.fixture
def table_hysteresis_factory():
    pytest.skip("Hysteresis not implemented.")


@pytest.fixture(params=["table_minimisation_factory", "table_llg_factory"])
def table_factory(request):
    """Energy minimisation or LLG tables."""
    return request.getfixturevalue(request.param)


@pytest.fixture
def table_llg_25ps(table_llg_factory):
    """LLG data with tmax=25ps."""
    # In this implementation we only have a single LLG example with tmax = 25ps. Adapter
    # packages can provide additional other samples.
    return table_llg_factory(x="t")
