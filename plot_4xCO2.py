import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")
os.makedirs('./Plots/', exist_ok=True)

tas_4xCO2_file = xr.open_dataset(data_path / "tas_FIO_4xCO2_global.nc").squeeze()
pr_4xCO2_file = xr.open_dataset(data_path / "pr_FIO_4xCO2_global.nc").squeeze()
tas_historical_file = xr.open_dataset(data_path / "tas_FIO_historical.nc").squeeze()
pr_historical_file = xr.open_dataset(data_path / "pr_FIO_historical.nc").squeeze()

tas_4xCO2 = tas_4xCO2_file.tas - 273.15
tas_historical = tas_historical_file.tas - 273.15

rolling_10yr = tas_4xCO2.rolling(time=120, center=True).mean().dropna('time')

fig, ax = plt.subplots(figsize=(9, 6))
years_raw = tas_4xCO2.time.dt.year.values
ax.plot(years_raw, tas_4xCO2.values, alpha=0.5, color='black', linewidth=0.8)
years_roll = rolling_10yr.time.dt.year.values
ax.plot(years_roll, rolling_10yr.values, linewidth=3, color='darkred', label='10-year RM')
ax.tick_params(direction='in')
plt.ylabel('Temperature (°C)', fontsize=12)
plt.xlabel('Year', fontsize=12)
# plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

plt.tight_layout()
plt.savefig('./Plots/FIO_4xCO2_rolling10yr.png', dpi=300, bbox_inches='tight')
plt.show()

