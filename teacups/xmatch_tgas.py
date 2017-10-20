# Cross match Semyeong's TGAS stars with RAVE, LAMOST, GALAH and APOGEE.

import numpy as np
import gaia_tools.load as gload
import gaia_tools.xmatch as gx
import pandas as pd

tgas_rave_hip_df = pd.read_csv("tgas_rave_hip_df.csv")

# # Match tgas_rave with stars 1 and 2.
# star1 = pd.read_csv("star1_kic_1.csv")
# star2 = pd.read_csv("star2_kic_1.csv")
# s1 = pd.DataFrame({"tycho2_id": star1.tycho2_id})
# s2 = pd.DataFrame({"tycho2_id": star2.tycho2_id})
# s1.to_csv("s1.csv")
# s2.to_csv("s2.csv")

tycho_id = []
for i, _ in enumerate(tgas_rave_hip_df.hip):
    tycho_id.append(tgas_rave_hip_df.hip[i][2:-1])
tycho_id_df = pd.DataFrame({"tycho2_id": tycho_id})

star1 = pd.read_csv("s1.csv")
star2 = pd.read_csv("s2.csv")

tycho_id_df = pd.DataFrame(tycho_id_df.tycho2_id)
star1 = pd.DataFrame(star1.tycho2_id)
star2 = pd.DataFrame(star2.tycho2_id)

tgas_rave_star1 = pd.merge(tycho_id_df, star1, on="tycho2_id")#, how="inner")
tgas_rave_star2 = pd.merge(tycho_id_df, star2, on="tycho2_id")#, how="inner")

print(np.shape(tgas_rave_star1))
print(np.shape(tgas_rave_star2))

# Double check
for i, _ in enumerate(tycho_id_df.tycho2_id):
    m = i == star1.tycho2_id
    l = i == star2.tycho2_id
    if len(star1.tycho2_id.values[m]):
        print(star1.tycho2_id.values[m], i)
    elif len(star2.tycho2_id.values[m]):
        print(star2.tycho2_id.values[m], i)

import csv

from collections import OrderedDict # to save keys order

with open('star1_kic_1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader) #skip header
    d = OrderedDict(({"val": rows[1], "flag": False}) for rows in reader)
print(d["flag"])
assert 0

with open('tgas_rave_hip_df.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader) #skip header
    for rows in reader:
        if rows[1] in d:
            d[rows[0]]["flag"] = True

import sys
sys.stdout = open("test.csv", "w")

for k, v in d.items():
    if v["flag"]:
        print([v["val"], k])

assert 0

tgas_lamost_hip_df = pd.read_csv("tgas_lamost_hip_df.csv")
# Match tgas_rave with stars 1 and 2.
tgas_lamost_star1 = pd.merge(tgas_lamost_hip_df, star1, on="hip")
tgas_lamost_star2 = pd.merge(tgas_lamost_hip_df, star2, on="hip")
print(np.shape(tgas_rave_star1), np.shape(tgas_rave_star2))

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
