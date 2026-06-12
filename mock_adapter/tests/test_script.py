import micromagneticmodel as mm
import pytest

import mock_adapter
from mock_adapter.scripts import input_script


def test_script_min(system):
    script = input_script(mock_adapter.MinDriver(), system)
    assert isinstance(script, dict)

    assert script["mode"] == "min"
    assert not script["save_steps"]
    assert script["H"] == [0, 0, 1]

    assert "alpha" not in script


def test_script_min_save_steps(system):
    script = input_script(mock_adapter.MinDriver(save_steps=True), system)
    assert isinstance(script, dict)

    assert script["mode"] == "min"
    assert script["save_steps"]


def test_script_wrong_energy_term(system):
    system.energy += mm.Exchange(A=1e-12)
    with pytest.raises(ValueError, match="Energy term Exchange.* not supported."):
        input_script(mock_adapter.MinDriver(), system)


def test_script_zeeman_H_wrong_type(system):
    system.energy.zeeman.H = {"left": [0, 0, 1], "right": [1, 0, 0]}
    with pytest.raises(TypeError, match="Zeeman H must be a single vector.*"):
        input_script(mock_adapter.MinDriver(), system)


def test_script_multiple_zeeman_terms(system):
    system.energy += mm.Zeeman(name="second", H=[1, 0, 0])
    with pytest.raises(ValueError, match="Only a single Zeeman term is supported.*"):
        input_script(mock_adapter.MinDriver(), system)


def test_script_llg(system):
    script = input_script(mock_adapter.TimeDriver(), system, t=1e-9, n=5)
    assert isinstance(script, dict)

    assert script["mode"] == "llg"
    assert script["H"] == [0, 0, 1]
    assert script["alpha"] == 1


def test_script_llg_no_damping(system):
    system.dynamics = mm.Precession()  # overwrite dynamics equation
    print(system.dynamics)
    with pytest.raises(ValueError, match="Dynamics equation must contain damping."):
        input_script(mock_adapter.TimeDriver(), system, t=1e-9, n=1)


def test_script_llg_damping_no_alpha(system):
    system.dynamics = mm.Damping()  # damping without alpha -> type system Parameter
    print(system.dynamics.damping.alpha)
    with pytest.raises(ValueError, match="Damping does not specify a value for alpha"):
        input_script(mock_adapter.TimeDriver(), system, t=1e-9, n=1)


def test_script_wrong_driver(system):
    with pytest.raises(RuntimeError, match="Unsupported driver.*"):
        input_script("not a driver", system)
