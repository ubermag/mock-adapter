import shlex
import subprocess as sp
import sys

from micromagneticmodel import adapter_base


class MockCalculatorRunner(adapter_base.ExternalRunner):
    @property
    def package_name(self):
        """Name of the calculator.

        This can be an arbitrary string and should be chosen such that it makes sense
        for the user. It will be displayed in the status line of running/completed
        jobs, and is primarily visible inside notebooks.
        """
        return "Ubermag Mock Calculator"

    def _call(self, argstr, need_stderr=False, dry_run=False):
        # This function needs to call the external calculator in a subprocess:
        # `mock_calculator` is a separate package in this repository and can be executed
        # in a subprocess using the same python interpreter as the running ubermag
        # session.
        command = [sys.executable, "-m", "mock_calculator", argstr]

        # `need_stderr` is ignored in this implementation, and stdout and stderr are
        # always captured.
        stdout = stderr = sp.PIPE

        if dry_run:
            return shlex.join(command)
        return sp.run(command, stdout=stdout, stderr=stderr)
