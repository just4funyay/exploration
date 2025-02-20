import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Baca file NetCDF
file_path = "./aod-file/AERDB_L2_VIIRS_SNPP.A2023255.0636.002.2023255185945.nc"
ds = xr.open_dataset(file_path)

# Ambil variabel penting
latitude = ds['Latitude'].values
longitude = ds['Longitude'].values
aod = ds['Aerosol_Type_Land'].values  # Sesuaikan nama variabel

# Definisikan bounding box Jakarta
lat_min, lat_max = -6.5, -5.9
lon_min, lon_max = 106.6, 107.0

# Filter data untuk wilayah Jakarta
mask = (latitude >= lat_min) & (latitude <= lat_max) & (longitude >= lon_min) & (longitude <= lon_max)

# Ambil data AOD yang sesuai dengan filter Jakarta
aod_jakarta = aod[mask]
latitude_jakarta = latitude[mask]
longitude_jakarta = longitude[mask]

# Membuat grid dari data AOD
lat_grid, lon_grid = np.meshgrid(np.unique(latitude_jakarta), np.unique(longitude_jakarta))

# Membuat matriks AOD dengan interpolasi atau pemetaan yang sesuai
aod_grid = np.zeros_like(lat_grid)

for i, lat in enumerate(np.unique(latitude_jakarta)):
    for j, lon in enumerate(np.unique(longitude_jakarta)):
        # Temukan nilai AOD yang sesuai
        idx = (latitude_jakarta == lat) & (longitude_jakarta == lon)
        aod_grid[i, j] = np.nanmean(aod_jakarta[idx])

# Visualisasi menggunakan Cartopy untuk peta dunia
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Peta dunia dengan Cartopy
ax.set_global()  # Menampilkan peta dunia secara keseluruhan
ax.coastlines(resolution='110m')  # Garis pantai dunia
ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')  # Batas negara
ax.add_feature(cfeature.LAND, facecolor='lightgray')  # Daratan
ax.add_feature(cfeature.LAKES, facecolor='lightblue')  # Danau

# Plot grid data AOD untuk wilayah Jakarta
c = ax.pcolormesh(lon_grid, lat_grid, aod_grid, cmap='viridis', shading='auto', transform=ccrs.PlateCarree())

# Menambahkan colorbar
plt.colorbar(c, ax=ax, label='AOD')

# Labeling
ax.set_title("AOD Grid untuk Wilayah Jakarta pada Peta Dunia", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Menampilkan peta
plt.show()
