# Get the names of stars and find them in the Kepler catalogue, then use
# source id to find them in stacked_tgas, then figure out what row they are in
# pair_indices.

from astropy.table import Table
import numpy as np
import pandas as pd

# # Load the observed stars
# observed = pd.read_csv("../data/targets-small-sep.csv")
# print(np.shape(observed), "observed stars")

# # Load the tgas data (just to get source id from the row inds)
# table = Table.read('stacked_tgas.fits')
# all_tgas = table.to_pandas()

# # # Load Semyeong's data file. These are ALL the pairs.
# t2 = Table.read('pairindices_cp1.fits')
# pair_df = t2.to_pandas()
# print(np.shape(pair_df), "all pairs")

# # Add pair_id and source_id columns to semyeong's file.
# pair_df["pair_id"] = range(len(pair_df.star1.values))
# pair_df["source_id1"] = all_tgas.source_id.values[pair_df.star1]
# pair_df["source_id2"] = all_tgas.source_id.values[pair_df.star2]

# # Merge 1st star in pairs with observed data on source_id to add group ids.
# # This produces a smaller df with info for just the first stars.
# observed_with_pair_id1 = pd.merge(pair_df, observed, right_on="source_id",
#                                    left_on="source_id1", how="inner")

# # Now do the same for the second stars in the pairs.
# observed_with_pair_id2 = pd.merge(pair_df, observed, right_on="source_id",
#                                    left_on="source_id2", how="inner")

# # Concatenate these two dfs.
# joint = pd.concat((observed_with_pair_id1, observed_with_pair_id2))

# joint.to_csv("joint.csv")
joint = pd.read_csv("joint.csv")

star1 = joint.source_id1.values
star2 = joint.source_id2.values
pair_id = joint.pair_id.values

# Now find repeated pairs of source_ids, either way around.
tups_fwd = list(zip(joint.source_id1.values, joint.source_id2.values))
tups_bkwd = list(zip(joint.source_id2.values, joint.source_id1.values))
for i in tups_bkwd:
    tups_fwd.append(i)
tups = tups_fwd

# # Remove duplicates
# seen = set()
# result = []
# pair_id_no_dups = []
# for i, tup in enumerate(tups):
#     if tup not in seen and tup[::-1] not in seen and tup[0] != tup[1]:
#          seen.add(tup)
#          result.append(tup)
#          pair_id_no_dups.append(pair_id[i])

def find_new_stars(star, star_array):
    """
    Given a star id, find all the pairs to that star in star_array.
    """
    group = [star]
    m1 = star == star_array[:, 0]
    m2 = star == star_array[:, 1]
    print("star = ", star)
    print("chosen star = ", star_array[:, 0][m1])
    print("its pairs = ", star_array[:, 1][m1])
    for st in star_array[:, 1][m1]:
        group.append(st)

    if len(star_array[:, 1][m2]):
        print("chosen star as star2 = ", star_array[:, 1][m2])
        print("its pairs = ", star_array[:, 0][m2])
        for st in star_array[:, 0][m2]:
            group.append(st)

    print("group = ", group)
    print("unique group = ", np.unique(np.array(group)))
    return np.unique(np.array(group))
    # return star_array[:, 1][m1], star_array[:, 0][m2]

# Now assign group ids. To start with, each pair in tups is a group. If any
# star is repeated elsewhere, that star's pair is added to the group.
def find_group(i, star_array):
    print(tups[i][0], tups[i][1], "\n")
    find_new_stars(tups[i][0], star_array)

star_array = np.vstack((star1, star2)).T
for i in range(1):
    find_group(i, star_array)
