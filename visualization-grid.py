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
print(aod)

# Masking nilai AOD untuk data yang valid (tidak NaN)
aod_valid = np.where(np.isnan(aod), np.nan, aod)

# Membuat peta dengan Cartopy untuk seluruh dunia
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Menampilkan peta dunia dengan garis pantai
ax.set_global()
ax.coastlines(resolution='110m')
ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.LAKES, facecolor='lightblue')

# Plot data AOD dalam bentuk grid (dengan longitude dan latitude asli)
c = ax.pcolormesh(longitude, latitude, aod_valid, cmap='viridis', shading='auto', transform=ccrs.PlateCarree())

# Menambahkan colorbar untuk AOD
plt.colorbar(c, ax=ax, label='AOD')

# Labeling dan judul
ax.set_title("Peta AOD VIIRS/SNPP (Grid 6km)", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Menampilkan peta
plt.show()
