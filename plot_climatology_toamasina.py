import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")
tp_file = data_path / "tp_ymonmean.nc"      
t2m_file = data_path / "t2m_ymonmean.nc"  

precip = xr.open_dataset(tp_file)
temperature = xr.open_dataset(t2m_file)

tp = 1000*precip['tp'].mean(dim='valid_time').sel(latitude=slice(-11.5, -26.0), 
                            longitude=slice(42, 52))
temp = temperature['t2m'].mean(dim='valid_time').sel(latitude=slice(-11.5, -26.0), 
                            longitude=slice(42, 52))

temp = temp - 273.15

def plot_global_field(field, title, filename):
    fig, ax = plt.subplots(figsize=(8, 12),
                           subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0)))
    
    im = ax.contourf(field.longitude, field.latitude, field.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.balance ,
                     levels=14
                     )
    
    ax.coastlines(resolution='110m', lw=2)
    ax.set_title(title, fontweight='bold', pad=20)
    ax.set_extent([42, 52, -26, -11.5], crs=ccrs.PlateCarree())
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=20, label=r'$^{\circ} C$')
    plt.subplots_adjust(bottom=0.15)
    fname = os.path.join(output_folder, filename)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    # plt.show()
    plt.close()
   
    print(f"Saved: {filename}")


plot_global_field(temp, '', 'Temp.png')
# plot_global_field(tp, '', 'Precip.png')

