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

timmean_fluxes = data_path / "fluxes_ymonmean.nc"    # Annual cycle of all the fluxes W m-2

ds = xr.open_dataset(timmean_fluxes)
print('---- Data successfully opened ----')
toamasina_box = ds.sel(
    latitude=slice(-17.50, -18.50),    
    longitude=slice(49.00, 49.50)    
)

ds_toamasina = toamasina_box.mean(dim=['longitude', 'latitude'])

# Radiative forcing
swf = ds_toamasina.avg_snswrf
lwf = ds_toamasina.avg_snlwrf
Rs = lwf + swf

# Outflux
shf = np.abs(ds_toamasina.avg_ishf)
lhf = np.abs(ds_toamasina.avg_slhtf)

# Ground heat flux
G = Rs - (shf + lhf)


months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

plt.figure(figsize=(10, 8))
plt.plot(months, Rs, 'k', lw=1.5, label='R$_n$')
plt.plot(months, lhf, 'b--', lw=1.5, label='LE')
plt.plot(months, shf, 'r--', lw=1.5, label='SH')
plt.plot(months, G, color='orange', ls='--', lw=1.5, label='G')
plt.tick_params(direction='in', which='both', top=True, right=True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('W m$^{-2}$', fontsize=14)
plt.legend(fontsize=14, loc='upper center', frameon=False)

fname = os.path.join(output_folder, 'Toamasina.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

