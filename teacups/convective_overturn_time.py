# Calculate the convective overturn times for all the binary stars.
# First Calculate V-Ks using isochrones.
# Then calculate tau using Wright et al. 2011.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import isochrones
from isochrones.mist import MIST_Isochrone
mist = MIST_Isochrone()
from isochrones import StarModel

s1 = pd.read_csv("star1_kic_1.csv")
teff = s1.teff.values
teff_err = s1.teff_err1.values
feh_err = s1.feh_err1.values
parallax = s1.parallax.values
parallax_err = s1.parallax_error.values
logg = s1.logg.values
logg_err = s1.logg_err1.values
feh = s1.feh.values
mass = s1.mass.values
radius = s1.radius.values
kepmag = s1.kepmag.values
jmag = s1.jmag.values
hmag = s1.hmag.values
kmag = s1.kmag.values

mod = StarModel(mist, Teff=(s1.teff.values[0], s1.teff.values[0]),
                logg=(s1.logg.values[0], s1.logg_err1.values[0]),
                feh=(s1.feh.values[0], s1.feh_err1.values[0]),
                J=s1.jmag.values[0], K=s1.kmag.values[0], H=s1.hmag.values[0],
                Kp=s1.kepmag.values[0],
                parallax=(s1.parallax.values[0], s1.parallax_err.values[0]),
                use_emcee=True)
mod.fit()

VK = np.median(mod.samples.V_mag) - np.median(mod.samples.K_mag)
