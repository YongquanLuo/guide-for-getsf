# -*- coding: utf-8 -*-

#%%

from astropy.io import ascii, fits
from astropy.wcs import WCS
from astropy import units as u
from radio_beam import Beam
import numpy as np

#%%

hdu = fits.open("your fits file")
header = hdu[0].header
data = hdu[0].data
hdu.close()

#%%

beam = Beam(major = header['BMAJ']*u.deg, minor = header['BMIN']*u.deg, pa = header['BPA']*u.deg)
beam_arc = np.sqrt(beam.sr.to(u.arcsec * u.arcsec)).value

wcs = WCS(header)
# pix_area = abs(wcs.proj_plane_pixel_area()).to(u.sr)  # area of each pixel in sr
beam_area = beam.sr                                 # spherical angle of beam

data_Jy_sr = data * (1*u.Jy) / beam_area
data_MJy_sr = data_Jy_sr.to(u.MJy/u.sr)

#%%

header_new = header
header_new['CD1_1'] = header['CDELT1']
header_new['CD1_2'] = 0
header_new['CD2_1'] = 0
header_new['CD2_2'] = header['CDELT2']
header_new['RA'] = header['CRVAL1']
header_new['DEC'] = header['CRVAL2']
header_new['EQUINOX'] = 2e3
header_new['WAVE'] = 1300
header_new['DATAMAX'] = np.nanmax(data_MJy_sr.value)
header_new['DATAMIN'] = np.nanmin(data_MJy_sr.value)
header_new['BUNIT'] = 'MJy/sr'
header_new['CROTA1'] = 0
header_new['CROTA2'] = 0
header_new['BZERO'] = 0
header_new['BSCALE'] = 1

hdu_new = fits.PrimaryHDU(data = data_MJy_sr.value, header = header_new)
hdu_new.writeto("***\\alma_1300.fits", overwrite = False)



