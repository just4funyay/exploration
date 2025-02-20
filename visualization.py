import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs  # Untuk menggunakan peta dunia

# Baca file NetCDF
file_path = "./aod-file/AERDB_L2_VIIRS_SNPP.A2024256.0530.002.2024256175428.nc"
ds = xr.open_dataset(file_path)

# Ambil variabel penting
latitude = ds['Latitude'].values
longitude = ds['Longitude'].values
aod = ds['Aerosol_Type_Land'].values  # Sesuaikan nama variabel

# Buat DataFrame untuk pemetaan Idx_Atrack dan Idx_Xtrack
idx_atrack, idx_xtrack = latitude.shape

data_list = []
for i in range(idx_atrack):
    for j in range(idx_xtrack):
        # Pastikan tidak ada NaN dalam latitude dan longitude
        if not pd.isna(latitude[i, j]) and not pd.isna(longitude[i, j]):
            data_list.append({
                "Idx_Atrack": i,
                "Idx_Xtrack": j,
                "Latitude": latitude[i, j],
                "Longitude": longitude[i, j],
                "AOD": aod[i, j] if not pd.isna(aod[i, j]) else None
            })

# Konversi menjadi DataFrame
df = pd.DataFrame(data_list)

# Definisikan bounding box Jakarta
lat_min, lat_max = -6.5, -5.9
lon_min, lon_max = 106.6, 107.0

# Filter data untuk wilayah Jakarta
jakarta_data = df[
    (df["Latitude"] >= lat_min) & (df["Latitude"] <= lat_max) &
    (df["Longitude"] >= lon_min) & (df["Longitude"] <= lon_max)
]

# Tampilkan hasil
print("Data AOD untuk wilayah Jakarta:")
print(jakarta_data)

# Hitung rata-rata AOD untuk Jakarta
if not jakarta_data.empty:
    mean_aod_jakarta = jakarta_data["AOD"].mean()
    print(f"Rata-rata AOD di Jakarta: {mean_aod_jakarta}")
else:
    print("Tidak ada data AOD dalam bounding box Jakarta.")

# Visualisasi menggunakan Cartopy untuk peta dunia

# Membuat plot peta Jakarta
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# Peta dunia dengan Cartopy
ax.coastlines()
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Plot data AOD di Jakarta
sc = ax.scatter(jakarta_data["Longitude"], jakarta_data["Latitude"], c=jakarta_data["AOD"], cmap='viridis', s=10, transform=ccrs.PlateCarree())

# Menambahkan colorbar
plt.colorbar(sc, ax=ax, label='AOD')

# Labeling
ax.set_title("Data AOD di Jakarta", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Menampilkan peta
plt.show()
