"""
Find the row in the stacked_tgas file given the KIC id.
"""

import numpy as np
import pandas as pd
from astropy.table import Table


def row_ind(kepid, tgas=None):
    """
    Takes a KIC id (kepid) and returns the indices of the corresponding rows
    in stacked tgas.
    returns:
    matched_star_ind: (int)
        The row index of the star with the given kepid in stacked tgas.fits
    other_star_ind: (int)
        The row index of the other star in the pair in stacked tgas.fits
    """

    # load the kplr_tgas file.
    kt = pd.read_csv("kic_tgas.csv")

    # Find the source id.
    m = kt.kepid.values == kepid
    source_id = int(kt.tgas_source_id.values[m])

    # Find the row in stackekd_tgas.
    if tgas is None:
        table = Table.read('stacked_tgas.fits')
    else:
        table = tgas
    # stacked_tgas_df = table.to_pandas()
    # k = stacked_tgas_df.source_id.values == source_id
    # r = np.arange(len(k))[k]
    return np.where(table['source_id'] == source_id)

    t2 = Table.read('pairindices_cp1.fits')
    pair = t2.to_pandas()
    s1 = pair.star1.values == r
    s2 = pair.star2.values == r

    if len(pair.star1.values[s1]):
        matched_star_ind = int(pair.star1.values[s1])
        other_star_ind = int(pair.star2.values[s1])
    elif len(pair.star2.values[s2]):
        matched_star_ind = int(pair.star2.values[s2])
        other_star_ind = int(pair.star1.values[s2])

    return matched_star_ind, other_star_ind


if __name__ == "__main__":
    print(row_ind(10454113))
