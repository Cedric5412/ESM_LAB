import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import os
import cmocean

# === LOAD DATA ===
data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data/CMIP6")
os.makedirs('./Plots/', exist_ok=True)

# === LOAD DATA ===
era5_MPI = xr.open_dataset(data_path / "water_cycle_ERA5_1981_2010_MPI.nc").squeeze()
era5_FIO = xr.open_dataset(data_path / "water_cycle_ERA5_1981_2010_FIO.nc").squeeze()
mpi  = xr.open_dataset(data_path / "evspsbl_Amon_MPI-ESM1-2-HR_historical_r1i1p1f1_gn_19810116-20101216.nc").squeeze()
fio  = xr.open_dataset(data_path / "evspsbl_Amon_FIO-ESM-2-0_historical_r1i1p1f1_gn_19810116-20101216.nc").squeeze()

era5_MPI_evap = -1000*era5_MPI.e
era5_FIO_evap = -1000*era5_FIO.e
mpi_evap  = 86400*mpi.evspsbl 
fio_evap  = 86400*fio.evspsbl

# === MEMORY-EFFICIENT CORRELATION ===
def compute_spatial_corr(da_obs, da_model, chunk_size=50):
    """Compute spatial correlation gridpoint-by-gridpoint."""
    
    corr_result = np.full(da_obs.shape[1:], np.nan)
    
    for lat_start in range(0, da_obs.shape[1], chunk_size):
        lat_end = min(lat_start + chunk_size, da_obs.shape[1])
        
        print(f"Processing lat {lat_start}-{lat_end}...")
        
        obs_chunk = da_obs[:, lat_start:lat_end, :].values
        model_chunk = da_model[:, lat_start:lat_end, :].values
        
        for i_lat in range(obs_chunk.shape[1]):
            for i_lon in range(obs_chunk.shape[2]):
                obs_time = obs_chunk[:, i_lat, i_lon]
                model_time = model_chunk[:, i_lat, i_lon]
                
                if np.isnan(obs_time).sum() > len(obs_time)*0.5 or np.isnan(model_time).sum() > len(model_time)*0.5:
                    continue
                    
                corr_val = np.corrcoef(obs_time[~np.isnan(obs_time)], 
                                     model_time[~np.isnan(model_time)])[0,1]
                corr_result[lat_start+i_lat, i_lon] = corr_val
    

    return xr.DataArray(corr_result, 
                       coords={'lat': da_obs.lat, 'lon': da_obs.lon},
                       dims=['lat', 'lon'])

# === COMPUTE CORRELATIONS ===
print("Computing MPI correlations...")
mpi_corr = compute_spatial_corr(era5_MPI_evap, mpi_evap)
print("Computing FIO correlations...")
fio_corr = compute_spatial_corr(era5_FIO_evap, fio_evap)

#======== correlation map ===================================
def Global_plot(dataset, title, ax, levels):
    im = ax.contourf(
        dataset.lon, 
        dataset.lat,
        dataset,
        levels=levels, cmap=cmocean.cm.tarn,
        transform=ccrs.PlateCarree(),
        extend='neither'
    )
    ax.coastlines(resolution='110m')
    ax.gridlines(linestyle='--', alpha=0.3, draw_labels=False)
    ax.set_title(title, fontweight='bold', fontsize=12, pad=20)
    ax.set_global()
    return im

levels_corr = np.linspace(-1, 1, 11)

fig, axs = plt.subplots(1, 2, figsize=(10, 5), 
                       subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))

im1 = Global_plot(mpi_corr, 'a) MPI-ESM1-2-HR', axs[0], levels_corr)
im2 = Global_plot(fio_corr, 'b) FIO-ESM-2-0', axs[1], levels_corr)

cbar1 = plt.colorbar(im1, ax=axs[0], orientation='horizontal', shrink=0.8, pad=0.1, aspect=40)
cbar1.set_label('r', fontsize=12, fontweight='bold')

cbar2 = plt.colorbar(im2, ax=axs[1], orientation='horizontal', shrink=0.8, pad=0.1, aspect=40)
cbar2.set_label('r', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('./Plots/evap_correlation_MPI_FIO_vs_ERA5.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Gridpoint-by-gridpoint correlation complete!")