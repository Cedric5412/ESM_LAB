import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import os
import cmocean

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6/FIO_ESM")
os.makedirs('./Plots/', exist_ok=True)

# Load data
tas_FIO_historical_file = xr.open_dataset(data_path / "tas_FIO_historical_timmean.nc").squeeze()
tas_FIO_4xCO2_file = xr.open_dataset(data_path / "tas_FIO_4xCO2_timmean.nc").squeeze()
olr_FIO_historical_file = xr.open_dataset(data_path / "rlut_FIO_historical_timmean.nc").squeeze()
olr_FIO_4xCO2_file = xr.open_dataset(data_path / "rlut_FIO_4xCO2_timmean.nc").squeeze()
pr_FIO_historical_file = xr.open_dataset(data_path / "pr_FIO_historical_timmean.nc").squeeze()
pr_FIO_4xCO2_file = xr.open_dataset(data_path / "pr_FIO_4xCO2_timmean.nc").squeeze()

tas_FIO_historical = tas_FIO_historical_file.tas - 273.15
tas_FIO_4xCO2 = tas_FIO_4xCO2_file.tas - 273.15
olr_FIO_historical = olr_FIO_historical_file.rlut
olr_FIO_4xCO2 = olr_FIO_4xCO2_file.rlut 
pr_FIO_historical = 86400 * pr_FIO_historical_file.pr 
pr_FIO_4xCO2 = 86400 * pr_FIO_4xCO2_file.pr

# Compute differences
tas_diff = tas_FIO_4xCO2 - tas_FIO_historical
olr_diff = olr_FIO_4xCO2 - olr_FIO_historical  
pr_diff = pr_FIO_4xCO2 - pr_FIO_historical

# Define levels 
pr_levels = np.linspace(0, 10, 11)  
pr_diff_levels = np.linspace(-3, 3, 11)     
olr_levels = 11                              
tas_levels = np.linspace(-30, 30, 13)       
tas_diff_levels = np.linspace(-10, 10, 11)   

# Colormap 
colormaps = {
    'OLR': 'turbo',
    'PR': cmocean.cm.rain,      
    'PR_diff': cmocean.cm.tarn, 
    'TAS': 'coolwarm'
}

def Global_plot(dataset, title, ax, levels, var_type, is_diff=False):
    if var_type == 'PR_diff':
        cmap = colormaps['PR_diff']
    else:
        cmap = colormaps[var_type]
    
    extend = 'both' if is_diff else 'neither'
    
    im = ax.contourf(
        dataset.lon,
        dataset.lat,
        dataset,
        transform=ccrs.PlateCarree(),
        cmap=cmap,
        levels=levels,
        extend=extend
    )
    ax.coastlines(resolution='110m')
    ax.gridlines(linestyle='--', alpha=0.2)
    ax.set_title(title, fontweight='bold', fontsize=9)
    return im

# === FIGURE 1: OLR ===
fig1, axs1 = plt.subplots(1, 3, figsize=(12, 6), subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
im1_1 = Global_plot(olr_FIO_historical, 'OLR Historical', axs1[0], olr_levels, 'OLR', False)
im1_2 = Global_plot(olr_FIO_4xCO2, 'OLR 4xCO2', axs1[1], olr_levels, 'OLR', False)
im1_3 = Global_plot(olr_diff, 'OLR 4xCO2 - H', axs1[2], olr_levels, 'OLR', True)

cbar1_1 = plt.colorbar(im1_1, ax=axs1[0], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar1_1.set_label('W m$^{-2}$', fontsize=8)
cbar1_2 = plt.colorbar(im1_2, ax=axs1[1], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar1_2.set_label('W m$^{-2}$', fontsize=8)
cbar1_3 = plt.colorbar(im1_3, ax=axs1[2], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar1_3.set_label('W m$^{-2}$', fontsize=8)
plt.subplots_adjust(bottom=0.2, top=0.85, wspace=0.1)
plt.savefig('./Plots/FIO_OLR_4xCO2.png', dpi=300, bbox_inches='tight')

# === FIGURE 2: PRECIP ===
fig2, axs2 = plt.subplots(1, 3, figsize=(12, 6), subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
im2_1 = Global_plot(pr_FIO_historical, 'P Historical', axs2[0], pr_levels, 'PR', True)
im2_2 = Global_plot(pr_FIO_4xCO2, 'P 4xCO2', axs2[1], pr_levels, 'PR', True)
im2_3 = Global_plot(pr_diff, 'P 4xCO2 - H', axs2[2], pr_diff_levels, 'PR_diff', True)

cbar2_1 = plt.colorbar(im2_1, ax=axs2[0], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar2_1.set_label('mm day$^{-1}$', fontsize=8)
cbar2_2 = plt.colorbar(im2_2, ax=axs2[1], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar2_2.set_label('mm day$^{-1}$', fontsize=8)
cbar2_3 = plt.colorbar(im2_3, ax=axs2[2], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar2_3.set_label('mm day$^{-1}$', fontsize=8)
plt.subplots_adjust(bottom=0.1, top=0.85, wspace=0.1)
plt.savefig('./Plots/FIO_PR_4xCO2.png', dpi=300, bbox_inches='tight')

# === FIGURE 3: TAS ===
fig3, axs3 = plt.subplots(1, 3, figsize=(12, 6), subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
im3_1 = Global_plot(tas_FIO_historical, 'T Historical', axs3[0], tas_levels, 'TAS', True)
im3_2 = Global_plot(tas_FIO_4xCO2, 'T 4xCO2', axs3[1], tas_levels, 'TAS', True)
im3_3 = Global_plot(tas_diff, 'T 4xCO2 - H', axs3[2], tas_diff_levels, 'TAS', True)

cbar3_1 = plt.colorbar(im3_1, ax=axs3[0], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar3_1.set_label('°C', fontsize=8)
cbar3_2 = plt.colorbar(im3_2, ax=axs3[1], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar3_2.set_label('°C', fontsize=8)
cbar3_3 = plt.colorbar(im3_3, ax=axs3[2], orientation='horizontal', shrink=0.8, pad=0.05, aspect=30)
cbar3_3.set_label('°C', fontsize=8)
plt.subplots_adjust(bottom=0.1, top=0.85, wspace=0.1)
plt.savefig('./Plots/FIO_TAS_4xCO2.png', dpi=300, bbox_inches='tight')

# plt.show()