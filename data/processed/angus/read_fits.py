# Read the header of a spectrum fits file. This is mainly for checking the
# object name.

from astropy.io import fits
import sys

assert len(sys.argv) > 3, "You need to tell me which night, object " \
    "number and file type (1d or p) to look at!"

night = sys.argv[1]
z = 3
if night == "1":
    z = 4
elif night == "2":
    z = 4
obs_number = str(sys.argv[2]).zfill(z)
filetype = str(sys.argv[3])

fname = "n{0}/{2}_n{0}.{1}.fit".format(night, obs_number, filetype)

hdulist = fits.open(fname)
hdulist.close()

print("Object name = ", hdulist[0].header["OBJECT"])

if hdulist[0].header["IMAGETYP"] == "COMP":
    print("IMAGETYP = ", hdulist[0].header["IMAGETYP"])
    if input("Would you like to change the IMAGETYP? y/n ") == "y":
        new_typ = input("What would you like to change it to? (type enter for"
                        " 'OBJECT') ")
        if new_typ == "":
            new_typ = "OBJECT"
        fits.setval(fname, "IMAGETYP", value=new_typ)

hdulist = fits.open(fname)
print("IMAGETYP name = ", hdulist[0].header["IMAGETYP"])

if input("Would you like to rename the header object? y/n ") == "y":
    new_name = input("Type the name you'd like: ")
    proceed2 = input("Replace header name with {}, are you sure? y/n "
                        .format(new_name))
    if proceed2 == "y":
        fits.setval(fname, "OBJECT", value=new_name)

    hdulist = fits.open(fname)
    print("New object name = ", hdulist[0].header["OBJECT"])
