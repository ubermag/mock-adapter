"""Plugins for micromagneticdata.

This submodule defines plugins for micromagneticdata:

- `MockCalculatorDrive` is used to read a drive on disk
- `table_from_file` is used to read tabular data and return `drive.table`
"""

from .mock_drive import MockCalculatorDrive as MockCalculatorDrive
from .read_table import table_from_file as table_from_file
