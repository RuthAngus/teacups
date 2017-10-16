# Cross match Semyeong's TGAS stars with RAVE, LAMOST, GALAH and APOGEE.

import gaia_tools.load as gload
import gaia_tools.xmatch as gx

# Xmatch with RAVE, taking into account the epoch difference.
tgas = gload.tgas()
rave_cat = gload.rave()
m1, m2, sep = gx.xmatch(rave_cat, tgas, colRA1='RAdeg', colDec1='DEdeg',
                        colRA2='ra', colDec2='dec', epoch1=2000.,
                        epoch2=2015.,swap=True)
rave_cat = rave_cat[m1]
tgas = tgas[m2]
print(len(rave_cat))
input("enter")

# Match LAMOST to TGAS
tgas = gload.tgas()
lamost_cat = gload.lamost()
m1, m2, sep = gx.xmatch(lamost_cat, tgas, colRA1='ra', colDec1='dec',
                        colRA2='ra',colDec2='dec', epoch1=2000.,epoch2=2015.,
                        swap=True)
lamost_cat = lamost_cat[m1]
tgas = tgas[m2]
print(len(lamost_cat))
input("enter")

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
