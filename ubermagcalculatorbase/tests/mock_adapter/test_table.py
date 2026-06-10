import pytest

from ubermagtable.tests.test_table import *  # noqa: F403

from ubermagcalculatorbase.mock_adapter._output_collecting_util import table_from_file
from ubermagcalculatorbase import mock_adapter
import micromagneticmodel as mm


def _table_energy_minimisation_factory(tmp_path):
    def _inner(*, table_kwargs=None, **kwargs):
        system = mm.examples.macrospin()
        md = mock_adapter.MinDriver()
        md.drive(system, dirname=tmp_path)

        table_kwargs = table_kwargs or {}
        return table_from_file(tmp_path / system.name / "drive-0" / "output.csv", **table_kwargs, **kwargs)

    return _inner

def _table_llg_factory(tmp_path):
    def _inner(*, table_kwargs=None, **kwargs):
        system = mm.examples.macrospin()
        td = mock_adapter.TimeDriver()
        td.drive(system, t=25e-12, n=10, dirname=tmp_path)

        table_kwargs = table_kwargs or {}
        return table_from_file(tmp_path / system.name / "drive-0" / "output.csv", **table_kwargs, **kwargs)

    return _inner


@pytest.fixture
def table_llg_factory(tmp_path):
    """LLG tables."""
    return _table_llg_factory(tmp_path)

@pytest.fixture
def table_minimisation_factory(tmp_path):
    return _table_energy_minimisation_factory(tmp_path)

@pytest.fixture
def table_hysteresis_factory():
    pytest.skip("Hysteresis not implemented.")

@pytest.fixture(params=[_table_energy_minimisation_factory, _table_llg_factory])
def table_factory(request, tmp_path):
    """Energy minimisation or LLG tables."""
    return request.param(tmp_path)

@pytest.fixture
def table_llg_25ps(tmp_path):
    """LLG data with tmax=25ps."""
    return _table_llg_factory(tmp_path)(x="t")
