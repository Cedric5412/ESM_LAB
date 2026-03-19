import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder
output_folder = './Plots/'
os.makedirs(output_folder, exist_ok=True)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")


# Computed PET
# ================================================================

timmean_fluxes = data_path / "fluxes_ymonmean.nc"    # Annual cycle of all the fluxes W m-2

ds = xr.open_dataset(timmean_fluxes)
toamasina_box = ds.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48.0, 50.0))

ds_toamasina = toamasina_box.mean(dim=['longitude', 'latitude'])

# Radiative forcing
swf = ds_toamasina.avg_snswrf
lwf = ds_toamasina.avg_snlwrf
Rs = lwf + swf

L = 2.5e6
pet = Rs/(1000*L) * 8.64*10**7
#================================================================


# ERA5 P, E, PET and T
tp_file = data_path / "tp_ymonmean.nc"      
e_file = data_path / "e_ymonmean.nc"        
pev_file = data_path / "pev_ymonmean.nc"  
t2m_file = data_path / "t2m_ymonmean.nc"  
runoff_file = data_path / "runoff_1991_2020_ymonmean.nc"
soilm_file = data_path / "moisture_1991_2020_ymonmean.nc"

precip = xr.open_dataset(tp_file)
evapor = xr.open_dataset(e_file)
pevapor = xr.open_dataset(pev_file)
temperature = xr.open_dataset(t2m_file)
runoff = xr.open_dataset(runoff_file)
moisture = xr.open_dataset(soilm_file)

print('---- Data successfully opened ----')

tp = precip['tp']
ev = np.abs(evapor['e'])
pev = np.abs(pevapor['pev'])
temp = temperature['t2m']
runo = runoff['ro']
sm = moisture['swvl1'] + moisture['swvl2'] + moisture['swvl3'] + moisture['swvl4'] 

precip_tomasina = tp.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

evapor_tomasina = ev.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

pev_tomasina = pev.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

temp_toamasina = temp.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
runoff_tomasina = runo.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

sm_toamasina = sm.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

# Convert to mm/day
tp_f = precip_tomasina * 1000.0
ev_f = evapor_tomasina * 1000.0
pev_f = pev_tomasina * 1000.0
runo_f = runoff_tomasina * 1000.0
soilm_f = sm_toamasina
temp_f = temp_toamasina - 273.15

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax1 = plt.subplots(figsize=(12,8))

ax1.plot(months, tp_f, 'b--', lw=2.5, label='P')
# ax1.bar(months, tp_f, alpha=0.5, color='darkslategray', label='P', width=0.4)
ax1.plot(months, ev_f, 'r--', lw=2.5, label='E')
# ax1.plot(months, pev_f, 'k-', lw=2.5, label='PET')
ax1.plot(months, pet, 'k-',  lw=2.5, label='PET')
ax1.plot(months, runo_f, color = 'orange', linestyle='--', lw=2.5, label=r'$\Delta f$')

ax1.tick_params(direction='in', which='both', top=True)
ax1.set_ylabel('Height (mm/day)', fontsize=14)
ax1.tick_params(colors='black', labelsize=14)

ax2 = ax1.twinx()
ax2.plot(months, temp_f, '-', color='purple', marker='o', lw=2.5, label='T')
ax2.set_ylabel(r'Temperature ($^{\circ} C$)', fontsize=14, color='purple')
ax2.tick_params('y', colors='purple', direction='in', labelsize=14)

ax3 = ax1.twinx()
ax3.plot(months, soilm_f, lw=2.5, color='green', marker='o', label='SM')
ax3.spines['right'].set_position(('outward', 80))
ax3.set_ylabel(r'Soil moisture ($m^3/m^3$)', color='green', fontsize=14)
ax3.tick_params('y', colors='green', labelsize=14, direction='in')


lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
lines = lines1 + lines2 + lines3
labels = labels1 + labels2 + labels3
plt.legend(lines, labels, loc='upper center', fontsize=14, frameon=False, ncol=2)
fname = os.path.join(output_folder, 'Water_balance_toamasina.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
