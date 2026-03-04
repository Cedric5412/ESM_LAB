import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import cmocean
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm


# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

# =============================================================================
# DATA PATH
# =============================================================================
data_path = Path("/home/cpizina/ESP/ESM/ESM_LAB/Data")

timmean_fluxes = data_path / "fluxes_timmean.nc"    # Annual mean of all the fluxes W m-2

# =============================================================================
# LOAD DATA
# =============================================================================

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

def Global_plot(dataset, title, ax):
    im = ax.contourf(dataset.longitude, dataset.latitude, dataset.values,
                     transform=ccrs.PlateCarree(),
                     cmap=cmocean.cm.balance, 
                     levels=21
                     )
    
    ax.coastlines(resolution='110m')
    ax.set_title(title, fontweight='bold', pad=20)
    # ax.add_feature(cf.OCEAN, edgecolor='black', zorder=0.5, facecolor='white')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linestyle='--',
                      linewidth=0.3, color='black', alpha=0.5, zorder=1.5)
    gl.top_labels = False
    gl.right_labels = False
    return im


# Plot Rs
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8),
                        subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))

title = ''
im1 = Global_plot(Rs, title, ax)
cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'Radiative_heating.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

# Plot LHF
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8),
                        subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))

title = ''
im1 = Global_plot(lhf, title, ax)
cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'latent_heat_flux.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')

#Plot SHF
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8),
                        subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))

title = ''
im1 = Global_plot(shf, title, ax)
cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'sensible_heat_flux.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')


# Plot G
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8),
                        subplot_kw=dict(projection=ccrs.Mollweide(central_longitude=180)))

title = ''
im1 = Global_plot(G, title, ax)
cbar = plt.colorbar(im1, ax=ax, orientation='horizontal', shrink=0.8, pad=0.08, aspect=40)
plt.subplots_adjust(bottom=0.15)
fname = os.path.join(output_folder, 'Ground_heat_flux.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')