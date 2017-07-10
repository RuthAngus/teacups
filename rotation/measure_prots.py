"""
This is the wrapper for measuring rotation periods using GPs, periodograms
and ACFs
"""


import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from kepler_data import load_kepler_data
# from gatspy.periodic import LombScargle
from astropy.stats import LombScargle
from filtering import butter_bandpass, butter_bandpass_filter
import kplr
client = kplr.API()


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
    subprocess.call("gprot-fit {} --kepler -v".format(kepid), shell=True)
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

def pgram_ps(x, y, yerr, kepid, plot=False):
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

    fname = "results/{}_pgram.csv".format(kepid)
    if os.path.exists(fname):
        pr = pd.read_csv(fname)
        ps, pgram = pr.periods.values, pr.power.values

    else:
        ps = np.arange(.1, 100, .1)
        freq = 1./ps
        # model = LombScargle().fit(x, y, yerr)
        # pgram = model.periodogram(ps)

        pgram = LombScargle(x, y, yerr).power(freq)

        period = 35.  # days
        fs = 1./(x[1] - x[0])
        lowcut = 1./period
        yfilt = butter_bandpass_filter(y, lowcut, fs, order=3, plot=False)

        med = np.median(y)
        y -= med
        var = np.std(y)
        y /= var

        print("Calculating periodogram")
        pgram = LombScargle(x, y, yerr).power(freq)

        peaks = np.array([i for i in range(1, len(ps)-1) if pgram[i-1] <
                            pgram[i] and pgram[i+1] < pgram[i]])

        presults = pd.DataFrame({"periods": ps, "power": pgram})
        presults.to_csv("results/{}_pgram.csv".format(kepid))

    pgram_period = ps[pgram == max(pgram[peaks])][0]
    if plot:
        plt.clf()
        plt.plot(ps, pgram)
        plt.axvline(pgram_period, color="r")
        plt.savefig("results/{}".format(kepid))

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


def pgram_prots(kepid_list, LC_DIR="/Users/ruthangus/.kplr/data/lightcurves",
                plot=False):
    pgram_period, err = [np.zeros(len(kepid_list)) for i in range(2)]
    for i, kepid in enumerate(kepid_list):
        print(kepid, i, "of", len(kepid_list))
        try:
            x, y, yerr = load_kepler_data(os.path.join(LC_DIR, "{}".
                                                    format(str(kepid).
                                                           zfill(9))))
        except IndexError:
            star = client.star(kepid)
            star.get_light_curves(fetch=True, short_cadence=False)
        pgram_period[i], err[i] = pgram_ps(x, y, yerr, kepid, plot=plot)
    return pgram_period, err


def get_period_from_pgram(ps, pgram, x, y, yerr):
    peaks = np.array([i for i in range(1, len(ps)-1) if pgram[i-1] <
                        pgram[i] and pgram[i+1] < pgram[i]])
    pgram_period = ps[pgram == max(pgram[peaks])][0]
    _freq = 1./pgram_period
    pgram_freq_err = calc_pgram_uncertainty(x, y, _freq)
    frac_err = pgram_freq_err/_freq
    pgram_period_err = pgram_period * frac_err
    return pgram_period, pgram_period_err


def get_period_from_kepid(kepid,
                          LC_DIR="/Users/ruthangus/.kplr/data/lightcurves"):
    fname = "results/{}_pgram.csv".format(kepid)
    if os.path.exists(fname):
        print(kepid, "periodogram found")

        # Load the light curve
        x, y, yerr = load_kepler_data(os.path.join(LC_DIR, "{}".
                                                format(str(kepid).
                                                        zfill(9))))
        # Load the pgram & calculate period & err
        pgram_df = pd.read_csv(fname)
        pgram_period, pgram_period_err = \
            get_period_from_pgram(pgram_df.periods.values,
                                    pgram_df.power.values, x, y, yerr)
        return pgram_period, pgram_period_err
    else:
        return 0, 0


def package_prots(LC_DIR="/Users/ruthangus/.kplr/data/lightcurves"):
    """
    Save the new rotation periods as a csv.
    """

    # load the star dataframes
    star1 = pd.read_csv("../data/star1_periods.csv")
    star2 = pd.read_csv("../data/star2_periods.csv").iloc[:-1]
    print(np.shape(star1), np.shape(star2))

    pgrams1, errs1, pgrams2, errs2 = [np.zeros(len(star1.kepid.values)) for i
                                               in range(4)]
    for i, kepid in enumerate(star1.kepid.values):
        print(star1.kepid.values[i], star2.kepid.values[i])
        per1, per_err1 = get_period_from_kepid(kepid)
        pgrams1[i], errs1[i] = per1, per_err1
        per2, per_err2 = get_period_from_kepid(star2.kepid.values[i])
        pgrams2[i], errs2[i] = per2, per_err2

    print(np.shape(pgrams1), np.shape(pgrams2), np.shape(star1.kepid.values))
    star1["pgram_period"] = pgrams1
    star1["pgram_period_err"] = errs1
    star2["pgram_period"] = pgrams2
    star2["pgram_period_err"] = errs2

    # save the new dataframes
    star1.to_csv("star1_pgram_periods.csv")
    star2.to_csv("star2_pgram_periods.csv")


if __name__ == "__main__":

    package_prots()
    assert 0

    DATA_DIR = "data"

    # Load list of targets (kepids)
    df = pd.read_csv(os.path.join(DATA_DIR, "targets-small-sep.csv"))

    # start, stop = int(sys.argv[1]), int(sys.argv[2])
    # kepid_list = df.kepid.values[start:stop]

    kepid_list = df.kepid.values

    # loop over kepids and measure their rotation periods.
    # gp_period, gp_errp, gp_errm = gp_prots(kepid_list)

    # save the rotation periods.
    # df = pd.DataFrame({"kepid": kepid_list, "gp_period": gp_period, "gp_errp":
                       # gp_errp, "gp_errm": gp_errm})
    # df.to_csv("targets-small-sep_gp_periods.csv")

    pgram_period, pgram_err = pgram_prots(kepid_list, plot=True)
    df = pd.DataFrame({"kepid": kepid_list, "pgram_period": pgram_period,
                       "pgram_err": pgram_err})
    df.to_csv("targets-small-sep_pgram_periods.csv")
