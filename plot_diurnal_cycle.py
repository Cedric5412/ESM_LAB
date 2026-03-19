import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder
output_folder = './Plots/'
os.makedirs(output_folder, exist_ok=True)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/Diurnal")


# # Computed PET
# # ================================================================

# timmean_fluxes = data_path / "fluxes_ymonmean.nc"    # Annual cycle of all the fluxes W m-2

# ds = xr.open_dataset(timmean_fluxes)
# toamasina_box = ds.sel(latitude=slice(-15.0, -20.0), 
#                             longitude=slice(48.0, 50.0))

# ds_toamasina = toamasina_box.mean(dim=['longitude', 'latitude'])

# # Radiative forcing
# swf = ds_toamasina.avg_snswrf
# lwf = ds_toamasina.avg_snlwrf
# Rs = lwf + swf

# L = 2.5e6
# pet = Rs/(1000*L) * 8.64*10**7
# #================================================================

# Not automatized, change the input 
#======= wet month ================================
# water_balance_file1 = data_path / "era5_water_balance_feb2026_diurnal.nc"
# t2m_sm_file1 = data_path / "era5_t2m_swl1_feb2026_diurnal.nc"

# wb_wet = xr.open_dataset(water_balance_file1).squeeze()
# temp_sm_wet = xr.open_dataset(t2m_sm_file1).squeeze()

# = ====  dry month =================================
water_balance_file2 = data_path / "era5_water_balance_sep2025_diurnal.nc"
t2m_sm_file2 = data_path / "era5_t2m_swl1_sep2025_diurnal.nc"

wb_dry = xr.open_dataset(water_balance_file2).squeeze()
temp_sm_dry = xr.open_dataset(t2m_sm_file2).squeeze()

print('---- Data successfully opened ----')

tp_wet = wb_dry['tp']
ev_wet = np.abs(wb_dry['e'])
pev_wet = np.abs(wb_dry['pev'])
runo_wet = wb_dry['ro']

temp_wet = temp_sm_dry['t2m']
sm_wet = temp_sm_dry['swvl1'] 

precip_tomasina = tp_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

evapor_tomasina = ev_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

pev_tomasina = pev_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

temp_toamasina = temp_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
runoff_tomasina = runo_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

sm_toamasina = sm_wet.sel(latitude=slice(-15.0, -20.0), 
                            longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

# Convert to mm/day
tp_f = precip_tomasina * 1000.0
ev_f = evapor_tomasina * 1000.0
pev_f = pev_tomasina * 1000.0
runo_f = runoff_tomasina * 1000.0
soilm_f = sm_toamasina
temp_f = temp_toamasina - 273.15

hours = np.arange(0, 24, 1)

fig, ax1 = plt.subplots(figsize=(12,8))

ax1.plot(hours, tp_f, 'b--', lw=2.5, label='P')
# ax1.bar(hours, tp_f, alpha=0.5, color='darkslategray', label='P', width=0.4)
ax1.plot(hours, ev_f, 'r--', lw=2.5, label='E')
ax1.plot(hours, pev_f, 'k-', lw=2.5, label='PET')
# ax1.plot(hours, pet, 'k-',  lw=2.5, label='PET')
ax1.plot(hours, runo_f, color = 'orange', linestyle='--', lw=2.5, label=r'$\Delta f$')

ax1.tick_params(direction='in', which='both', top=True)
ax1.set_ylabel('Height (mm/day)', fontsize=14)
ax1.set_xlabel('Hours', fontsize=14)
ax1.tick_params(colors='black', labelsize=14)

ax2 = ax1.twinx()
ax2.plot(hours, temp_f, '-', color='purple', marker='o', lw=2.5, label='T')
ax2.set_ylabel(r'Temperature ($^{\circ} C$)', fontsize=14, color='purple')
ax2.tick_params('y', colors='purple', direction='in', labelsize=14)

ax3 = ax1.twinx()
ax3.plot(hours, soilm_f, lw=2.5, color='green', marker='o', label='SM')
ax3.spines['right'].set_position(('outward', 80))
ax3.set_ylabel(r'Soil moisture ($m^3/m^3$)', color='green', fontsize=14)
ax3.tick_params('y', colors='green', labelsize=14, direction='in')


lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
lines = lines1 + lines2 + lines3
labels = labels1 + labels2 + labels3
plt.legend(lines, labels, loc='upper right', 
           fontsize=14, frameon=False, ncol=3)
fname = os.path.join(output_folder, 'Dry_WB_dirnal_cycle.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
