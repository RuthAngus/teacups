from astropy.io import fits
hdulist = fits.open("1d_n1.0131.fit")
hdulist.close()
print(hdulist[0].header)
print(hdulist[0].header["OBJECT"])
