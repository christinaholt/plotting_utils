#######################################################################
#----------------------------------------------------------------------
# eta2height.py
# useage: python eta2height.py -f wrf_out_file -p plot_name.pdf
# calculates and plots vertical grid spacing for a WRF eta grid.
# Created by Terra Thompson 2/26/14
#----------------------------------------------------------------------
#######################################################################

# imports
import sys
import numpy as N
import netCDF4
from optparse import OptionParser
import matplotlib.pyplot as plt

# Contsants
R = 287.
CP = 1004.
G = 9.81

#----------------------------------------------------------------------
# Function to convert WRF eta coordinates
# Eta definition (nu):
# nu = (P - Ptop) / (Psfc - Ptop)
def convert_eta(wrfnc, p_or_z):
    
    # option to return height or pressure
    if p_or_z.lower() == "z":
        return_z = True
    else:
        return_z = False
    
    # get variables from file
    height_data = wrfnc.variables["HGT"][0,:,:]
    znu_data = wrfnc.variables["ZNU"][0,:] # these are the mass levels (center of grid box)
    t00_data = wrfnc.variables["T00"][0]
    psfc_data = wrfnc.variables["PSFC"][0,:,:]
    ptop_data = wrfnc.variables["P_TOP"][0]
    pth_data = wrfnc.variables["T"][0,:,:,:] # Pert potential temp 
    
    theta_data = pth_data + t00_data
     
    pcalc_data = N.zeros(pth_data.shape, dtype=N.float32)
    mean_t_data = N.zeros(pth_data.shape, dtype=N.float32)
    temp_data = N.zeros(pth_data.shape, dtype=N.float32)
    z_data = N.zeros(pth_data.shape, dtype=N.float32)
    
    # calculate pressure
    for k in xrange(znu_data.shape[0]):
        pcalc_data[k,:,:] = znu_data[k]*(psfc_data[:,:] - (ptop_data)) + (ptop_data)
    
    # calculate height
    if return_z:
        for k in xrange(znu_data.shape[0]):
            temp_data[k,:,:] = (theta_data[k,:,:]) / ((100000.0 / (pcalc_data[k,:,:]))**(R/CP))      
            mean_t_data[k,:,:] = N.mean(temp_data[0:k+1,:,:], axis=0)
            z_data[k,:,:] = ((R*mean_t_data[k,:,:]/G) * N.log(psfc_data[:,:]/pcalc_data[k,:,:]))
        
        return z_data
    else:
        return pcalc_data




#----------------------------------------------------------------------
# Main program 
# 
if __name__ == "__main__":
    
    # command line options
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="file", type="string", help="WRF file")
    parser.add_option("-p", "--plotfile", dest="plotfile", type="string", help="name of output file")
    (options, args) = parser.parse_args()

    if options.file == None:
        print
        print "You must supply a wrfout file..."
        print "For example:  -f ./wrfout_d02_2010-06-13_18:00:00"
        print "Exiting."
        sys.exit()
    else:
        print
        print "Using the file:", options.file
        print 
    
    if options.plotfile == None:
        pname = "test_eta.pdf"
    else:
        pname = options.plotfile
    
    
    # open the input files for reading
    wrfnc = netCDF4.Dataset(options.file, 'r')
    
    # convert
    zdata = convert_eta(wrfnc, 'Z')
    #zdata = convert_eta(wrfnc, 'p')
    
    # close file
    wrfnc.close()
    
    
    # number of levels
    s = N.shape(zdata)
    print "You have %s vertical levels." % str(s[0])
    
    # take mean of grid
    zmean = N.zeros([s[0]])
    for l in range(s[0]):
        zmean[l] = N.mean(zdata[l,:,:])
    
    print "Mean height in km for model level 5: ", zmean[5]/1000.
    print "Mean height in km for model level 6: ", zmean[6]/1000.
    print "Mean height in km for model level 8: ", zmean[8]/1000.
    print "Mean height in km for model level 14: ", zmean[14]/1000.
    print "Mean height in km for model level 15: ", zmean[15]/1000.
    print "Mean height in km for model level 20: ", zmean[20]/1000.
    
    # calculate spacing
    zdiff = N.zeros([s[0]])
    for l in range(s[0]-1):
        zdiff[l] = zmean[l+1] - zmean[l]
       

   #----------------------------------------------------------------------
    # plot the heights
    fig = plt.figure(figsize=(8.,12.))
    ax = fig.add_subplot(111)
    
    # plot heights and spacing
    ax.plot(zdiff[:], zmean[:]/1000., 'ro-')
    ax.set_ylim(0,4)
    ax.set_xlim(0,700)
    ax.set_ylabel("Height (km)")
    ax.set_xlabel("Spacing (m)")

    # pressure plot
    #ax.plot(zdiff[:]/100., zmean[:]/100., 'ro-')
    #ax.set_ylim(1000,4)
    #ax.set_ylabel("Pressure (mb)")
    #ax.set_xlabel("Spacing (mb)")

    ax.grid(True)
    
    plt.savefig(pname)
    plt.show()
    
    

    
