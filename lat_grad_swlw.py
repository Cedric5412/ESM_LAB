import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean 
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

local_pathsw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_zonalmean_sw.nc')
dssw = xr.open_dataset(local_pathsw)

local_pathlw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_zonalmean_lw.nc')
dslw = xr.open_dataset(local_pathlw)

print("Data loaded successfully.")

sw = dssw['avg_tnswrf'].isel(lon=0).mean('valid_time')  
lw = np.abs(dslw['avg_tnlwrf'].isel(lon=0).mean('valid_time'))
net_flux = sw - lw

def annual_flux(sw_data, lw_data, net_flux, title):

    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(14,9))

    ax1.plot(sw_data.lat, sw_data.values, linewidth=3, label='SW')
    ax1.plot(lw_data.lat, lw_data.values, linewidth=3, label='LW')
    ax1.set_title(title, fontweight='bold', pad=20, fontsize=14)
    ax1.set_ylabel('Net flux (W m$^{-2}$)',  fontsize=13)
    ax1.grid(True, alpha=0.3)

    lat_ticks = [-90, -60, -30, 0, 30, 60, 90]
    ax1.set_xticks(lat_ticks)
    ax1.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'], fontsize=13)
    ax1.set_xlim(np.min(lat_ticks), np.max(lat_ticks))
    ax1.legend(loc='upper right', fontsize=13)
    ax1.spines[['top', 'right']].set_visible(False)
    ax1.tick_params(axis='both', labelsize=13)

    
    ax2.plot(net_flux.lat, net_flux.values, linewidth=3, label=r'SW $-$ LW')
    ax2.legend(loc='upper right', fontsize=13)
    ax2.set_xlabel('Latitude', fontsize=13)
    ax2.set_ylabel('Net flux (W m$^{-2}$)',  fontsize=13)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.tick_params(axis='both', labelsize=13)
    ax2.grid(True, alpha=0.3)
   

   

title = 'Zonal mean TOA radiation fluxes \n (ERA5 1991-2020)'
annual_flux(sw, lw, net_flux, title)
plt.tight_layout()
fname = os.path.join(output_folder, 'Zonal_curve.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

