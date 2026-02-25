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

path_1 = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/ERA5_diff_t2m.nc')
ds1 = xr.open_dataset(path_1)

path_2 = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/annual_t2m.nc')
ds2 = xr.open_dataset(path_2)

print("Data loaded successfully.")

# Data 1
t2m = ds1['t2m'].isel(valid_time=0)
t2m_north = t2m.sel(latitude=slice(90, 0), longitude=slice(0, 360))

# Data 2
t2m_zonmean = ds2['t2m'].isel(valid_time=0).mean(dim='longitude') 
t2m_anom = ds2['t2m'].isel(valid_time=0) - t2m_zonmean
t2m_north_anom = t2m_anom.sel(latitude=slice(90, 0), longitude=slice(0, 360))

def Global_plot(dataset, title, ax):
    data_min = float(dataset.min())
    data_max = float(dataset.max())
    levels = np.linspace(data_min, data_max, 7)

    cs = ax.contour(dataset.longitude, dataset.latitude, dataset,
                    transform=ccrs.PlateCarree(),
                    levels=levels,  cmap='coolwarm'
                    , linewidths=0.6)

    
    ax.clabel(cs, inline=True, fontsize=10, fmt='%.1f')
    ax.coastlines(resolution='110m', alpha=0.2)
    ax.set_title(title, fontweight='bold', fontsize=10)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='black', alpha=0.2, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}
    return cs  

# plot 1
fig = plt.figure(figsize=(12, 8))
title = ''
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
im1 = Global_plot(t2m_north, title, ax)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 't2m_seasonal_amp.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

# plot 2
fig = plt.figure(figsize=(12, 8))
title = ''
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
im1 = Global_plot(t2m_north_anom, title, ax)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 't2m_zonal_anom.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')