# SCRIPT 1: PLOT REGRIDDED DATA (Your exact style)
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean
import matplotlib.colors as mcolors

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")

# Load regridded datasets
# era5 = xr.open_dataset(data_path / "t2m_ERA5_global.nc").squeeze()
mpi  = xr.open_dataset(data_path / "MPI_ESM_tas_global.nc").squeeze()
fio  = xr.open_dataset(data_path / "FIO_ESM_tas_global.nc").squeeze()


# era5_temp = era5.t2m
mpi_temp  = mpi.tas
fio_temp  = fio.tas


def plot_global_temp(field, title, filename):

    field = field -273.15
    levels = np.arange(-20, 34, 2)

    fig, ax = plt.subplots(figsize=(8, 5),
                           subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
    
    im = ax.contourf(field.lon, field.lat, field.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.balance, 
                     levels=levels,
                     extend='both')
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40, label=r'$^\circ$C')
    plt.subplots_adjust(bottom=0.15)
    fname = os.path.join(output_folder, filename)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

# Individual plots
# plot_global_temp(era5_temp, 'ERA5 t2m (1981-2010)', 'ERA5_t2m_global.png')
plot_global_temp(mpi_temp,  'MPI-ESM1-2-HR', 'MPI_tas_regrid.png')
plot_global_temp(fio_temp,  'FIO-ESM-2-0',   'FIO_tas_regrid.png')
