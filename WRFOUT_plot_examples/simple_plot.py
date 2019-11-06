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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib

############# Change this stuff ##############################

BACK = "/mnt/lfs3/projects/rtwbl/terra/GSI_tests/HRRRE/2016052415/wrfprd_mem0001/wrfinput_d01_after_enkf"


lev=6

plotq=True
showinc=True


matplotlib.rcParams.update({'font.size': 18})

#-------------------------------------------------------------------------------
# Main function 

if __name__ == "__main__":

    main_start_time = time.time()

    print
    print "---------------------------- Plot Increment Script  -------------------------------------"
    print
    print

    #----------------------------------------------------
    # open the input files for reading
    b_in = ncdf.Dataset(BACK, 'r')
    # get netCDF variable object
    b_lon  = b_in.variables['XLONG'][:,:,:]
    b_lat  = b_in.variables['XLAT'][:,:,:]
    b_q  = b_in.variables['QVAPOR'][:,:,:,:]
    b_in.close()



    #----------------------------------------------------
    # plot qcloud inc
    if plotq:

        fig = P.figure(figsize=(16.,10.))
        fig.suptitle("Water Vapor Increments for model level " + str(lev))

        #HRRR CONUS
        #mymap = Basemap(llcrnrlon=-123.,llcrnrlat=20.,urcrnrlon=-59., urcrnrlat=48., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #HRRRE
        #mymap = Basemap(llcrnrlon=-110.,llcrnrlat=22.,urcrnrlon=-63., urcrnrlat=46., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T2 subdomain
        #mymap = Basemap(llcrnrlon=-108.,llcrnrlat=36.5,urcrnrlon=-86., urcrnrlat=49., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T3 subdomain
        #mymap = Basemap(llcrnrlon=-94.,llcrnrlat=35.,urcrnrlon=-66.5, urcrnrlat=46., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T5 subdomain
        #mymap = Basemap(llcrnrlon=-107.8,llcrnrlat=23.7,urcrnrlon=-87., urcrnrlat=42.4, projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T6 subdomain
        #mymap = Basemap(llcrnrlon=-95.,llcrnrlat=24.2,urcrnrlon=-70.8, urcrnrlat=36.5, projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T7 subdomain
        #mymap = Basemap(llcrnrlon=-96.5,llcrnrlat=36.5,urcrnrlon=-71., urcrnrlat=47., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T8 subdomain Colorado
        mymap = Basemap(llcrnrlon=-109,llcrnrlat=36.,urcrnrlon=-99.5, urcrnrlat=42., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #T8 subdomain Chasemap
        #mymap = Basemap(llcrnrlon=-109,llcrnrlat=33.,urcrnrlon=-95., urcrnrlat=44., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        mplotx, mploty = mymap(b_lon[0,:,:],b_lat[0,:,:])

        ax = P.subplot(1,1,1)
        mymap.drawcoastlines()
        mymap.drawcountries()
        mymap.drawstates()
        parallels = np.arange(20.,50,5.)
        mymap.drawparallels(parallels,linewidth=0.001,labels=[1,0,0,0],labelstyle="+/-",fontsize=18)
        meridians = np.arange(180.,360.,5.)
        mymap.drawmeridians(meridians,linewidth=0.001, labels=[0,0,0,1],labelstyle="+/-",fontsize=18)
        # Colorado county map
        mymap.readshapefile('../tl_2012_08_cousub/tl_2012_08_cousub', 'tl_2012_08_cousub', color="white")


        plt = mymap.contourf(mplotx,mploty, b_q[0,lev,:,:]*1000)

        cax = fig.add_axes([0.91, 0.25, 0.01, 0.5])
        cb = fig.colorbar(plt, cax, orientation='vertical')
        cb.set_label('g/kg', size = 'large')
        if showinc: P.show()


    main_end_time = time.time()
    print "Time taken for main: %f minutes" % ((main_end_time - main_start_time)/60.)
    print "End"

