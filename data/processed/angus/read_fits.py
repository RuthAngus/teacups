# Read the header of a spectrum fits file. This is mainly for checking the
# object name.

from astropy.io import fits
import sys

assert len(sys.argv) > 2, "You need to tell me which night and object " \
    "number to look at!"

night = sys.argv[1]
z = 4
if night == "3":
    z = 3
obs_number = str(sys.argv[2]).zfill(z)

hdulist = fits.open("n{0}/1d_n{0}.{1}.fit".format(night, obs_number))
hdulist.close()

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
