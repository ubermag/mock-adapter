import micromagneticdata as mdata


class MockCalculatorDrive(mdata.Drive):
    def __init__(self, name, number, dirname="./", x=None, use_cache=False, **kwargs):
        super().__init__(name, number, dirname, x, use_cache, **kwargs)

    @mdata.AbstractDrive.x.setter
    def x(self, value):
        """Independent variable name.

        Defaults to ``'iteration'`` for drives of a ``MinDriver`` and to ``'t'`` for
        drives of a ``TimeDriver``. Any other column of ``self.table`` can be assigned.

        Parameters
        ----------
        value : str

            Independent variable name.

        Returns
        -------
        str

            Independent variable name.

        Raises
        ------
        ValueError

            If the column name does not exist in table.

        Examples
        --------
        1. Getting and setting the independent variable name.

        >>> import tempfile
        >>> import micromagneticmodel as mm
        >>> import mock_adapter
        ...
        >>> dirname = tempfile.mkdtemp()
        >>> system = mm.examples.macrospin()
        >>> mock_adapter.MinDriver().drive(system, dirname=dirname, verbose=0)
        >>> drive = MockCalculatorDrive(name='macrospin', number=0, dirname=dirname)
        >>> drive.x
        'iteration'
        >>> drive.x = 'mx'
        >>> drive.x
        'mx'

        """
        if value is None:
            if self.info["driver"] == "TimeDriver":
                self._x = "t"
            elif self.info["driver"] == "MinDriver":
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

    # ``property.setter`` keeps the docstring of ``AbstractDrive.x``, so the docstring
    # written above (on the setter function) has to be promoted to the property itself.
    x.__doc__ = x.fset.__doc__

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
