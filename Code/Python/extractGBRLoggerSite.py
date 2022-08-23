## This function extracts the full temp logger data set from a GBR specific site
## data comes from the full logger dataset stored as parquet files
## the site must be picked from list
import os
import datetime
import numpy as np
import pandas as pd
import dask
import dask.dataframe as dd

parquetDir = '/DATA/AIMS/Loggers/parquet'
dataDir = '/DATA/AIMS/Loggers/loggers_GBR'
rootDir = '/DATA/AIMS/Loggers'
outDir = '/DATA/AIMS/Loggers/Extracted'


print("TEMP LOGGER EXTRACTOR")


with open(os.path.join(rootDir, "siteList.txt")) as ff:
    siteList = ff.read().splitlines()


go = 'r'
while go == 'r':
    ## select site
    for i, site in enumerate(siteList):
        print(i, site)

    siteID = input("Input your site number: ")
    if int(siteID) > len(siteList)-1:
        go = input("Invalid site number, re-try (r), or exit (e) ")
    else:
        print('Selected site is ', siteList[int(siteID)])
        go = input("Proceed (p), re-try (r), or exit (e) ")

if go == 'e':
    exit()


## Do the extraction
print("Extracting logger data for " + siteList[int(siteID)] + ". It will take few minutes...")
siteCode = siteList[int(siteID)].split(' - ')[-1]
siteName = siteList[int(siteID)].split(' - ')[0].replace(" ", "").replace(",", "")

dfp = dd.read_parquet(parquetDir)
dfSite = dfp[(dfp.gbrmpa_reef_id==siteCode) & (dfp.parameter=="Water Temperature")].compute()

## save data
dfSite.to_csv(os.path.join(outDir, siteName) + ".csv", index=False)
print("Extracted logger data saved in", (os.path.join(outDir, siteName) + ".csv"))



