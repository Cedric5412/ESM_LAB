import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder
output_folder = './Plots/'
os.makedirs(output_folder, exist_ok=True)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/Diurnal")

flux_wet_file = data_path / "era5_energy_flux_feb2026_diurnal.nc"
flux_dry_file = data_path / "era5_energy_flux_sep2025_diurnal.nc"

flux_wet = xr.open_dataset(flux_wet_file).squeeze()
flux_dry = xr.open_dataset(flux_dry_file).squeeze()

in_data = flux_wet
# in_data = flux_dry


toamasina_box = in_data.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48.0, 50.0))

input_dat = toamasina_box.mean(dim=['longitude', 'latitude'])

# wet
swf = input_dat['avg_snswrf']
lwf = input_dat['avg_snlwrf']
Rs = swf + lwf

shf = np.abs(input_dat['avg_ishf'])
lhf = np.abs(input_dat['avg_slhtf'])
# Ground heat flux
G = Rs - (shf + lhf)


hours = np.arange(0, 24, 1)

plt.figure(figsize=(12, 8))
plt.plot(hours, Rs, 'k', lw=2.5, label='R$_n$')
plt.plot(hours, lhf, 'b--', lw=2.5, label='LE')
plt.plot(hours, shf, 'r--', lw=2.5, label='SH')
plt.plot(hours, G, color='orange', ls='--', lw=2.5, label=r'$G+\Delta F$')
plt.tick_params(direction='in', which='both', top=True, right=True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('W m$^{-2}$', fontsize=14)
plt.xlabel('Hours', fontsize=14)
plt.legend(fontsize=14, loc='upper right', frameon=False)

fname = os.path.join(output_folder, 'Wet_surface_energy_toamasina.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

