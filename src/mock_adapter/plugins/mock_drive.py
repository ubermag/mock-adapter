import discretisedfield as df
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
        return (
            f"{self.__class__.__name__}(name='{self.name}', number={self.number}, "
            f"dirname='{self.dirname}', x='{self.x}')"
        )

    def _read_m(self, filename):
        return df.Field.from_file(filename)
