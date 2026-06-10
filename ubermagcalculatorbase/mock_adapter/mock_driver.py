import json
import pathlib
import discretisedfield as df
import micromagneticmodel as mm
import abc

from ubermagcalculatorbase.base import ExternalDriver
from ubermagcalculatorbase import mock_adapter


class Driver(ExternalDriver):

    @abc.abstractmethod
    def _checkargs(self, kwargs):
        pass

    def schedule_kwargs_setup(self, schedule_kwargs):
        self._checkargs(schedule_kwargs)

    def drive_kwargs_setup(self, drive_kwargs):
        self._checkargs(drive_kwargs)

    def _inputfilename(self, system):
        return f"{system.name}.input.json"

    def _write_input_files(self, system, **kwargs):
        with open(self._inputfilename(system), "w", encoding="utf-8") as f:
            json.dump(mock_adapter.input_script(self, system, **kwargs), f, indent=4)

        system.m.to_file('m0.hdf5')
        self._write_info_json(system, **kwargs)

    def _call(self, system, runner, verbose=1, **kwargs):
        if runner is None:
            runner = mock_adapter.mock_runner.MockRunner()
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
        return ["# run command line"]

    def _read_data(self, system):
        output_files = pathlib.Path(".").glob("m_*.hdf5")
        last_outpup_file = sorted(output_files)[-1]
        # pass Field.array instead of Field to system.m.value
        # - to avoid overriding component labels
        # - to avoid overriding subregions
        # - for better performance
        system.m.array = df.Field.from_file(str(last_outpup_file)).array

        # TODO: update table information
        # system.table = ut.Table.fromfile(f"{system.name}.odt", x=self._x)


class MinDriver(Driver):
    _allowed_attributes = [
        "convergence_mode",  # possible values: lin [default], log
        "save_steps",  # possible values: true, false [default]
    ]

    def _checkargs(self, kwargs):
        pass  # no kwargs should be checked


    def _check_system(self, system):
        """Checks the system has energy in it"""
        if len(system.energy) == 0:
            raise RuntimeError("System's energy is not defined")
        if not any(isinstance(term, mm.Zeeman) for term in system.energy):
            raise RuntimeError("Zeeman energy must be defined")

    @property
    def _x(self):
        return "iteration"


class TimeDriver(Driver):
    _allowed_attributes = []

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
        """Checks the system has dynamics in it"""
        if len(system.dynamics) == 0:
            raise RuntimeError("System's dynamics is not defined")
        if len(system.energy) == 0:
            raise RuntimeError("System's energy is not defined")
        if not any(isinstance(term, mm.Zeeman) for term in system.energy):
            raise RuntimeError("Zeeman energy must be defined")

    @property
    def _x(self):
        return "t"
