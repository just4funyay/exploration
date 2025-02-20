import xarray as xr
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine

# Baca file NetCDF VIIRS/SNPP
file_path = "./aod-file/AERDB_L2_VIIRS_SNPP.A2023255.0636.002.2023255185945.nc"
ds = xr.open_dataset(file_path)

# Ambil variabel penting
latitude = ds['Latitude'].values
longitude = ds['Longitude'].values
aod = ds['Aerosol_Optical_Thickness_550_Land_Best_Estimate'].values

# Masking nilai AOD untuk Jakarta
lat_min, lat_max = -6.5, -5.9
lon_min, lon_max = 106.6, 107.0

# Filter hanya data Jakarta
mask_jakarta = (latitude >= lat_min) & (latitude <= lat_max) & (longitude >= lon_min) & (longitude <= lon_max)

# Buat list data titik valid
data_points = []
for i in range(latitude.shape[0]):
    for j in range(latitude.shape[1]):
        if mask_jakarta[i, j] and not np.isnan(aod[i, j]):
            point = Point(longitude[i, j], latitude[i, j])
            data_points.append({"geometry": point, "AOD": aod[i, j]})

# Konversi ke GeoDataFrame
gdf = gpd.GeoDataFrame(data_points, crs="EPSG:4326")

# Buat koneksi ke database PostGIS
db_connection_url = "postgresql://postgres:mandaika@localhost:5432/aod-example"
engine = create_engine(db_connection_url)

# Simpan GeoDataFrame ke PostGIS
table_name = "aod_jakarta_points"
gdf.to_postgis(table_name, engine, if_exists='replace')

print(f"Data AOD Jakarta berhasil disimpan ke tabel '{table_name}' di PostGIS.")
