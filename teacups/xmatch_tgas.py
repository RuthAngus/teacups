# Cross match Semyeong's TGAS stars with RAVE, LAMOST, GALAH and APOGEE.

import numpy as np
import gaia_tools.load as gload
import gaia_tools.xmatch as gx
import pandas as pd


def make_tycho_dfs_for_star12():
    # Match tgas_rave with stars 1 and 2.
    star1 = pd.read_csv("star1_kic_1.csv")
    star2 = pd.read_csv("star2_kic_1.csv")
    s1 = pd.DataFrame({"tycho2_id": star1.tycho2_id})
    s2 = pd.DataFrame({"tycho2_id": star2.tycho2_id})
    s1.to_csv("s1.csv")
    s2.to_csv("s2.csv")


def rave_match(tycho_id_df):

    # Load the star one and star two files.
    star1 = pd.read_csv("s1.csv")
    star2 = pd.read_csv("s2.csv")

    # Convert the pandas series objects into dataframes.
    star1 = pd.DataFrame(star1.tycho2_id)
    star2 = pd.DataFrame(star2.tycho2_id)

    # Merge them
    tgas_rave_star1 = pd.merge(tycho_id_df, star1, on="tycho2_id")#, how="inner")
    tgas_rave_star2 = pd.merge(tycho_id_df, star2, on="tycho2_id")#, how="inner")

    # Print the shape of the merged files.
    print(np.shape(tgas_rave_star1))
    print(np.shape(tgas_rave_star2))

    # Double check
    for i, _ in enumerate(tycho_id_df.tycho2_id):
        m = i == star1.tycho2_id
        l = i == star2.tycho2_id
        if len(star1.tycho2_id.values[m]):
            print(star1.tycho2_id.values[m], i)
        elif len(star2.tycho2_id.values[l]):
            print(star2.tycho2_id.values[l], i)

if __name__ == "__main__":

    # # Load the tgas/rave crossmatch file.
    # tgas_rave_hip_df = pd.read_csv("tgas_rave_hip_df.csv")

    # # Remove the "b" and quotation marks from the strings
    # rave_tycho_id = []
    # for i, _ in enumerate(tgas_rave_hip_df.hip):
    #     rave_tycho_id.append(tgas_rave_hip_df.hip[i][2:-1])
    # rave_tycho_id_df = pd.DataFrame({"tycho2_id": tycho_id})

    # rave_tycho_id_df = pd.DataFrame(rave_tycho_id_df.tycho2_id)
    # rave_match(rave_tycho_id_df)

    # Load the tgas/lamost crossmatch file.
    tgas_lamost_tycho_df = pd.read_csv("tgas_lamost_hip_df.csv")
    tgas_lamost_tycho_df = pd.DataFrame(tgas_lamost_tycho_df.tycho2_id)

    # Remove the "b" and quotation marks from the strings
    lamost_tycho_id = []
    for i, _ in enumerate(tgas_lamost_tycho_df.tycho2_id):
        lamost_tycho_id.append(tgas_lamost_tycho_df.tycho2_id[i][2:-1])
    lamost_tycho_id_df = pd.DataFrame({"tycho2_id": lamost_tycho_id})

    lamost_tycho_id_df = pd.DataFrame(lamost_tycho_id_df.tycho2_id)
    rave_match(lamost_tycho_id_df)
