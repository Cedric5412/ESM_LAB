import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean


# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

path_sw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_mean_sw.nc')
path_lw = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_mean_lw.nc')

ds_sw = xr.open_dataset(path_sw)
ds_lw = xr.open_dataset(path_lw)

print("Data loaded successfully.")

swr = ds_sw['avg_tnswrf'].isel(valid_time=0)
lwr = np.abs(ds_lw['avg_tnlwrf'].isel(valid_time=0))

def Global_plot(dataset, title, ax):
    im = ax.contourf(dataset.longitude, dataset.latitude, dataset,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.solar, levels=20, vmin = 0.8*dataset.min(), vmax = 1.2*dataset.max()
                     )
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.5, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    return im


# SW
fig = plt.figure(figsize=(12, 8))
title = 'Annual TOA SW flux (W m$^{-2}$)\n(ERA5 1991-2020)'
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide(central_longitude=180))
im1 = Global_plot(swr, title, ax)
cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'swr_era5_global.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

# LW
fig = plt.figure(figsize=(12, 8))
title = 'Annual TOA OLR flux (W m$^{-2}$)\n(ERA5 1991-2020)'
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide(central_longitude=180))
im2 = Global_plot(lwr, title, ax)
cbar = plt.colorbar(im2, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)

fname = os.path.join(output_folder, 'lwr_era5_global.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')