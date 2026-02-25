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

local_path = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/sig.nc')

ds = xr.open_dataset(local_path)

print("Data loaded successfully.")

sigma_t2m = ds['tmp'].isel(time=0)


def Global_plot(dataset, title, ax):
    im = ax.contourf(dataset.lon, dataset.lat, dataset.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.balance, 
                     levels=10
                     )
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    # ax.add_feature(cf.OCEAN, edgecolor='black', zorder=0.5, facecolor='white')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    return im


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8),
                        subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))

title = '2m temperature STD ($K$)\n(ERA5 1991-2020)'
im1 = Global_plot(sigma_t2m, title, ax)

cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'sigma_t2m.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
