import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import os
import cmocean

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")
os.makedirs('./Plots/', exist_ok=True)

era5_MPI = xr.open_dataset(data_path / "water_balance_ERA5_global_MPI.nc").squeeze()
era5_FIO = xr.open_dataset(data_path / "water_balance_ERA5_global_FIO.nc").squeeze()
mpi  = xr.open_dataset(data_path / "MPI_ESM1_pr_global.nc").squeeze()
fio  = xr.open_dataset(data_path / "FIO_ESM_pr_global.nc").squeeze()

era5_MPI_precip = 1000*era5_MPI.tp
era5_FIO_precip = 1000*era5_FIO.tp
mpi_precip  = 86400*mpi.pr 
fio_precip  = 86400*fio.pr

# === COMPUTE BIAS ===
# CDO remapbil created perfect grids, need to reassign dims explicitly
mpi_bias_field = xr.DataArray(
    mpi_precip.values - era5_MPI_precip.values,
    dims=['lat', 'lon'],
    coords={'lat': mpi_precip.lat, 'lon': mpi_precip.lon}
)

fio_bias_field = xr.DataArray(
    fio_precip.values - era5_FIO_precip.values,
    dims=['lat', 'lon'],
    coords={'lat': fio_precip.lat, 'lon': fio_precip.lon}
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
    ax.set_global()
    return im

levels = np.linspace(-5, 5, 11)

# === FIGURE ===
fig, axs = plt.subplots(
    1, 2,
    figsize=(10, 5),
    subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180))
)

im1 = Global_plot(mpi_bias_field, 'a) MPI-ESM1-2-HR', axs[0], levels)
im2 = Global_plot(fio_bias_field, 'b) FIO-ESM-2-0', axs[1], levels)

cbar1 = plt.colorbar(im1, ax=axs[0], orientation='horizontal', shrink=0.8, pad=0.1, aspect=30)
cbar1.set_label('Bias (mm/day)', fontsize=12)
cbar2 = plt.colorbar(im2, ax=axs[1], orientation='horizontal', shrink=0.8, pad=0.1, aspect=30)
cbar2.set_label('Bias (mm/day)', fontsize=12)

plt.tight_layout()
plt.savefig('./Plots/pr_bias_MPI_vs_FIO.png', dpi=300, bbox_inches='tight')
plt.show()