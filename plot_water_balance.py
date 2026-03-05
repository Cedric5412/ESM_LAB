import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder
output_folder = './Plots/'
os.makedirs(output_folder, exist_ok=True)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")

tp_file = data_path / "tp_ymonmean.nc"      
e_file = data_path / "e_ymonmean.nc"        
pev_file = data_path / "pev_ymonmean.nc"    

precip = xr.open_dataset(tp_file)
evapor = xr.open_dataset(e_file)
pevapor = xr.open_dataset(pev_file)

print('---- Data successfully opened ----')

precip_tomasina = precip.sel(latitude=slice(-18, -18.50), 
                            longitude=slice(49.00, 49.50)).mean(dim=['longitude', 'latitude']).tp

evapor_tomasina = evapor.sel(latitude=slice(-18, -18.50), 
                            longitude=slice(49.00, 49.50)).mean(dim=['longitude', 'latitude']).e

pev_tomasina = pevapor.sel(latitude=slice(-18, -18.50), 
                          longitude=slice(49.00, 49.50)).mean(dim=['longitude', 'latitude']).pev

# Convert to mm/day
tp = precip_tomasina * 1000.0
e = evapor_tomasina * 1000.0
pev = pev_tomasina * 1000.0

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

plt.figure(figsize=(10, 8))
plt.plot(months, -pev, 'k-', lw=2.5, label='PET')
plt.plot(months, tp, 'b--', lw=2.5, label='P')
plt.plot(months, -e, 'r--', lw=2.5, label='E')

plt.tick_params(direction='in', which='both', top=True, right=True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel('mm/day', fontsize=14)
plt.legend(fontsize=14, loc='upper right')

fname = os.path.join(output_folder, 'Tomasina_Water_balance.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
