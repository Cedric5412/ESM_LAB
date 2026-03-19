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

file_path = '/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6/drought_severity.rgb'

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")

# era5 = xr.open_dataset(data_path / "water_balance_ERA5_global.nc").squeeze()
mpi  = xr.open_dataset(data_path / "evspsbl_Amon_MPI_global.nc").squeeze()
fio  = xr.open_dataset(data_path / "evspsbl_Amon_FIO_global.nc").squeeze()


# era5_evapo = -1000*era5.e
mpi_evapo  = 86400*mpi.evspsbl 
fio_evapo  = 86400*fio.evspsbl

def plot_global_evapo(field, title, filename):

    levels = np.arange(0, 6.5, 0.5)

    fig, ax = plt.subplots(figsize=(8, 5),
                           subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
    
    im = ax.contourf(field.lon, field.lat, field.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.rain, 
                     levels=levels,
                     extend='max')
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40, label='mm/day')
    plt.subplots_adjust(bottom=0.15)
    fname = os.path.join(output_folder, filename)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")

# Individual plots
# plot_global_evapo(era5_evapo, 'ERA5 ', 'ERA5_ev_global.png')
plot_global_evapo(mpi_evapo,  'MPI-ESM1-2-HR', 'MPI_ev_regrid.png')
plot_global_evapo(fio_evapo,  'FIO-ESM-2-0',   'FIO_ev_regrid.png')
