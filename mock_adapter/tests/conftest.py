import discretisedfield as df
import micromagneticmodel as mm
import pytest


@pytest.fixture
def system():
    system = mm.System(name="test")
    system.energy = mm.Zeeman(H=[0, 0, 1])
    system.m = df.Field(
        mesh=df.Mesh(p1=(0, 0, 0), p2=(10, 10, 10), n=(2, 2, 2)),
        nvdim=3,
        value=[1, 0, 0],
        norm=1e5,
    )
    system.dynamics = mm.Damping(alpha=1)
    return system
