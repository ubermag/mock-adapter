import micromagneticdata as mdata


class MockCalculatorDrive(mdata.Drive):
    def __init__(self, name, number, dirname="./", x=None, use_cache=False, **kwargs):
        super().__init__(name, number, dirname, x, use_cache, **kwargs)

    @property
    def _default_x(self):
        return {"TimeDriver": "t", "MinDriver": "iteration"}[self.info["driver"]]

    @property
    def _table_path(self):
        return self.drive_path / "output.csv"

    @property
    def _step_file_glob(self):
        return self.drive_path.glob("m_*.hdf5")

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

        >>> import tempfile
        >>> import micromagneticmodel as mm
        >>> import mock_adapter
        ...
        >>> dirname = tempfile.mkdtemp()
        >>> system = mm.examples.macrospin()
        >>> mock_adapter.MinDriver().drive(system, dirname=dirname, verbose=0)
        >>> MockCalculatorDrive(name='macrospin', number=0, dirname=dirname)
        ... # doctest: +ELLIPSIS
        MockCalculatorDrive(name='macrospin', number=0, dirname='...', x='iteration')

        """
        return (
            f"{self.__class__.__name__}(name='{self.name}', number={self.number}, "
            f"dirname='{self.dirname}', x='{self.x}')"
        )
