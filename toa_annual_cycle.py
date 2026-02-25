import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os



# Creates output folder if it doesn't exist
output_folder = './Plots/'
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

path_1 = os.path.expanduser('~/ESP/ESM/ESM_LAB/Data/toa_ymonmean_annuacycle_sw.nc')
ds1 = xr.open_dataset(path_1)
var = ds1['avg_tnswrf'].isel(lat=0, lon=0)
x = var.valid_time
y = var.values.T

months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']


plt.figure(figsize=(12, 6))
plt.grid(True, alpha=0.3)
plt.plot(months, y, linewidth=3)
plt.xlabel('Month', fontsize=13)
plt.ylabel('Net radiation ($Wm^{-2}$)', fontsize=13)
plt.gca().spines[['top', 'right']].set_visible(False)
plt.tight_layout()

fname = os.path.join(output_folder, 'toa_annualcycle_sw.png')
plt.savefig(fname, dpi=300, bbox_inches='tight')