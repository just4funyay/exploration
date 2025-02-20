import xarray as xr
import os

netcdf_file_name = 'AERDB_L2_VIIRS_NOAA20.A2023253.0618.002.2023253184826.nc'
csv_file_out = netcdf_file_name[:-3] + '.csv'
ds = xr.open_dataset(netcdf_file_name, decode_timedelta=True)
df = ds.to_dataframe()
df.to_csv("tesaja.csv")