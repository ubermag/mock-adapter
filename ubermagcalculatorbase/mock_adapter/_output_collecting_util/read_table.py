import pandas as pd
import ubermagtable


def table_from_file(filename, /, x=None, rename=True):
    data = pd.read_csv(filename, skiprows=[1])
    with open(filename) as f:
        columns = f.readline().strip().split(",")
        units = f.readline().strip().split(",")

    return ubermagtable.Table(data=data, units=dict(zip(columns, units)), x=x)
