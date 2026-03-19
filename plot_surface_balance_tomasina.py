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

timmean_fluxes = data_path / "fluxes_ymonmean.nc"    

ds = xr.open_dataset(timmean_fluxes)
print('---- Data successfully opened ----')
toamasina_box = ds.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48.0, 50.0))

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

plt.figure(figsize=(12, 8))
plt.plot(months, Rs, 'k', lw=2.5, label='R$_n$')
plt.plot(months, lhf, 'b--', lw=2.5, label='LE')
plt.plot(months, shf, 'r--', lw=2.5, label='SH')
plt.plot(months, G, color='orange', ls='--', lw=2.5, label=r'$G+\Delta F$')
plt.tick_params(direction='in', which='both', top=True, right=True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('W m$^{-2}$', fontsize=14)
plt.legend(fontsize=14, loc='upper center', frameon=False)

fname = os.path.join(output_folder, 'Toamasina_surface_balance.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

