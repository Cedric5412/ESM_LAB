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

local_pathsw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/net_zonmean_sw.nc')
dssw = xr.open_dataset(local_pathsw)

local_pathlw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/net_zonmean_lw.nc')
dslw = xr.open_dataset(local_pathlw)

print("Data loaded successfully.")

sw = dssw['avg_snswrf'].isel(lon=0).mean('valid_time')  
lw = np.abs(dslw['avg_snlwrf'].isel(lon=0).mean('valid_time'))

def annual_flux(sw_data, lw_data, title, ax):

    # Both on same axes
    ax.plot(sw_data.lat, sw_data.values, linewidth=3, label='Net SW')
    ax.plot(lw_data.lat, lw_data.values, linewidth=3, label='Net LW')
    
    ax.set_title(title, fontweight='bold', pad=20, fontsize=14)
    ax.set_xlabel('Latitude', fontsize=13)
    ax.set_ylabel('Net Flux (W m$^{-2}$)',  fontsize=13)

    y_labels = [60, 90, 120, 150, 180, 210, 240, 270, 300]
    ax.set_yticks(y_labels)
    ax.set_yticklabels(['60', '90', '120', '150', '180', '210', '240', '270', '300'], fontsize=13)

    lat_ticks = [-90, -60, -30, 0, 30, 60, 90]
    ax.set_xticks(lat_ticks)
    ax.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'], fontsize=13)
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    

# Usage (drop-in replacement)
fig, ax = plt.subplots(figsize=(12, 8))
title = 'Zonal mean TOA radiation fluxes \n (ERA5 1991-2020)'
annual_flux(sw, lw, title, ax)
plt.tight_layout()
fname = os.path.join(output_folder, 'Zonal_curve.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

