# Get the names of stars and find them in the Kepler catalogue, then use
# source id to find them in stacked_tgas, then figure out what row they are in
# pair_indices.

from astropy.table import Table
import numpy as np
import pandas as pd

# Load the observed stars
observed = pd.read_csv("../data/targets-small-sep.csv")
print(np.shape(observed), "observed stars")

# Load the tgas data (just to get the row inds)
table = Table.read('stacked_tgas.fits')
all_tgas = table.to_pandas()

# Load Semyeong's data file. These are ALL the pairs.
t2 = Table.read('pairindices_cp1.fits')
pair_df = t2.to_pandas()
print(np.shape(pair_df), "all pairs")

# Add group_id and source_id columns to semyeong's file.
pair_df["group_id"] = range(len(pair_df.star1.values))
pair_df["source_id1"] = all_tgas.source_id.values[pair_df.star1]
pair_df["source_id2"] = all_tgas.source_id.values[pair_df.star2]

observed_with_group_id1 = pd.merge(observed, pair_df, left_on="source_id",
                                   right_on="source_id1", how="inner")
observed_with_group_id = pd.merge(observed_with_group_id1, observed,
                                  left_on="source_id2",
                                  right_on="source_id", how="outer",
                                  suffixes=("_star1", "_star2"))

print(np.shape(observed_with_group_id), "all observed stars")
print(observed_with_group_id.keys())
