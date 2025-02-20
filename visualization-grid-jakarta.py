import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Baca file NetCDF VIIRS/SNPP
file_path = "./aod-file/AERDB_L2_VIIRS_SNPP.A2023255.0636.002.2023255185945.nc"
ds = xr.open_dataset(file_path)

# Ambil variabel penting
latitude = ds['Latitude'].values
longitude = ds['Longitude'].values
aod = ds['Aerosol_Optical_Thickness_550_Land_Best_Estimate'].values  # Sesuaikan nama variabel AOD

# Masking nilai AOD untuk data yang valid (tidak NaN)
#aod_valid = np.where(np.isnan(aod), np.nan, aod)

# Definisikan bounding box Jakarta
#lat_min, lat_max = -6.5, -5.9
#lon_min, lon_max = 106.6, 107.0

# Masking data di luar Jakarta menjadi NaN
#mask_jakarta = (latitude >= lat_min) & (latitude <= lat_max) & (longitude >= lon_min) & (longitude <= lon_max)
#aod_filtered = np.full(aod.shape, np.nan)  # Set seluruh nilai awal NaN
#aod_filtered[mask_jakarta] = aod[mask_jakarta]  # Hanya nilai Jakarta yang 

#print(aod_filtered)

#print(aod_filtered.shape[0])
#print(aod_filtered.shape[1])


# Visualisasi dengan format raster
fig, ax = plt.subplots(figsize=(14, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Tambahkan fitur peta dunia
ax.coastlines(resolution='110m')
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Raster plot AOD
c = ax.pcolormesh(longitude, latitude, aod, cmap='viridis', shading='auto', transform=ccrs.PlateCarree())

# Tambahkan colorbar
plt.colorbar(c, ax=ax, label='AOD (Jakarta Data Only)')

# Judul dan label peta
ax.set_title("Peta Dunia dengan Data AOD Hanya di Jakarta", fontsize=16)

plt.show()