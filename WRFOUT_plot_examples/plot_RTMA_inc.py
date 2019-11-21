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
import wrf

############# Change this stuff ##############################

# CSH point to path of wrfout background file
BACK = "/mnt/lfs3/projects/rtwbl/terra/GSI_tests/HRRR/2017041017/wrfout_d01_2017-04-10_17_00_00"
# CSH point to path of wrf_inout analysis file 
ANAL = "/mnt/lfs3/projects/rtwbl/terra/GSI_tests/HRRR/2017041017/gsiprd/wrf_inoutNEWCODE"

# CSH this is the model level, can try a few options
lev=6

plotq=True
plotqcross=False
showinc=True

# CSH pick a name for your plot
PNAME="qv_"+str(lev)+"_2017041017_NEWCODE.png"

# CSH these are the contour intervals... trial and error needed to get a good plot 
cmin=-5
cmax=6.
cint=1.
#mynorm = matplotlib.colors.Normalize(vmin=cmin,vmax=cmax,clip=True)
clevels = np.arange(cmin,cmax+cint,cint)

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
    b_qcloud  = b_in.variables['QCLOUD'][:,:,:,:]
    b_qice  = b_in.variables['QICE'][:,:,:,:]
    #b_t  = b_in.variables['T'][0,:,:,:]
    #b_tinit  = b_in.variables['T_INIT'][0,:,:,:]
    b_tc=wrf.getvar(b_in,"tc")
    b_t=(wrf.to_np(b_tc)*9./5.+32.)
    b_in.close()

    a_in = ncdf.Dataset(ANAL, 'r')
    a_q  = a_in.variables['QVAPOR'][:,:,:,:]
    a_qcloud  = a_in.variables['QCLOUD'][:,:,:,:]
    a_qice  = a_in.variables['QICE'][:,:,:,:]
    a_in.close()

    Zlons=np.zeros([np.shape(b_qcloud)[1],np.shape(b_qcloud)[3]])
    LATzs=np.zeros([np.shape(b_qcloud)[1],np.shape(b_qcloud)[3]])
    #print np.shape(Zlons)
    for z in np.arange(np.shape(b_qcloud)[1]):
        Zlons[z,:]=b_lon[0,lat,:]
    #print Zlons[0]
    for l in np.arange(np.shape(b_qcloud)[3]):
        LATzs[:,l]=np.arange(np.shape(b_qcloud)[1])

    # water vapor increment
    inc_q = (a_q[0,:,:,:] - b_q[0,:,:,:])*1000.
    inc_q = np.ma.masked_inside(inc_q,-0.000001,0.000001)
    # cloud water increment
    inc_qcloud = (a_qcloud - b_qcloud)*1000.
    # cloud ice increment
    inc_qice = (a_qice - b_qice)*1000.


    #----------------------------------------------------
    # plot qcloud inc
    if plotq:

        fig = P.figure(figsize=(16.,10.))
        # CSH change plot title
        #fig.suptitle("Cloud Ice Increments for model level " + str(lev))
        fig.suptitle("Water Vapor Increments for model level " + str(lev))
        #fig.suptitle("HRRR Cloud Water Increments for model level " + str(lev))

        #HRRR CONUS
        #mymap = Basemap(llcrnrlon=-123.,llcrnrlat=20.,urcrnrlon=-59., urcrnrlat=48., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #OK
        #mymap = Basemap(llcrnrlon=-105.,llcrnrlat=27.,urcrnrlon=-88., urcrnrlat=40., projection='lcc', lat_1=38.5,lat_0=38.5,lon_0=-97.5, resolution='l')
        #mplotx, mploty = mymap(b_lon[0,:,:],b_lat[0,:,:])

        ax = P.subplot(1,1,1)
        #mymap.drawcoastlines()
        #mymap.drawcountries()
        #mymap.drawstates()
        #parallels = np.arange(20.,50,5.)
        #mymap.drawparallels(parallels,linewidth=0.001,labels=[1,0,0,0],labelstyle="+/-",fontsize=18)
        #meridians = np.arange(180.,360.,5.)
        #mymap.drawmeridians(meridians,linewidth=0.001, labels=[0,0,0,1],labelstyle="+/-",fontsize=18)

        #use wrf python
        lats, lons = wrf.latlon_coords(b_tc)
        bm = wrf.get_basemap(b_tc)
        bm.drawcoastlines(linewidth=0.25)
        bm.drawstates(linewidth=0.25)
        bm.drawcountries(linewidth=0.25)
        mplotx, mploty = bm(wrf.to_np(lons), wrf.to_np(lats))

        #plt = mymap.contourf(mplotx,mploty, inc_q[lev,:,:], clevels, extend='both', cmap=P.cm.seismic_r)
        # CSH change inc_? for which field plotted
        # CSH can remove clevels to have it pick contour levels for you
        plt = bm.contourf(mplotx,mploty, inc_q[lev,:,:], clevels, extend='both', cmap=P.cm.seismic_r)


        cax = fig.add_axes([0.91, 0.25, 0.01, 0.5])
        cb = fig.colorbar(plt, cax, orientation='vertical')
        cb.set_label('g/kg', size = 'large')
        P.savefig(PNAME)
        if showinc: P.show()


    main_end_time = time.time()
    print "Time taken for main: %f minutes" % ((main_end_time - main_start_time)/60.)
    print "End"

