#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import date
from itertools import groupby
import argparse
import numpy as np
import pandas as pd
import xarray as xr
from tabulate import tabulate

pd.options.display.max_colwidth = 200


def args():
    parser = argparse.ArgumentParser(description="Produce information about LTSP gridded product")
    parser.add_argument('-site', dest='site', help='site code, like NRMMAI',  type=str, default=None, required=True)

    vargs = parser.parse_args()
    return(vargs)



def blockPlot(x, lineLength = 80):
    """
    Print a line block-plot of data availability of specified length
    E. Klein. ekleins@gmail.com 2020-10-20
    :param x: numpy array of dim 1
    :param lineLength: lenght of the line plot
    :return: string
    """

    blockSymbols = ['\u2591','\u2593']
    ## make boolean vector 1-nodata 0-data
    x_bool = np.isnan(x.values).astype(int).tolist()
    ## run-length encoder
    x_rle = [[key, len(list(group))] for key, group in groupby(x_bool)]
    ## list of number of symbols
    x_sum = len(x)
    ##x_sum = sum(x[1] for x in x_rle)
    x_symbols = list(round(lineLength * x[1]/x_sum) for x in x_rle)
    return''.join(list(blockSymbols[x_rle[i][0]] * x_symbols[i] for i in range(len(x_rle))))



def infoLTSP(site):
    """
    Produce a summary report for gridded LTSP for a site
    :param site: site name

    :return: nothing
    """

    webRoot = 'http://thredds.aodn.org.au/thredds/dodsC/'

    ## get gridded-_timeseries filename
    url = ("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='%s')" % site)
    df = pd.read_csv(url)
    fileName = df['url'].loc[df['url'].str.contains('gridded_timeseries')].to_string(index=False).lstrip()

    if '\n' in fileName:
        print('ERROR: more than one filename:')
        print(fileName)
        return

    ## print(os.path.join(webRoot, fileName))
    nc = xr.open_dataset(os.path.join(webRoot, fileName))
    depthList = list(nc.DEPTH.values)

    table = list()
    ## print file info
    table.append(['Site', site])
    table.append(['Sub-Facility:',  str.split(fileName, "/")[2]])
    table.append(['Filename for download:', nc.source_file_download])
    table.append(['Filename for connection:', nc.source_file_opendap])
    table.append(['Location:', (str(round(np.mean([nc.geospatial_lat_max, nc.geospatial_lat_min]), 5)) + " - " +
                                        str(round(np.mean([nc.geospatial_lon_max, nc.geospatial_lon_min]), 5)))])
    table.append(['Time coverage:', nc.time_coverage_start + ' through ' + nc.time_coverage_end])
    table.append(['Max DEPTH:', str(nc.geospatial_vertical_max)])
    table.append(['Included DEPTHS:',  ", ".join(str(x) for x in depthList)])
    for dd in depthList:
        temp = nc.TEMP.sel(DEPTH=float(dd))
        table.append(['Data Availability at '+ str(dd) + "m:", blockPlot(temp, lineLength=40)])

    print(tabulate(table))
    print('\u2591 DATA, \u2593 NO DATA')
    return


if __name__ == "__main__":
     vargs = args()
     infoLTSP(**vars(vargs))


