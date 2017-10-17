# Cross match Semyeong's TGAS stars with RAVE, LAMOST, GALAH and APOGEE.

import numpy as np
import gaia_tools.load as gload
import gaia_tools.xmatch as gx
import pandas as pd


def masked_array_to_simple_array(masked_array):
    tgas_survey_hip_id = np.zeros(len(masked_array))
    tgas_survey_array = np.array(masked_array)
    for i, _ in enumerate(masked_array):
        masked_array[i] = np.array(masked_array[i])
        tgas_survey_hip_id[i] = masked_array[i][0]
    return tgas_survey_hip_id


# Xmatch with RAVE, taking into account the epoch difference.
tgas = gload.tgas()
rave_cat = gload.rave()
m1, m2, sep = gx.xmatch(rave_cat, tgas, colRA1='RAdeg', colDec1='DEdeg',
                        colRA2='ra', colDec2='dec', epoch1=2000.,
                        epoch2=2015.,swap=True)
rave_cat = rave_cat[m1]
tgas_rave = tgas[m2]

# tgas_rave_hip = np.zeros(len(tgas_rave))
# tgas_rave_tycho_ids = np.array(tgas_rave)
# for i, _ in enumerate(tgas_rave_tycho_ids):
#     tgas_rave_tycho_ids[i] = np.array(tgas_rave_tycho_ids[i])
#     tgas_rave_hip[i] = tgas_rave_tycho_ids[i][0]
print("pixie")
tgas_rave_hip = masked_array_to_simple_array(tgas_rave)

print("fairy dust")
tgas_rave_hip_df = pd.DataFrame({"hip": tgas_rave_hip})
pd.to_csv("tgas_rave_hip_df.csv")

assert 0

print("goblin")
# Match tgas_rave with stars 1 and 2.
star1 = pd.read_csv("star1_kic_1.csv")
star2 = pd.read_csv("star2_kic_1.csv")
tgas_rave_star1 = pd.merge(tgas_rave_hip_df, star1, on="hip")
tgas_rave_star2 = pd.merge(tgas_rave_hip_df, star2, on="hip")

print("elf")
print(np.shape(tgas_rave_star1), np.shape(tgas_rave_star2))

assert 0

# Match LAMOST to TGAS
tgas = gload.tgas()
lamost_cat = gload.lamost()
m1, m2, sep = gx.xmatch(lamost_cat, tgas, colRA1='ra', colDec1='dec',
                        colRA2='ra',colDec2='dec', epoch1=2000.,epoch2=2015.,
                        swap=True)
lamost_cat = lamost_cat[m1]
tgas_lamost = tgas[m2]

tgas_lamost_hip_id = masked_array_to_simple_array(tgas_lamost)

assert 0

# Match APOGEE or APOGEE-RC to TGAS
tgas = gload.tgas()
apogee_cat = gload.apogee()
m1, m2, sep = gx.xmatch(apogee_cat, tgas, colRA2='ra', colDec2='dec',
                        epoch1=2000., epoch2=2015., swap=True)
apogee_cat = apogee_cat[m1]
tgas = tgas[m2]
print(len(apogee_cat))
input("enter")

# Match GALAH to TGAS
tgas = gload.tgas()
galah_cat = gload.galah()
m1, m2, sep = gx.xmatch(galah_cat, tgas, colRA1='RA', colDec1='dec',
                        colRA2='ra', colDec2='dec', epoch1=2000.,
                        epoch2=2015.,swap=True)
galah_cat = galah_cat[m1]
tgas = tgas[m2]
print(len(galah_cat))
