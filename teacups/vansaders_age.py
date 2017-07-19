"""
Uses a KDtree to find the nearest point in Jen van Saders' evolutionary
tracks.
"""

import numpy as np
import pandas as pd
import scipy.spatial as sps


def age(query_array):
    """
    Calculate an age from a luminosity, temperature and rotation period.
    Uses a KDtree to find the nearest point in Jen van Saders' evolutionary
    tracks.
    Currently has only solar metallicity.
    To do:
    Use interpolation instead of nearest.

    parameters:
    ----------
    query_array: (array_like)
         The temperature and period of a star.
    returns:
    -------
    age: (float)
        Age in Gyr.
    """
    df = pd.read_csv("skeleton3_run_000.out", skiprows=172)
    m = (3000 < 10**df.log_Teff_K.values) & (10**df.log_Teff_K.values < 8000) & (df.Age_Gyr > .1)
    _teff, _P, _age = 10**df.log_Teff_K.values[m], df.Prot_days.values[m], df.Age_Gyr.values[m]
    data = np.vstack((_teff, _P)).T
    tree = sps.cKDTree(data)
    dist, index = tree.query(query_array, 1)
    return _age[index]


if __name__ == "__main__":
    sun = p[5777, 26]
