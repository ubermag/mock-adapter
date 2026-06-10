"""This script mimics a micromagnetic calculator such as OOMMF or Mumax3.

NOTE: THIS SCRIPT PRODUCES FAKE DATE AND DOES NOT RUN REAL MICROMAGNETIC SIMULATIONS

Two different simulation modes are supported: 'min' and 'llg'.
"""
import discretisedfield as df
from scipy.spatial.transform import Rotation
from pathlib import Path
import json
import sys
import math


TABLE_NAME = "output.csv"


def read_config(path) -> dict:
    with open(path) as f:
        return json.load(f)


def init_table(path, iteration_name, iteration_unit, extra_columns='', extra_column_units=''):
    with open(path / TABLE_NAME, "w") as f:
        f.write(f"{iteration_name},energy,mx,my,mz{extra_columns}\n")
        f.write(f"{iteration_unit},J,,,{extra_column_units}\n")


def update_table(path, iteration, energy, m, *extra_columns):
    data = [iteration, energy, float(m.x.mean()), float(m.y.mean()), float(m.z.mean()), *extra_columns]
    with open(path / TABLE_NAME, "a") as f:
        f.write(','.join(map(str, data)) + "\n")


def fake_min(config, path):
    print("Starting energy minimisation")
    init_table(path, "iteration", "")
    m = df.Field.from_file(path / 'm0.hdf5')
    H = df.Field(mesh=m.mesh, nvdim=3, value=config['H'])
    if config['save_steps']:
        print("Saving enery minimsation steps")
        angles = m.angle(H)
        for i in range(1, 10):
            factor = i / 10
            angle = angles * factor
            rot_field = df.Field(m.mesh, nvdim=3, value=m.cross(H).array, norm=angle)
            r = Rotation.from_rotvec(rot_field.array.reshape((-1, 3)))
            m_new_array = r.apply(m.array.reshape((-1, 3)))
            m_new = df.Field(m.mesh, nvdim=3, value=m_new_array.reshape((*m.mesh.n, 3)), norm=m.norm)
            m_new.to_file(path / f'm_{i:06}.hdf5')
            update_table(path, i, -1e-10 * i, m_new.orientation)
            print(f"Step {i} finished")

    m_final = m.norm * H.orientation
    m_final.to_file(path / 'm_000010.hdf5')
    update_table(path, 10, -1e-9 , m_final.orientation)
    print("Final magnetisation saved")


def fake_llg(config, path):
    print("Starting llg")
    init_table(path, "t", "s", ",alpha_factor,precession_angle", ",,")
    t = config['t']
    n = config['n']
    dt = t / n
    m = df.Field.from_file(path / 'm0.hdf5')
    H = df.Field(mesh=m.mesh, nvdim=3, value=config['H'])
    precession_period = 1e-9  # s
    damping_angles = H.angle(m)
    for i in range(1, n+1):
        # We rotate the external field direction in the directon of the current
        # magnetic field (and renormalise to Ms) with the amount of rotation given by
        # alpha_factor; the deviation between m and H decreases as a sigmoid function,
        # alpha can be used to control the damping strength.
        #
        # This scheme has been chosen because it prodives fast initial damping
        # and slows down as we approach the final state and the algorithm is independent
        # of the rate at which data is saved.
        alpha_factor = 2 - 2 / (1 + math.exp(-i * dt / 1e-9 * config['alpha']))
        damping_angle = damping_angles * alpha_factor
        damping_rot_field = df.Field(m.mesh, nvdim=3, value=H.cross(m).array, norm=damping_angle)
        damping_r = Rotation.from_rotvec(damping_rot_field.array.reshape((-1, 3)))
        m_new_array = damping_r.apply(H.array.reshape((-1, 3)))

        precession_angle = dt / precession_period * 2*math.pi
        precession_rot_field = df.Field(m.mesh, nvdim=3, value=H.array, norm=precession_angle)
        precession_r = Rotation.from_rotvec(precession_rot_field.array.reshape((-1, 3)))
        m_new_array = precession_r.apply(m_new_array)

        m.array = m_new_array.reshape((*m.mesh.n, 3))
        m.to_file(path / f'm_{i:06}.hdf5')
        update_table(path, i*dt, -1e-10 * i, m.orientation, alpha_factor, precession_angle)
        print(f"Step {i} finished")


def main():
    assert len(sys.argv) == 2
    path = Path(sys.argv[1]).absolute()
    print("Running simulation for", path)
    config = read_config(path)
    if config['mode'] == 'min':
        fake_min(config, path.parent)
    elif config['mode'] == 'llg':
        fake_llg(config, path.parent)
    else:
        raise RuntimeError(f"Mode {config['mode']} not supported. Use 'min' or 'llg'.")
    print("Simulation finished; terminating")


if __name__ == '__main__':
    main()
