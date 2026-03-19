import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import os
import matplotlib.colors as mcolors
import cmocean

# === LOAD DATA ===
data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")
os.makedirs('./Plots/', exist_ok=True)

era5_mpi = xr.open_dataset(data_path / "t2m_ERA5_global_MPI.nc").squeeze()
era5_fio = xr.open_dataset(data_path / "t2m_ERA5_global_FIO.nc").squeeze()


mpi  = xr.open_dataset(data_path / "MPI_ESM_tas_global.nc").squeeze()
fio  = xr.open_dataset(data_path / "FIO_ESM_tas_global.nc").squeeze()

era5_temp_mpi = era5_mpi.t2m - 273.15
era5_temp_fio = era5_fio.t2m - 273.15

mpi_temp  = mpi.tas - 273.15
fio_temp  = fio.tas - 273.15

# === COMPUTE BIAS ===
mpi_bias_field = xr.DataArray(
    mpi_temp.values - era5_temp_mpi.values,
    dims=['lat', 'lon'],
    coords={'lat': mpi_temp.lat, 'lon': mpi_temp.lon}
)

fio_bias_field = xr.DataArray(
    fio_temp.values - era5_temp_fio.values,
    dims=['lat', 'lon'],
    coords={'lat': fio_temp.lat, 'lon': fio_temp.lon}
)
# === PLOT FUNCTION ===
def Global_plot(dataset, title, ax, levels):
    im = ax.contourf(
        dataset.lon,
        dataset.lat,
        dataset,
        transform=ccrs.PlateCarree(),
        cmap=cmocean.cm.balance,
        levels=levels,
        extend='both'
    )
    ax.coastlines(resolution='110m')
    ax.gridlines(linestyle='--', alpha=0.4)
    ax.set_title(title, fontweight='bold', fontsize=12)
    return im

levels = np.linspace(-5, 5, 11)

# === FIGURE ===
fig, axs = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(10, 5),
    subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180))
)

# Plot maps
im1 = Global_plot(mpi_bias_field, 'a) MPI-ESM1-2-HR', axs[0], levels)
im2 = Global_plot(fio_bias_field, 'b) FIO-ESM-2-0', axs[1], levels)

cbar1 = plt.colorbar(im1, ax=axs[0], orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40)
cbar1.set_label('Bias (°C)', fontsize=12)

cbar2 = plt.colorbar(im1, ax=axs[1], orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40)
cbar2.set_label('Bias (°C)', fontsize=12)

plt.tight_layout()
plt.savefig('./Plots/01_bias_MPI_vs_FIO.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nBias computation and plotting complete.")
