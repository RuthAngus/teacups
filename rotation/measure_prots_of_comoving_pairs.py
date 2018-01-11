# A script for measuring the rotation periods of the comoving pairs.

# 1. Identify comoving stars and download light curves if they are not already
# on file.

# 2. Measure the LS periodogram rotation periods of all stars.

# 3. Look at the light curve with your eyes and figure out whether you believe
# the LS period.

# 4. If you do believe it, run MCMC with Celerite and GProtation.
# If the rotational signal looks small run the MCMC for a long time with a
# large number of data points.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rotation as ro

import kepler_data as kd
import kplr
client = kplr.API()


def download_all_light_curves():
    """
    Download all the light curves for the comoving pair candidates.
    """
    data = pd.read_csv("../data/targets-small-sep.csv")
    for i, kepid in enumerate(data.kepid.values):
        print(kepid, i, "of", len(data.kepid.values))
        star = client.star(kepid)
        star.get_light_curves(fetch=True, short_cadence=False, clobber=False)


def measure_LS_period():
    data = pd.read_csv("../data/targets-small-sep.csv")
    for i, kepid in enumerate(data.kepid.values[10:50]):
        lc_dir = "/Users/ruthangus/.kplr/data/lightcurves/{}"\
            .format(str(kepid).zfill(9))
        x, y, yerr = kd.load_kepler_data(lc_dir)

        prot = ro.prot(kepid, x, y, yerr)
        prot.pgram_ps(plot=True)


if __name__ == "__main__":
    # download_all_light_curves()
    measure_LS_period()
