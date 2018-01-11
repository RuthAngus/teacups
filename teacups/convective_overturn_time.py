# Calculate the convective overturn times for all the binary stars.
# First Calculate V-Ks using isochrones.
# Then calculate tau using Wright et al. 2011.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import isochrones
from isochrones.mist import MIST_Isochrone
from isochrones.dartmouth import DartmouthModelGrid
mist = MIST_Isochrone()
g_dar = DartmouthModelGrid(['g','r','i','J','H','K'])
from isochrones import StarModel


def calculate_V_minus_K(s, i, dartmouth=False):
    """
    Using the isochrones package, calculate the V-K color of a star using data
    from the KIC. Takes a pandas dataframe and the index of the star in the
    dataframe. Returns V-K for that star.
    """
    if dartmouth:
        grid = g_dar
    else:
        grid = mist
    mod = StarModel(grid, Teff=(s.teff.values[i], s.teff.values[i]),
                    logg=(s.logg.values[i], s.logg_err1.values[i]),
                    feh=(s.feh.values[i], s.feh_err1.values[i]),
                    J=s.jmag.values[i], K=s.kmag.values[i], H=s.hmag.values[i],
                    Kp=s.kepmag.values[i],
                    parallax=(s.parallax.values[i],
                              s.parallax_error.values[i]),
                    use_emcee=True)
    mod.fit()
    if dartmouth:
        return np.median(mod.samples.V_mag) - np.median(mod.samples.Ks_mag)
    else:
        return np.median(mod.samples.V_mag) - np.median(mod.samples.K_mag)


def convective_overturn_time(VKs):
    """
    Calculate the convective overturn time based on the wright 2011 relation.
    """
    if VKs < 3.5:
        return 0.73 + 0.22 * VKs
    else:
        return -2.16 + 1.50 * VKs - 0.13 * VKs**2


if __name__ == "__main__":
    s1 = pd.read_csv("star1_kic_1.csv")
    s2 = pd.read_csv("star2_kic_1.csv")
    VKs1 = calculate_V_minus_K(s1, 0)
    VKs2 = calculate_V_minus_K(s2, 0)

    print("tau = ", convective_overturn_time(VKs1))
    print("tau = ", convective_overturn_time(VKs2))
