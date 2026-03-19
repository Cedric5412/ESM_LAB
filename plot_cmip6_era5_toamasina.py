import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import os

# Creates output folder
output_folder = './Plots/'
os.makedirs(output_folder, exist_ok=True)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6/Ymon_mean")

era5_file = data_path / "water_balance_ERA5_annualcycle.nc"      
mpi_pr_file = data_path / "MPI_ESM1_pr_annualcycle_regridded.nc"        
fio_pr_file = data_path / "pr_FIO-ESM-annualcycle_regridded.nc"  

fio_evap_file = data_path / "evap_FIO_ESM_1981-2010_regridded_ymonmean.nc"  
mpi_evap_file = data_path / "evap_MPI_ESM1_1981-2010_regridded_ymonmean.nc"

era5_temp_file = data_path / "t2m_ERA5_annualcycle.nc"
fio_tas_file = data_path / "tas_FIO-ESM-annualcycle_regridded.nc"
mpi_tas_file = data_path / "MPI_ESM_tas_annualcycle_regridded.nc"

# Loading 
era5_tp_ev = xr.open_dataset(era5_file).squeeze()
mpi_pr = xr.open_dataset(mpi_pr_file).squeeze()
fio_pr = xr.open_dataset(fio_pr_file).squeeze()

fio_evap = xr.open_dataset(fio_evap_file)
mpi_evap = xr.open_dataset(mpi_evap_file)

era5_temp = xr.open_dataset(era5_temp_file)
fio_tas = xr.open_dataset(fio_tas_file)
mpi_tas = xr.open_dataset(mpi_tas_file)

tp_era5 = 1000*era5_tp_ev.tp.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
pr_mpi = 86400*mpi_pr.pr.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
pr_fio = 86400*fio_pr.pr.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

ev_era5 = -1000*era5_tp_ev.e.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
evspsbl_mpi = 86400*mpi_evap.evspsbl.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])
evspsbl_fio = 86400*fio_evap.evspsbl.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude'])

t2m_era5 = era5_temp.t2m.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude']) - 273.15
tas_mpi = mpi_tas.tas.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude']) - 273.15
tas_fio = fio_tas.tas.sel(latitude=slice(-15.0, -20.0), longitude=slice(48, 50)).mean(dim=['longitude', 'latitude']) - 273.15

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,12), 
                               sharex=True, height_ratios=[2,1])

ax1.plot(months, pr_fio, 'teal', lw=3, label='FIO-ESM-2-0')
ax1.plot(months, tp_era5, 'k', lw=3, label='ERA5')
ax1.plot(months, pr_mpi, color='indianred', lw=3, label='MPI-ESM1-2-HR')


ax1.plot(months, evspsbl_fio, 'teal', linestyle='--', lw=3, label='FIO-ESM-2-0')
ax1.plot(months, ev_era5, 'k--', lw=4, label='ERA5')
ax1.plot(months, evspsbl_mpi, 'indianred', linestyle='--', lw=3, label='MPI-ESM1-2-HR')


ax1.tick_params(direction='in', which='both', top=True)
ax1.set_ylabel('P, E (mm/day)', fontsize=14)
ax1.tick_params(colors='black', labelsize=14)
ax1.legend(fontsize=14, frameon=False, ncol=2)

ax2.plot(months, tas_fio, 'teal', lw=3, label='FIO-ESM-2-0')
ax2.plot(months, t2m_era5, 'k', lw=3, label='ERA5')
ax2.plot(months, tas_mpi, 'indianred', lw=3, label='MPI-ESM1-2-HR')


ax2.tick_params(direction='in', which='both', top=True)
ax2.set_ylabel('T (°C)', fontsize=14)
ax2.tick_params(colors='black', labelsize=14)
ax2.set_xlabel('Month', fontsize=14)
ax2.legend(fontsize=14, frameon=False, ncol=1, loc='upper center')

plt.tight_layout()
fname = os.path.join(output_folder, 'CMIP_seasonal_cycle_temp.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')
# plt.show()