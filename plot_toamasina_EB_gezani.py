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

gezani_fluxes = data_path / "february_2026_fluxes.nc"    #  Hourly fluxes W m-2

ds = xr.open_dataset(gezani_fluxes)
print('---- Data successfully opened ----')

toamasina_box = ds.sel(
    latitude=slice(-18.00, -18.50),    
    longitude=slice(49.00, 49.50)    
)

ds_toamasina = toamasina_box.mean(dim=['longitude', 'latitude'])
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

plt.figure(figsize=(14, 8))
plt.plot(time_ax, Rs, 'k', lw=1.5, label='R$_n$')
plt.plot(time_ax, lhf, 'b--', lw=1.5, label='LE')
plt.plot(time_ax, shf, 'r--', lw=1.5, label='SH')
plt.plot(time_ax, G, color='orange', ls='--', lw=1.5, label='G')
plt.tick_params(direction='in', which='both', top=True, right=True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('W m$^{-2}$', fontsize=14)
plt.legend(fontsize=14, loc='upper center', frameon=False)

fname = os.path.join(output_folder, 'Gezani_Toamasina.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

