#######
# Plot script for RAP
# Makes a 2D composite of cloud water and ice
# Created: Aug 2017, Terra Ladwig
#######


#import
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import pygrib
import glob
import os
import datetime as DT
from netCDF4 import Dataset
# note this uses the wrf python package, so you must have a python version with it
# this one works 11/6/2019
# /mnt/lfs1/projects/rtwbl/terra/miniconda2/bin/python
from wrf import to_np, getvar, smooth2d, get_basemap, latlon_coords

# This netcdf wrfout file is used to get the RAP grid info and data
RAPgrid="/mnt/lfs1/projects/rtwbl/terra/wrfout_d01_2019-11-06_15_00_00"

# Set countour intervals here
cmin=0.0
cmax=3.0
cint=0.3
clevels = np.arange(cmin,cmax+cint,cint)

#open the NetCDF file
ncfile = Dataset(RAPgrid)

# Get the sea level pressure
slp = getvar(ncfile, "slp")
cld_water=getvar(ncfile, "QCLOUD")
cld_ice  =getvar(ncfile, "QICE")
cloud3d = to_np(cld_water)+to_np(cld_ice)
print np.shape(cloud3d)
comp_cld=np.sum(cloud3d,axis=0)*1000.
print np.shape(comp_cld)

# Get the latitude and longitude points
lats, lons = latlon_coords(slp)

# Get the basemap object
bm = get_basemap(slp)

# Create a figure
fig = plt.figure(figsize=(12,9))

# Add geographic outlines
bm.drawcoastlines(linewidth=0.25)
bm.drawstates(linewidth=0.25)
bm.drawcountries(linewidth=0.25)

# Convert the lats and lons to x and y.  Make sure you convert the lats and lons to
# numpy arrays via to_np, or basemap crashes with an undefined RuntimeError.
x, y = bm(to_np(lons), to_np(lats))

# Draw the contours and filled contours
#bm.contour(x, y, to_np(slp), 10, colors="black")
#bm.contourf(x, y, to_np(slp), 10, cmap=get_cmap("jet"))
bm.contourf(x, y, comp_cld, clevels, cmap=get_cmap("jet"))

# Add a color bar
plt.colorbar(shrink=.62)

#plt.title("Sea Level Pressure (hPa)")
plt.title("Composite Cloud Mixing Ratio (g/kg)")

plt.show()

ncfile.close()
#end
