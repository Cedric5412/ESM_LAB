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

ds = xr.open_dataset(tp_file)
print('---- Data successfully opened----')

tp_global = ds.tp * 1000.0 *30

tp_madagascar = tp_global.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 51))

tp_clim = tp_madagascar.sum(dim='valid_time')
tp_djfm = tp_madagascar.sel(valid_time=tp_madagascar.valid_time.dt.month.isin([12, 1, 2, 3])).sum(dim='valid_time')
tp_djfm_prop = (tp_djfm/tp_clim) * 100

def plot_global_field(field, title, filename):
    
    fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=180)))
    
    im = ax.contourf(field.longitude, field.latitude, field.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.tarn, 
                     levels=21)
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    ax.add_feature(cf.BORDERS, linewidth =2)
    ax.add_feature(cf.OCEAN, edgecolor='black', zorder=100, facecolor='white')
    # ax.set_extent([10, 52, -35, -5], crs=ccrs.PlateCarree())
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, ax=ax, orientation='vertical',label=r'$\%$')
    plt.subplots_adjust(bottom=0.15)
    plt.tight_layout()
    fname = os.path.join(output_folder, filename)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")


plot_global_field(tp_djfm_prop, '', 'Toam.png')
