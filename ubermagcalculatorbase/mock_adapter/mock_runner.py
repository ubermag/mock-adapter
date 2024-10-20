from ubermagcalculatorbase.base import ExternalRunner
import subprocess as sp
import sys
import shlex


class MockRunner(ExternalRunner):
    @property
    def package_name(self):
        return "Ubermag Mock Calculator"

    def _call(self, argstr, need_stderr=False, dry_run=False):
        command = [
            sys.executable,
            "-m",
            "ubermagcalculatorbase.mock_calculator",
            argstr
        ]

        stdout = stderr = sp.PIPE

        if dry_run:
            return shlex.join(command)
        return sp.run(command, stdout=stdout, stderr=stderr)
