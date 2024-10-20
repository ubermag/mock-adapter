from ubermagcalculatorbase import mock_adapter


def input_script(driver, system, **kwargs):
    settings = {
        "H": system.energy.zeeman.H,
    }
    if isinstance(driver, mock_adapter.MockMinDriver):
        settings["mode"] = "min"
        settings["convergence"] = kwargs.get("convergence", "linear")
        settings["save_steps"] = kwargs.get("save_steps", False)
    elif isinstance(driver, mock_adapter.MockTimeDriver):
        settings["mode"] = "llg"
        settings["t"] = kwargs["t"]
        settings["n"] = kwargs["n"]
        settings["alpha"] = system.dynamics.damping.alpha
    else:
        raise RuntimeError(f"Unsupported driver: {driver!r}")

    return settings
