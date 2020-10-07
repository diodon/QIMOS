#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import date
import argparse
import numpy as np
import pandas as pd
import xarray as xr

pd.options.display.max_colwidth = 200

def args():
    parser = argparse.ArgumentParser(description="Get a TEMP timeseries from the gridded product at specified DEPTH")
    parser.add_argument('-site', dest='site', help='site code, like NRMMAI',  type=str, default=None, required=True)
    parser.add_argument('-depth', dest='depth', help='selecyted depth, like 10',  type=float, default=None, required=True)
    parser.add_argument('-ts', dest='dateStart', help='start time like 2015-12-01', default=None, type=str, required=False)
    parser.add_argument('-te', dest='dateEnd', help='end time like 2018-06-30', type=str, default=None, required=False)
    #parser.add_argument('-i', '--info', dest='info', help='display file info ONLY', type=bool, default=False, required=False)

    vargs = parser.parse_args()
    return(vargs)



def NRSgetTS(site, depth, dateStart='1970-01-01', dateEnd=date.today()):
    """
    Extract hourly temperature time series from NRS gridded product
    :param site: site name
    :param depth: selected depth
    :param dateStart: start date as yyyy-mm-dd
    :param dateEnd: end date as yyyy-mm-dd
    :param info: print file info only

    :return: name of the csv output file
    """

    webRoot = 'http://thredds.aodn.org.au/thredds/dodsC/'
    info=False

    ## get gridded-_timeseries filename
    url = ("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='%s')" % site)
    df = pd.read_csv(url)
    fileName = df['url'].loc[df['url'].str.contains('gridded_timeseries')].to_string(index=False).lstrip()
    print(fileName)

    if '\n' in fileName:
        print('ERROR: more than one filename:')
        print(fileName)
        return

    print(os.path.join(webRoot, fileName))
    nc = xr.open_dataset(os.path.join(webRoot, fileName))
    depthList = list(nc.DEPTH.values)
    coverageStart = nc.time_coverage_start
    coverageEnd = nc.time_coverage_end



    if depth not in depthList:
        print('ERROR: Requested DEPTH (%im) is not available.' % depth)
        info = True

    ## print file info
    print('FILE DETAILS:')
    print(fileName)
    print('Site: ' + site)
    print('Sub-Facility: ' + str.split(fileName, "/")[2])
    print('Location: ' + str(np.mean([nc.geospatial_lat_max, nc.geospatial_lat_min])) + ", " +
          str(np.mean([nc.geospatial_lon_max, nc.geospatial_lon_min])))
    print('Time coverage: ' + nc.time_coverage_start + ' trough ' + nc.time_coverage_end)
    print('Max DEPTH: ' + str(nc.geospatial_vertical_max))
    print('Included DEPTHS: ' + str(depthList))

    if info:
        return


    ## extract TEMP at selected DEPTH
    temp = nc.TEMP.sel(DEPTH=float(depth))

    ## save csv
    fileNameCSV = "_".join([site, 'TEMP', (str(depth)+'m'),
                            (str.split(nc.time_coverage_start, "T")[0].replace("-","") + "-" +
                             str.split(nc.time_coverage_end, "T")[0].replace("-","")),]) + '.csv'
    temp.to_series().to_csv(fileNameCSV)


    print("Output file: " + fileNameCSV)

    return


if __name__ == "__main__":
     vargs = args()
     NRSgetTS(**vars(vargs))



