#!/usr/bin/env python
#
#  Created by Terra ladwig on 9/6/16
#

import numpy as np
import netCDF4 as ncdf
import datetime as DT
import time 
import sys
import pylab as P
import glob
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib

############# Change this stuff ##############################

AQPI_88D_dir = "/mnt/lfs1/projects/public/retro/radar/mrms/without_xband"
AQPI_withXband_dir = "/mnt/lfs1/projects/public/retro/radar/mrms/with_xband"
HRRR_MRMS_dir = ""


# pick a time
mytime = "20190217-120000"
filename = mytime+".netcdf"

#radar="AQPI_88D"
#AQPI_88D=AQPI_88D_dir+"/*/"+filename
radar="AQPI_with_xband"
AQPI_withXband=AQPI_withXband_dir+"/*/"+filename

PNAME=mytime+"Composite_"+radar+".png"


plotq=True
showinc=True

# Set countour intervals here
cmin=0.0
cmax=75.0
cint=5.
clevels = np.arange(cmin,cmax+cint,cint)


#-------------------------------------------------------------------------------
# Main function 

if __name__ == "__main__":

    main_start_time = time.time()

    print
    print "---------------------------- Plot Radar Script  -------------------------------------"
    print
    print

    firstFile = 0

    #for f in glob.glob(AQPI_88D) :
    for f in glob.glob(AQPI_withXband) :
        print f

        #----------------------------------------------------
        # open the input files for reading
        f_in = ncdf.Dataset(f, 'r')
        # get netCDF variable object
        fDBZ  = f_in.variables['MergedReflectivityDPQC'][:,:]

        if firstFile == 0:
            #make composite equal to values from first file
            compositeDBZ = fDBZ

            # get grid info for plotting 
            startLon = f_in.getncattr('Longitude')
            ilon = len(f_in.dimensions['Lon'])
            LonSpace = f_in.getncattr('LonGridSpacing')
            endLon = startLon + LonSpace*ilon
            lons=np.linspace(startLon,endLon,ilon,endpoint=True)

            endLat = f_in.getncattr('Latitude')
            ilat = len(f_in.dimensions['Lat'])
            LatSpace = f_in.getncattr('LatGridSpacing')
            startLat = endLat - LatSpace*ilat
            lats=np.linspace(startLat,endLat,ilat,endpoint=True)

            gridx,gridy=np.meshgrid(lons,lats)

            f_in.close()
            firstFile=1
        else:
            # where next file is greater replace value
            compositeDBZ = np.where(fDBZ>compositeDBZ,fDBZ,compositeDBZ)

    print np.amax(compositeDBZ)

    #----------------------------------------------------
    # plot composite
    if plotq:

        fig = P.figure(figsize=(16.,10.))
        title="Composite Reflectivity " + mytime + " " + radar
        fig.suptitle(title,fontsize=18)

        #HRRR CONUS
        mymap = Basemap(llcrnrlon=-123.,llcrnrlat=20.,urcrnrlon=-59., urcrnrlat=48., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        # CA zoom
        #mymap = Basemap(llcrnrlon=-126.,llcrnrlat=27.,urcrnrlon=-106., urcrnrlat=44., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')

        mplotx, mploty = mymap(gridx,gridy)

        ax = P.subplot(1,1,1)
        mymap.drawcoastlines()
        mymap.drawcountries()
        mymap.drawstates()
        parallels = np.arange(20.,50,3.)
        mymap.drawparallels(parallels,linewidth=0.001,labels=[1,0,0,0],labelstyle="+/-",fontsize=12)
        meridians = np.arange(180.,360.,3.)
        mymap.drawmeridians(meridians,linewidth=0.001, labels=[0,0,0,1],labelstyle="+/-",fontsize=12)
        # Colorado county map
        #mymap.readshapefile('../tl_2012_08_cousub/tl_2012_08_cousub', 'tl_2012_08_cousub', color="white")
        # California counties
        #mymap.readshapefile('../tl_2012_08_cousub/CA_Counties/CA_Counties_TIGER2016', 'CA_Counties_TIGER2016', color="white")


        myplt = mymap.contourf(mplotx,mploty, compositeDBZ, clevels, cmap=plt.get_cmap('jet'))

        cax = fig.add_axes([0.91, 0.25, 0.01, 0.5])
        cb = fig.colorbar(myplt, cax, orientation='vertical')
        cb.set_label('g/kg', size = 'large')
        P.savefig(PNAME)
        if showinc: P.show()


    main_end_time = time.time()
    print "Time taken for main: %f minutes" % ((main_end_time - main_start_time)/60.)
    print "End"

