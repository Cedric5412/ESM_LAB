import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")

gezani_fluxes = data_path / "february_2026_fluxes.nc"    
gezani_surface_pressure = data_path / "surface_pressure.nc"

ds = xr.open_dataset(gezani_fluxes)
dt = xr.open_dataset(gezani_surface_pressure)

toamasina_flux = ds.sel(
    latitude=slice(-17.50, -18.50),    
    longitude=slice(49.00, 49.50)    
)   

toamasina_pressure = dt.sel(
    latitude=slice(-17.50, -18.50),    
    longitude=slice(49.00, 49.50)    
)

ds_toamasina = toamasina_flux.mean(dim=['longitude', 'latitude'])
dt_toamasina = toamasina_pressure.mean(dim=['longitude', 'latitude'])

time_ax = ds_toamasina.valid_time

# Radiative forcing
swf = ds_toamasina.avg_snswrf
lwf = ds_toamasina.avg_snlwrf
Rs = lwf + swf

# Outflux
shf = np.abs(ds_toamasina.avg_ishf)
lhf = np.abs(ds_toamasina.avg_slhtf)

# Ground heat flux
G = Rs - (shf + lhf)

# Pressures in hPa
sp = dt_toamasina.sp / 100
mslp = dt_toamasina.msl / 100

# Create combined plot with twin axes
fig, ax1 = plt.subplots(figsize=(14, 8))

# Left y-axis for fluxes (W m-2)
color = 'k'
ax1.set_xlabel('Time', fontsize=14)
ax1.set_ylabel('Surface Energy Fluxes (W m$^{-2}$)', fontsize=14, color=color)
ax1.plot(time_ax, Rs, 'k', lw=2, label='R$_n$')
ax1.plot(time_ax, lhf, 'b--', lw=2, label='LE')
ax1.plot(time_ax, shf, 'r--', lw=2, label='SH')
ax1.plot(time_ax, G, color='orange', ls='--', lw=2, label='G')
ax1.tick_params(axis='y', labelcolor=color, direction='in', which='both')
ax1.tick_params(axis='x', direction='in', which='both', top=True, right=True)
ax1.tick_params(labelsize=14)
ax1.legend(loc='upper left', fontsize=14, frameon=False)

# Right y-axis for pressures (hPa)
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Surface Pressure (hPa)', fontsize=14, color=color)
# ax2.plot(time_ax, sp, marker='o', lw=2, alpha=0.8, label='SP', color='green')
ax2.plot(time_ax, mslp, marker='o', lw=2, alpha=0.8, label='MSLP', color='green')
ax2.tick_params(axis='y', labelcolor=color, direction='in', which='both')
ax2.tick_params(labelsize=14, color='green')

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=14, loc='upper center', 
           frameon=False, ncol=2)

fname = os.path.join(output_folder, 'Gezani_Toamasina_combined.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
plt.show()
