# Crossmatch tgas with spectroscopic surveys and save the resulting list of
# Hipparchos ids as a .csv file.

import numpy as np
import gaia_tools.load as gload
import gaia_tools.xmatch as gx
import pandas as pd


def masked_array_to_simple_array(masked_array):
    # tgas_survey_hip_id = np.zeros(len(masked_array))
    tgas_survey_hip_id = []
    tgas_survey_array = np.array(masked_array)
    for i, _ in enumerate(masked_array):
        masked_array[i] = np.array(masked_array[i])
        # tgas_survey_hip_id[i] = masked_array[i][1]
        tgas_survey_hip_id.append(masked_array[i][1])
    return tgas_survey_hip_id


def save_matched_hipp_ids(spec_survey):
    if spec_survey == "rave":
        # Xmatch with RAVE, taking into account the epoch difference.
        tgas = gload.tgas()
        rave_cat = gload.rave()
        m1, m2, sep = gx.xmatch(rave_cat, tgas, colRA1='RAdeg', colDec1='DEdeg',
                                colRA2='ra', colDec2='dec', epoch1=2000.,
                                epoch2=2015.,swap=True)
        rave_cat = rave_cat[m1]
        tgas_rave = tgas[m2]

        tgas_rave_hip = masked_array_to_simple_array(tgas_rave)
        tgas_rave_hip_df = pd.DataFrame({"hip": tgas_rave_hip})
        tgas_rave_hip_df.to_csv("tgas_rave_hip_df.csv")

    elif spec_survey == "lamost":
        # Match LAMOST to TGAS
        tgas = gload.tgas()
        lamost_cat = gload.lamost()
        m1, m2, sep = gx.xmatch(lamost_cat, tgas, colRA1='ra', colDec1='dec',
                                colRA2='ra', colDec2='dec', epoch1=2000.,
                                epoch2=2015., swap=True)
        lamost_cat = lamost_cat[m1]
        tgas_lamost = tgas[m2]
        tgas_lamost_hip_id = masked_array_to_simple_array(tgas_lamost)
        tgas_lamost_hip_df = pd.DataFrame({"tycho2_id": tgas_lamost_hip_id})
        tgas_lamost_hip_df.to_csv("tgas_lamost_hip_df.csv")

if __name__ == "__main__":
    # save_matched_hipp_ids("rave")
    save_matched_hipp_ids("lamost")
