import micromagneticdata as mdata


class MockCalculatorDrive(mdata.Drive):
    def __init__(self, name, number, dirname="./", x=None, use_cache=False, **kwargs):
        print("we hare here")
        super().__init__(name, number, dirname, x, use_cache, **kwargs)

    @mdata.AbstractDrive.x.setter
    def x(self, value):
        if value is None:
            if self.info["driver"] == "MockTimeDriver":
                self._x = "t"
            elif self.info["driver"] == "MockMinDriver":
                self._x = "iteration"
        else:
            # self.table reads self.x so self._x has to be defined first
            if hasattr(self, "_x"):
                # store old value to reset in case value is invalid
                _x = self._x
            self._x = value
            if value not in self.table.data.columns:
                self._x = _x
                raise ValueError(f"Column {value=} does not exist in data.")

    @property
    def _table_path(self):
        return self.drive_path / f"output.csv"

    @property
    def _step_file_glob(self):
        return self.drive_path.glob(f"m_*.hdf5")

    @property
    def _m0_path(self):
        return self.drive_path / "m0.hdf5"

    @property
    def calculator_script(self):
        with (self.drive_path / f"{self.name}.input.json").open() as f:
            return f.read()

    def __repr__(self):
        """Representation string.
        Returns
        -------
        str
            Representation string.
        Examples
        --------
        1. Representation string.
        >>> import os
        >>> import micromagneticdata as md
        ...
        >>> dirname = dirname=os.path.join(os.path.dirname(__file__),
        ...                                'tests', 'test_sample')
        >>> drive = md.Drive(name='system_name', number=0, dirname=dirname)
        >>> drive
        OOMMFDrive(name='system_name', number=0, dirname='...test_sample', x='t')
        """
        return (
            f"{self.__class__.__name__}(name='{self.name}', number={self.number}, "
            f"dirname='{self.dirname}', x='{self.x}')"
        )
