#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import date, datetime
from itertools import groupby
import argparse
import numpy as np
import pandas as pd
import xarray as xr
from tabulate import tabulate

pd.options.display.max_colwidth = 200


def args():
    parser = argparse.ArgumentParser(description="Information about IMOS-LTSP product")
    parser.add_argument('-site', dest='site', help='site code, like NRMMAI',  type=str, default=None, required=True)
    parser.add_argument('-type', dest='fileType', help='file type: H - hourly, G - gridded', type=str, default=None, required=True)
    vargs = parser.parse_args()
    return(vargs)



def blockPlot(x, lineLength = 80):
    """
    Print a line block-plot of data availability of specified length
    E. Klein. eklein at ocean-analytics dot com dot au. 2020-10-20
    :param x: numpy array of dim 1
    :param lineLength: lenght of the line plot
    :return: string
    """

    blockSymbols = ['\u2593', '\u2591']
    ## make boolean vector 1-nodata 0-data
    if x.dtype == 'float32':
        x_bool = np.isnan(x.values).astype(int).tolist()
    else:
        x_bool = np.isnan(x).astype(int).tolist()
    ## run-length encoder
    x_rle = [[key, len(list(group))] for key, group in groupby(x_bool)]
    ## list of number of symbols
    x_sum = len(x)
    x_symbols = list([i, round(lineLength * rle[1] / x_sum)] for i, rle in enumerate(x_rle))
    nBlocks =sum([item[1] for item in x_symbols])
    if nBlocks != lineLength:
        x_symbols = sorted(x_symbols, key=lambda x: x[1], reverse=True)
        diffSign = np.sign(lineLength - nBlocks)
        diffBlocks = abs(lineLength - nBlocks)
        for block in range(diffBlocks):
            x_symbols[block][1] += diffSign
        x_symbols = sorted(x_symbols, key=lambda x: x[0], reverse=False)
    x_symbols = [x_symbols[i][1] for i in range(len(x_symbols))]
    return ''.join(list(blockSymbols[x_rle[i][0]] * int(x_symbols[i]) for i in range(len(x_rle))))




def getFileName(site, fType, param=None, webroot='opendap'):
    '''
    get the file name of the LTSP files
    Eduardo Klein. eklein at ocean-analytics dor com dot au
    May 2021
    :param site: site code
    :param fType: type of LTSP: A aggregated, H hourly, G gridded, V velocity hourly
    :param param: if ftype A, the code name of the parameter, like TEMP
    :param webroot: opendap to get opendap URL, wget to get AWS URL, anything else, just the filename
    :return: string: file name
    '''
    fType = fType.upper()
    fileType = {'A': 'aggregated-timeseries',
                'H': '_hourly-timeseries_',
                'G': 'gridded-timeseries',
                'V': '_velocity-hourly-timeseries_' }

    if webroot=='opendap':
        webRoot = 'http://thredds.aodn.org.au/thredds/dodsC/'
    elif webroot=='wget':
        webRoot = 'https://s3-ap-southeast-2.amazon.com/imos-data/'
    else:
        webRoot = ''

    ## get gridded-_timeseries filename
    url = ("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='%s')" % site)
    df = pd.read_csv(url)
    fileName = df['url'].loc[df['url'].str.contains(fileType[fType])].to_string(index=False).lstrip()
    if fType=='A':
        if not param:
            return print('ERROR: Need param NAME')

        fileName = fileName.replace(" ", "").split('\n')
        fileName ="".join([match for match in kk if param in match])

    if '\n' in fileName:
        print('ERROR: more than one filename:')
        print(fileName)

    return os.path.join(webRoot,fileName)




def infoLTSPg(site):
    """
    Produce a summary report for **gridded** LTSP for a site
    :param site: site name
    :return: tabulated printout
    """

    fileName = getFileName(site, "G")
    nc = xr.open_dataset(fileName)
    depthList = list(nc.DEPTH.values)

    table = list()
    ## print file info
    table.append(['Site', site])
    table.append(['Sub-Facility:',  str.split(fileName, "/")[2]])
    table.append(['Filename for download:', nc.source_file_download])
    table.append(['Filename for connection:', nc.source_file_opendap])
    table.append(['Location:', (str(round(np.mean([nc.geospatial_lat_max, nc.geospatial_lat_min]), 5)) + " - " +
                                        str(round(np.mean([nc.geospatial_lon_max, nc.geospatial_lon_min]), 5)))])
    table.append(['Variables: ', list(nc.data_vars)])
    table.append(['Time coverage:', nc.time_coverage_start + ' through ' + nc.time_coverage_end])
    table.append(['Max DEPTH:', str(nc.geospatial_vertical_max)])
    table.append(['Included DEPTHS:',  ", ".join(str(x) for x in depthList)])
    for dd in depthList:
        temp = nc.TEMP.sel(DEPTH=float(dd))
        table.append(['Data Availability at '+ str(dd) + "m:", blockPlot(temp, lineLength=40)])

    print(tabulate(table))
    print('\u2591 NO DATA, \u2593 DATA')
    return


def infoLTSPh(site, infoInst=False):
    """
    Produce a summary report for **hourly** LTSP for a site
    :param site: site name
    :param infoInst: True for additional information on the instruments
    :return: tabulated printout
    """
    FileName = getFileName(site, 'H')
    nc = xr.open_dataset(fileName)
    varList = list(nc.data_vars)
    varIdx = [i for i, val in enumerate(["_" in item for item in varList]) if not val]
    varListClean = [varList[i] for i in varIdx]

    table = list()
    ## print file info
    table.append(['Site', site])
    table.append(['Sub-Facility:',  str.split(fileName, "/")[2]])
    table.append(['Filename for download:', fileName])
    ##table.append(['Filename for connection:', nc.source_file_opendap])
    table.append(['Location:', (str(round(np.mean([nc.geospatial_lat_max, nc.geospatial_lat_min]), 5)) + " - " +
                                        str(round(np.mean([nc.geospatial_lon_max, nc.geospatial_lon_min]), 5)))])
    table.append(['Time coverage:', nc.time_coverage_start + ' thru ' + nc.time_coverage_end])
    table.append(['Min DEPTH:', str(np.round(nc.geospatial_vertical_min, 1))])
    table.append(['Max DEPTH:', str(np.round(nc.geospatial_vertical_max, 1))])
    table.append(['DATA variables:',  ", ".join(str(x) for x in varListClean)])
    table.append(['Number of Instruments', len(nc.INSTRUMENT)])

    for vv in varListClean:
        table.append([vv, blockPlot(nc[vv])])

    print(tabulate(table, tablefmt="plain"))
    print('\u2591 NO DATA, \u2593 DATA')

    if infoInst:
        infoHourlyInstrument(nc)

    return


def infoHourlyInstrument(nc):
    '''
    Produce detailed information of every instrument in an **HOURLY** LTSP file
    :param nc: xarray dataset
    :return: tabulated printout
    '''
    timeFormat='%Y-%m-%d'
    timeRange0 = pd.date_range(start=np.min(nc.TIME.values), end=np.max(nc.TIME.values), freq='1H').to_numpy()
    nInstruments = len(nc.INSTRUMENT)
    table = list()
    for ii in range(nInstruments):
        timeRangeInst = np.copy(timeRange0)
        ## this is a trick to override the NaT returned by np.min
        ncTimeInst = nc.TIME[np.where(~np.isnat(nc.TIME.where(nc.instrument_index==ii)))].values
        timeMin = pd.to_datetime(np.min(ncTimeInst)).to_numpy()
        timeMax = pd.to_datetime(np.max(ncTimeInst)).to_numpy()
        timeRangeInst[(timeRangeInst<timeMin) | (timeRangeInst>timeMax)] = np.datetime64('NaT')
        table.append([ii,
              nc.instrument_id[ii].values.astype(str),
              pd.to_datetime(timeMin).strftime(timeFormat),
              pd.to_datetime(timeMax).strftime(timeFormat),
              blockPlot(timeRangeInst, lineLength=40)])
    print(tabulate(table, tablefmt="plain",
                   headers=['Instrument_index', 'Instrument id', 'Coverage FROM', 'Coverage THRU', 'Data Availability']))
    return




if __name__ == "__main__":
    vargs = args()
    if vargs.fileType == "G":
        infoLTSPg(vargs.site)
    elif vargs.fileType == "H":
        infoLTSPh(vargs.site)
    else:
        print("File TYPE %s unknown. Must be G or H" % vargs.fileType)


