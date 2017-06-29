"""
Make plot of pgram periods vs gp periods.
"""


import numpy as np
import matplotlib.pyplot as pl
import pandas as pd


plotpar = {'axes.labelsize': 18,
           'font.size': 10,
           'legend.fontsize': 18,
           'xtick.labelsize': 18,
           'ytick.labelsize': 18,
           'text.usetex': True}
pl.rcParams.update(plotpar)


def p_compare(p1, p1_err, p2, p2_err, xlabel, ylabel, fname):
    """
    Plot one period measurement against another.
    """
    xs = np.linspace(0, 60)
    pl.clf()
    pl.errorbar(p1, p2, xerr=p1_err, yerr=p2_err, fmt="k.")
    pl.plot(xs, xs, "--", color=".5")
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)
    pl.subplots_adjust(bottom=.15)
    pl.savefig(fname)


if __name__ == "__main__":
    df = pd.read_csv("targets-small-sep_periods.csv")

    y = df.gp_period
    yerr = [df.gp_errm, df.gp_errp]
    ylabel = "$\mathrm{GP~period~(days)}$"

    x = df.pgram_period
    xerr = df.pgram_err
    xlabel = "$\mathrm{Periodogram~period~(days)}$"
    p_compare(x, xerr, y, yerr, xlabel, ylabel, "gp_vs_period")
