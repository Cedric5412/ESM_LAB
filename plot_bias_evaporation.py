import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import os
import matplotlib.colors as mcolors
import cmocean


# === METRIC FUNCTION ===
def bias(model, obs):
    return float((model - obs).mean())

# === LOAD DATA ===
data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")
os.makedirs('./Plots/', exist_ok=True)

era5_MPI = xr.open_dataset(data_path / "water_balance_ERA5_global_MPI.nc").squeeze()
era5_FIO = xr.open_dataset(data_path / "water_balance_ERA5_global_FIO.nc").squeeze()
mpi  = xr.open_dataset(data_path / "evspsbl_Amon_MPI_global.nc").squeeze()
fio  = xr.open_dataset(data_path / "evspsbl_Amon_FIO_global.nc").squeeze()

era5_MPI_evap = -1000*era5_MPI.e
era5_FIO_evap = -1000*era5_FIO.e
mpi_evap  = 86400*mpi.evspsbl 
fio_evap  = 86400*fio.evspsbl

# === COMPUTE BIAS ===
mpi_bias_field = xr.DataArray(
    mpi_evap.values - era5_MPI_evap.values,
    dims=['lat', 'lon'],
    coords={'lat': mpi_evap.lat, 'lon': mpi_evap.lon}
)

fio_bias_field = xr.DataArray(
    fio_evap.values - era5_FIO_evap.values,
    dims=['lat', 'lon'],
    coords={'lat': fio_evap.lat, 'lon': fio_evap.lon}
)

# === PLOT FUNCTION ===
def Global_plot(dataset, title, ax, levels):
    im = ax.contourf(
        dataset.lon,
        dataset.lat,
        dataset,
        transform=ccrs.PlateCarree(),
        cmap=cmocean.cm.tarn,
        levels=levels,
        extend='both'
    )
    ax.coastlines(resolution='110m')
    ax.gridlines(linestyle='--', alpha=0.4)
    ax.set_title(title, fontweight='bold', fontsize=12)
    return im

levels = np.linspace(-2, 2, 9)

# === FIGURE ===
fig, axs = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(10, 5),
    subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180))
)

# Plot maps
im1 = Global_plot(mpi_bias_field, 'a) MPI-ESM1-2-HR', axs[0], levels=levels)
im2 = Global_plot(fio_bias_field, 'b) FIO-ESM-2-0', axs[1], levels=levels)

cbar1 = plt.colorbar(im1, ax=axs[0], orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40)
cbar1.set_label('Bias (mm/day)', fontsize=12)

cbar2 = plt.colorbar(im1, ax=axs[1], orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40)
cbar2.set_label('Bias (mm/day)', fontsize=12)

plt.tight_layout()
plt.savefig('./Plots/evap_bias_MPI_vs_FIO.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nBias computation and plotting complete.")
