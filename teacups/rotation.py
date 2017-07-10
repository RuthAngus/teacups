"""
A system for measuring rotation periods.
"""

import os
import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import filtering as flt

import kplr
client = kplr.API()

import kepler_data as kd
from astropy.stats import LombScargle


class prot(object):
    """
    Given a star object with a kepid or x, y and yerr values, measure the
    rotation period.
    """

    def __init__(self, kepid=None, x=None, y=None, yerr=None,
                 LC_DIR="/Users/ruthangus/.kplr/data/lightcurves"):
        """
        params:
        ------
        kepid: (int)
            The KIC id.
        x: (array)
            The time array.
        y: (array)
            The flux array.
        yerr: (array)
            The flux uncertainty array.
        """
        self.kepid = kepid

        # If x, y and yerr are not provided, load them.
        if not x and not y and not yerr:
            lc_path = os.path.join(LC_DIR, str(kepid).zfill(9))

            # If you don't have the light curves, download them.
            if not os.path.exists(lc_path):
                print("Downloading light curve...")
                star = client.star(kepid)
                star.get_light_curves(fetch=True, short_cadence=False)

            print("Loading light curve...")
            self.x, self.y, self.yerr = kd.load_kepler_data(lc_path)
        else:
            self.x, self.y, self.yerr = x, y, yerr

    def pgram_ps(self, plot=False):
        """
        Measure a periodogram rotation period
        returns:
        -------
        pgram_period: (float)
            The rotation period
        pgram_period_err: (float)
            The formal uncertainty on the period.

        Adds self.pgram_period, self.pgram_period.err, self.pgram and self.ps.
        """

        pgram_fname = "pgrams/{}_pgram.csv".format(self.kepid)
        if os.path.exists(pgram_fname):
            pr = pd.read_csv(pgram_fname)
            ps, pgram = pr.periods.values, pr.power.values

        else:
            ps = np.arange(.1, 100, .1)
            freq = 1./ps

            filter_period = 35.  # days
            fs = 1./(self.x[1] - self.x[0])
            lowcut = 1./filter_period
            yfilt = flt.butter_bandpass_filter(self.y, lowcut, fs, order=3,
                                               plot=False)

            print("Calculating periodogram")
            pgram = LombScargle(self.x, yfilt, self.yerr).power(freq)

            peaks = np.array([i for i in range(1, len(ps)-1) if pgram[i-1] <
                                pgram[i] and pgram[i+1] < pgram[i]])

            presults = pd.DataFrame({"periods": ps, "power": pgram})
            presults.to_csv("{}.csv".format(pgram_fname))

        pgram_period = ps[pgram == max(pgram[peaks])][0]
        if plot:
            plt.clf()
            plt.plot(ps, pgram)
            plt.axvline(pgram_period, color="r")
            plt.savefig(pgram_fname)

        # Calculate the uncertainty.
        _freq = 1./pgram_period
        pgram_freq_err = self.calc_pgram_uncertainty(_freq)
        frac_err = pgram_freq_err/_freq
        pgram_period_err = pgram_period * frac_err

        self.pgram_period = pgram_period
        self.pgram_period_err = pgram_period_err
        self.pgram = pgram
        self.ps = ps
        return pgram_period, pgram_period_err

    def calc_pgram_uncertainty(self, freq):
        """
        Calculate the formal uncertainty on the periodogram period (1/freq).
        """
        phase, A = self.calc_phase_and_amp(freq)
        y_noise = self.y - A**2*np.sin(2*np.pi*freq*self.x + phase)
        sigma_n = np.var(y_noise)
        N, T = len(self.x), self.x[-1] - self.x[0]
        return 3 * np.pi * sigma_n / (2 * N**.5 * T * A)

    def calc_phase_and_amp(self, f):
        """
        Phase and amplitude calculation for the calc_pgram_uncertainty
        function.
        """
        AT = np.vstack((self.x, np.ones((3, len(self.y)))))
        ATA = np.dot(AT, AT.T)
        arg = 2*np.pi*f*self.x
        AT[-2, :] = np.sin(arg)
        AT[-1, :] = np.cos(arg)
        v = np.dot(AT[:-2, :], AT[-2:, :].T)
        ATA[:-2, -2:] = v
        ATA[-2:, :-2] = v.T
        ATA[-2:, -2:] = np.dot(AT[-2:, :], AT[-2:, :].T)
        w = np.linalg.solve(ATA, np.dot(AT, self.y))
        A, B = w[-1], w[-2]
        phase = np.arctan(A/B)
        Amp = (np.abs(A) + np.abs(B))**.5
        return phase, Amp
