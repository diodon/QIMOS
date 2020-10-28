## extract cloud variables from already clipped VISST product at lat/lon
## coordinates pairs are read from a text file
## E Klein. ekleins@gmail.com
## 2020-10-21

import os
import itertools
import numpy as np
import pandas as pd
import xarray as xr

## setup directories
dataDir = "VISST/GBR_cat"
resultsDir = "VISST/GBR_cat"

## name of the data file
dataFileName = "GBR_2016_SepOct.nc"
coordsFileName = "coords.csv"

## read data and coordinates files
nc = xr.open_dataset(os.path.join(dataDir, dataFileName))
df = pd.read_csv(os.path.join(dataDir, coordsFileName))

## set latitude and longitude as indices
nc = nc.set_index(lat="latitude", lon="longitude")

## select flux and albedo variable only for clear sky
nc['LW_flux'] = nc.broadband_longwave_flux[:,:,:,0]
nc['SW_albedo'] = nc.broadband_shortwave_albedo[:,:,:,0]

## clean the dataset
nc = nc.drop(["broadband_longwave_flux", "broadband_shortwave_albedo", 'cld_type', 'scn_type'])
nc = nc.squeeze()


## extract data from coordinates
df_sites = pd.DataFrame()
for i in range(len(df)):
    print(i, df.Site[i])
    llat = df.Latitude[i]
    llon = df.Longitude[i]
    nc_select = nc.sel(lat=[llat], lon=[llon], method="nearest").squeeze()
    timeLen = len(nc_select.time)

    data = nc_select.to_dataframe()
    data['Site'] = df.Site[i]
    df_sites = df_sites.append(data)
## write results
df_sites.to_csv(os.path.join(dataDir, ("clouds_" + dataFileName.split(".")[0] + ".csv")))
