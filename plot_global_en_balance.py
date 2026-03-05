import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean

# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")
timmean_fluxes = data_path / "fluxes_timmean.nc"  # Annual mean of all the fluxes W m-2

ds = xr.open_dataset(timmean_fluxes).squeeze('valid_time')
print('---- Data successfully opened----')

# Radiative forcing
swf = ds.avg_snswrf
lwf = ds.avg_snlwrf
Rs = lwf + swf

# Outflux
shf = np.abs(ds.avg_ishf)
lhf = np.abs(ds.avg_slhtf)

# Ground heat flux
G = Rs - (shf + lhf)

def plot_global_field(field, title, filename):
    
    fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))
    
    im = ax.contourf(field.longitude, field.latitude, field.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.balance, 
                     levels=21)
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                        shrink=0.8, pad=0.08, aspect=40, label=r'$Wm^{-2}$')
    plt.subplots_adjust(bottom=0.15)
    fname = os.path.join(output_folder, filename)
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")


plot_global_field(Rs, '', 'Radiative_heating.png')
plot_global_field(lhf, '', 'latent_heat_flux.png')
plot_global_field(shf, '', 'sensible_heat_flux.png')
plot_global_field(G, '', 'Ground_heat_flux.png')
