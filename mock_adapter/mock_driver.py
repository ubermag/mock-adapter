import json
import pathlib
import discretisedfield as df
from micromagneticmodel import adapter_base

import mock_adapter
from mock_adapter.plugins import table_from_file


class _Driver(adapter_base.ExternalDriver):
    def _inputfilename(self, system):
        return f"{system.name}.input.json"

    def _write_input_files(self, system, **kwargs):
        with open(self._inputfilename(system), "w", encoding="utf-8") as f:
            json.dump(mock_adapter.scripts.input_script(self, system, **kwargs), f, indent=4)

        system.m.to_file('m0.hdf5')

    def _call(self, system, runner, verbose=1, **kwargs):
        if runner is None:
            runner = mock_adapter.mock_runner.MockCalculatorRunner()
        runner.call(
            argstr=self._inputfilename(system),
            verbose=verbose,
            total=kwargs.get("n"),
            glob_name=f"{system.name}*.omf",
        )

    def _schedule_commands(self, system, runner):
        # Python is used to test/simulate schedule during tests because there
        # typically is no scheduling system and Python is always available.
        # Therefore, we return a Python comment that can be added to the
        # schedule script without breaking the execution.
        if runner is None:
            runner = mock_adapter.MockCalculatorRunner()
        return [
            "# calculator-specific setup, e.g. setting environment variables",
            "# " + runner._call(argstr=self._inputfilename(system), dry_run=True),
        ]

    def _read_data(self, system):
        output_files = pathlib.Path(".").glob("m_*.hdf5")
        last_outpup_file = sorted(output_files)[-1]
        # pass Field.array instead of Field to system.m.value
        # - to avoid overriding component labels
        # - to avoid overriding subregions
        # - for better performance
        system.m.array = df.Field.from_file(str(last_outpup_file)).array

        # update table information
        system.table = table_from_file("output.csv", x=self._x)


class MinDriver(_Driver):
    """Energy minimisation with mock_calculator.

    mock_calculator takes a single energy term Zeeman with uniform field direction and
    rotates the initial magnetisation to that field direction in 10 steps.

    Parameters
    ----------

    save_steps : bool, default: False

        If set to True intermediate steps 1-9 of the energy minimisation are saved.
        If False only the final step 10 is saved.
    """
    _allowed_attributes = [
        "save_steps",  # possible values: true, false [default]
    ]

    def schedule_kwargs_setup(self, schedule_kwargs):
        """MinDriver takes no special keyword arguments."""
        pass

    def drive_kwargs_setup(self, drive_kwargs):
        """MinDriver takes no special keyword arguments."""
        pass

    def _check_system(self, system):
        """Check that system.energy is defined."""
        if len(system.energy) == 0:
            raise RuntimeError("System's energy is not defined")

    @property
    def _x(self):
        return "iteration"


class TimeDriver(_Driver):
    """Time integration with mock_calculator.

    For time integration with mock_calculator damping is required and controls the
    speed of relaxation. A precession term in the dynamics equation is ignored; instead
    precession is hard-coded with period 1ns.
    """
    _allowed_attributes = []

    def schedule_kwargs_setup(self, schedule_kwargs):
        """Additional keyword arguments for time drive.

        Parameters
        ----------
        t : int, float

            The end time of the time integration in seconds. Must be positive.

        n : int

            The number of steps to save during time integration. The first step is
            saved at t/n, the last step at t. Must be positive.

        """
        self._checkargs(schedule_kwargs)

    def drive_kwargs_setup(self, drive_kwargs):
        """Additional keyword arguments for time drive.

        Parameters
        ----------
        t : int, float

            The end time of the time integration in seconds. Must be positive.

        n : int

            The number of steps to save during time integration. The first step is
            saved at t/n, the last step at t. Must be positive.

        """
        self._checkargs(drive_kwargs)

    def _checkargs(self, kwargs):
        t, n = kwargs["t"], kwargs["n"]
        if t <= 0:
            msg = f"Cannot drive with {t=}."
            raise ValueError(msg)
        if not isinstance(n, int):
            msg = f"Cannot drive with {type(n)=}."
            raise ValueError(msg)
        if n <= 0:
            msg = f"Cannot drive with {n=}."
            raise ValueError(msg)

    def _check_system(self, system):
        """Check that system.energy and system.dynamics are non-empty."""
        if len(system.dynamics) == 0:
            raise RuntimeError("System's dynamics is not defined")
        if len(system.energy) == 0:
            raise RuntimeError("System's energy is not defined")

    @property
    def _x(self):
        return "t"
