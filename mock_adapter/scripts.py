import mock_adapter
import numpy as np
import micromagneticmodel as mm


def input_script(driver, system, **kwargs):
    settings = _process_energy_equation(system.energy)
    if isinstance(driver, mock_adapter.MinDriver):
        settings["mode"] = "min"
        settings["save_steps"] = getattr(driver, "save_steps", False)
    elif isinstance(driver, mock_adapter.TimeDriver):
        settings["mode"] = "llg"
        settings["t"] = kwargs["t"]
        settings["n"] = kwargs["n"]
        if not hasattr(system.dynamics, "damping"):
            raise ValueError("Dynamics equation must contain damping.")
        if not isinstance(system.dynamics.damping.alpha, (int, float)):
            raise ValueError("Damping does not specify a value for alpha")
        settings["alpha"] = system.dynamics.damping.alpha
    else:
        raise RuntimeError(f"Unsupported driver: {driver!r}")

    return settings


def _process_energy_equation(energy):
    result = {}
    for term in energy:
        if not isinstance(term, mm.Zeeman):
            raise ValueError(f"Energy term {term} not supported.")
        elif "H" in result:
            raise ValueError(f"Only a single Zeeman term is supported, got H={result['H']} and {term}.")
        elif not isinstance(term.H, (list, tuple, np.ndarray) or not np.atleast_1d(term.H).shape == (3,)):
            # TODO: the shape check might not be required as micromagneticmodel.Zeeman
            # may fully cover that.
            raise TypeError(f"Zeeman H must be a single vector of length 3, got {term.H}")
        # convert to a list of builtin.float to allow json serialisation
        # this will also cover all cases where elements of H are of the wrong type
        result["H"] = list(map(float, term.H))
    return result
