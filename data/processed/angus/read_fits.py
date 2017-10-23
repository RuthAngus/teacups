# Read the header of a spectrum fits file. This is mainly for checking the
# object name.

from astropy.io import fits
import sys

assert len(sys.argv) > 2, "You need to tell me which night and object " \
    "number to look at!"

night = sys.argv[1]
z = 3
if night == "1":
    z = 4
elif night == "2":
    z = 4
obs_number = str(sys.argv[2]).zfill(z)

hdulist = fits.open("n{0}/1d_n{0}.{1}.fit".format(night, obs_number))
hdulist.close()

if hdulist[0].header["IMAGETYP"] == "COMP":
    print("IMAGETYP = ", hdulist[0].header["IMAGETYP"])
    if input("Would you like to change the IMAGETYP? y/n ") == "y":
        new_typ = input("What would you like to change it to? (type enter for"
                        " 'object') ")
        if new_typ == "":
            new_typ = "object"
        fits.setval("n{0}/1d_n{0}.{1}.fit".format(night, obs_number),
                    "IMAGETYP", value=new_typ)

    hdulist = fits.open("n{0}/1d_n{0}.{1}.fit".format(night, obs_number))
    print("New IMAGETYP name = ", hdulist[0].header["IMAGETYP"])

print("Object name = ", hdulist[0].header["OBJECT"])
if input("Would you like to rename the header object? y/n ") == "y":
    new_name = input("Type the name you'd like: ")
    proceed2 = input("Replace header name with {}, are you sure? y/n "
                        .format(new_name))
    if proceed2 == "y":
        fits.setval("n{0}/1d_n{0}.{1}.fit".format(night, obs_number),
                    "OBJECT", value=new_name)

    hdulist = fits.open("n{0}/1d_n{0}.{1}.fit".format(night, obs_number))
    print("New object name = ", hdulist[0].header["OBJECT"])
