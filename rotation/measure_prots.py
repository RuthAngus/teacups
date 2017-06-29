"""
This is the wrapper for measuring rotation periods using GPs, periodograms
and ACFs
"""


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from kepler_data import load_kepler_data
from gatspy.periodic import LombScargle
from filtering import butter_bandpass, butter_bandpass_filter


def GP_rot(kepid, RESULTS_DIR="results"):
    """
    Measure a GP rotation period.
    params:
    ------
    kepid: (str)
        The KIC id.
    returns:
    --------
    samples: (3d array)
        The period posterior samples.
    """
    fn = os.path.join(RESULTS_DIR, "KIC-{}.h5".format(int(kepid)))
    if not os.path.exists(fn):
        subprocess.call("gprot-fit {} --kepler -v".format(kepid), shell=True)
    df = pd.read_hdf(fn, key="samples")
    samps = np.exp(df.ln_period.values)
    period = np.median(samps)
    upper = np.percentile(samps, 84)
    lower = np.percentile(samps, 16)
    errp = upper - period
    errm = period - lower
    return period, errp, errm

def pgram_ps(x, y, yerr):
    """
    Measure a periodogram rotation period
    x: (array)
        The time array.
    y: (array)
        The flux array.
    yerr: (array)
        The flux uncertainties.
    returns:
    -------
    pgram_period: (float)
        The rotation period
    pgram_period_err: (float)
        The formal uncertainty on the period.
    """
    ps = np.arange(.1, 100, .1)
    model = LombScargle().fit(x, y, yerr)
    pgram = model.periodogram(ps)

    period = 35.  # days
    fs = 1./(x[1] - x[0])
    lowcut = 1./period
    yfilt = butter_bandpass_filter(y, lowcut, fs, order=3, plot=False)

    med = np.median(y)
    y -= med
    var = np.std(y)
    y /= var

    print("Calculating periodogram")
    ps = np.arange(.1, 100, .1)
    model = LombScargle().fit(x, yfilt, yerr)
    pgram = model.periodogram(ps)

    peaks = np.array([i for i in range(1, len(ps)-1) if pgram[i-1] <
                        pgram[i] and pgram[i+1] < pgram[i]])
    pgram_period = ps[pgram == max(pgram[peaks])][0]

    # Calculate the uncertainty.
    _freq = 1./pgram_period
    pgram_freq_err = calc_pgram_uncertainty(x, y, _freq)
    frac_err = pgram_freq_err/_freq
    pgram_period_err = pgram_period * frac_err
    return pgram_period, pgram_period_err


def calc_pgram_uncertainty(x, y, freq):
    phase, A = calc_phase_and_amp(x, y, freq)
    y_noise = y - A**2*np.sin(2*np.pi*freq*x + phase)
    sigma_n = np.var(y_noise)
    N, T = len(x), x[-1] - x[0]
    return 3 * np.pi * sigma_n / (2 * N**.5 * T * A)


def calc_phase_and_amp(x, y, f):
    AT = np.vstack((x, np.ones((3, len(y)))))
    ATA = np.dot(AT, AT.T)
    arg = 2*np.pi*f*x
    AT[-2, :] = np.sin(arg)
    AT[-1, :] = np.cos(arg)
    v = np.dot(AT[:-2, :], AT[-2:, :].T)
    ATA[:-2, -2:] = v
    ATA[-2:, :-2] = v.T
    ATA[-2:, -2:] = np.dot(AT[-2:, :], AT[-2:, :].T)
    w = np.linalg.solve(ATA, np.dot(AT, y))
    A, B = w[-1], w[-2]
    phase = np.arctan(A/B)
    Amp = (np.abs(A) + np.abs(B))**.5
    return phase, Amp


def ACF_period(x, y, yerr):
    """
    Measure an ACF rotation period
    x: (array)
        The time array.
    y: (array)
        The flux array.
    yerr: (array)
        The flux uncertainties.
    returns:
    -------
    period: (float)
        The rotation period
    """


def gp_prots(kepid_list):
    """
    Takes a list of kepler ids and returns rotation periods.
    """
    gp_period, gp_errp, gp_errm = [np.zeros(len(kepid_list)) for i in
                                   range(3)]
    for i, kepid in enumerate(kepid_list):
        print(kepid, i, "of", len(kepid_list))
        gp_period[i], gp_errp[i], gp_errm[i] = GP_rot(kepid)
    return gp_period, gp_errp, gp_errm


def pgram_prots(kepid_list, LC_DIR="/Users/ruthangus/.kplr/data/lightcurves"):
    pgram_period, err = [np.zeros(len(kepid_list)) for i in range(2)]
    for i, kepid in enumerate(kepid_list):
        print(kepid, i, "of", len(kepid_list))
        x, y, yerr = load_kepler_data(os.path.join(LC_DIR, "{}".
                                                format(str(kepid).zfill(9))))
        pgram_period[i], err[i] = pgram_ps(x, y, yerr)
    return pgram_period, err


if __name__ == "__main__":

    DATA_DIR = "data"

    # Load list of targets (kepids)
    df = pd.read_csv(os.path.join(DATA_DIR, "targets-small-sep.csv"))
    kepid_list = df.kepid.values[:3]

    # loop over kepids and measure their rotation periods.
    gp_period, gp_errp, gp_errm = gp_prots(kepid_list)
    pgram_period, pgram_err = pgram_prots(kepid_list)

    # save the rotation periods.
    df = pd.DataFrame({"kepid": kepid_list, "gp_period": gp_period, "gp_errp":
                       gp_errp, "gp_errm": gp_errm, "pgram_period":
                       pgram_period, "pgram_err": pgram_err})
    df.to_csv("targets-small-sep_periods.csv")