import micromagneticmodel as mm


class Evolver(mm.abstract.Abstract):
    """An abstract class for deriving evolvers.

    An evolver can be used to control numerical details of the simulation, e.g. the type
    of gradient decent for energy minimisation or properties of the time integration.

    Not all calculators provide extensive control over such parameters and implementing
    evolvers in an adapter package is therefore optional. In simple cases it can be
    easier to allow passing additional keyword arguments to the `Driver.drive` and
    `Driver.schedule` method and to validate them in `Driver.drive_kwarg_setup` and
    `Driver.schedule_kwarg_setup`.
    """

    pass
