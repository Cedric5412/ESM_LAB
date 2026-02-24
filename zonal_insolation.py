import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm


# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

local_path = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_zonalmean_tdsw.nc')
ds = xr.open_dataset(local_path)

print("Data loaded successfully.")

val = ds['avg_tdswrf'].isel(lon=0)

def Zonal_plot(dataset, title, ax):
    # Set up color levels
    vmin, vmax = np.nanmin(val), np.nanmax(val)
    levels = np.linspace(vmin, vmax, 12)
    # Create a custom colormap where 0 values are white
    cmap = plt.get_cmap(cmocean.cm.thermal, len(levels) - 1)
    newcolors = cmap(np.linspace(0, 1, len(levels) - 1))

    # Identify which bin contains 0
    zero_index = np.digitize([0], levels)[0] - 1  # adjust to 0-based index

    # Replace color at zero bin with white
    if 0 <= zero_index < len(newcolors):
        newcolors[zero_index] = [1, 1, 1, 1]  # RGBA for white

    custom_cmap = ListedColormap(newcolors)
    norm = BoundaryNorm(levels, custom_cmap.N)

    im = ax.contourf(dataset.valid_time, dataset.lat, dataset.T, 
                      cmap=custom_cmap, norm=norm, levels=levels)
    
    ax.set_title(title, fontweight='bold', pad=20, fontsize=14)

    lat_ticks = [-90, -60, -30, 0, 30, 60, 90] 
    ax.set_yticks(lat_ticks)
    latitude_labels = ['90S', '60S', '30S', '0', '30N', '60N', '90N']
    ax.set_yticklabels(latitude_labels, fontsize=13)
    
    month_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    ax.set_xticks(dataset.valid_time[:12])  
    ax.set_xticklabels(month_labels, fontsize=13)
    
    return im

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111) 
title = 'Zonal Mean Insolation (W m$^{-2}$)\n(ERA5 1991-2020)'
im1 = Zonal_plot(val, title, ax)

# Customize colrbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.08)
cbar = plt.colorbar(im1, cax=cax, aspect=30)
cbar.ax.tick_params(labelsize=12)

plt.tight_layout()
fname = os.path.join(output_folder, 'solar_insolation_zonal.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

