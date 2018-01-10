# Get the names of stars and find them in the Kepler catalogue, then use
# source id to find them in stacked_tgas, then figure out what row they are in
# pair_indices.

from astropy.table import Table
import numpy as np
import pandas as pd

# Load the observed stars
df = pd.read_csv("../data/targets-small-sep.csv")

# Load the tgas data
table = Table.read('stacked_tgas.fits')
table_df = table.to_pandas()
table_df["ruth_index"] = np.arange(np.shape(table_df)[0])
print(table_df.ruth_index)

# Merge the observed stars with tgas
observed_tgas = pd.merge(df, table_df, on="source_id", how="inner")
print(observed_tgas.ruth_index)
print(np.shape(table_df), np.shape(df), np.shape(observed_tgas))

# Load Semyeong's data file. These are ALL the pairs.
t2 = Table.read('pairindices_cp1.fits')
pair_df = t2.to_pandas()

# star1_row_index, star2_row_index = [], []
# for i, star in enumerate(observed_tgas.values):
#     if np.isin(star, observed_tgas.ruth_index) and \
#             np.isin(pair_df.star2.values[i], observed_tgas.ruth_index):
#         star1_row_index.append(star)
#         star2_row_index.append(pair_df.star2.values[i])
# inds = np.array(group_id)
# final_df =

for

observed_df["star1_row_index"] = np.array(star1_row_index)
observed_df["star2_row_index"] = np.array(star2_row_index)
observed_df["group_id"] = np.array(group_id)

observed_df.to_csv("observed_kic_tgas.csv")
