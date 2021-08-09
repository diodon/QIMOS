#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Explore individual IMOS NMN files


import os
import sys
from datetime import date, datetime
from itertools import groupby
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from tabulate import tabulate

pd.options.display.max_colwidth = 200


def args():
    parser = argparse.ArgumentParser(description="Explore velocity or temperature AODN individual files")
    parser.add_argument('-site', dest='site', help='site code, like NRMMAI',  type=str, default=None, required=True)
    parser.add_argument('-param', dest='param', help='parameter, like V for velocity, T temperature', type=str, default=None, required=True)
    vargs = parser.parse_args()
    return(vargs)

def splitStr(valueList, nchar=80):
    '''
    Cut the string at nchar lenght, inserting new lines after comma
    :param valueList: list of values to join
    :param nchar: length of the line
    :return: string
    '''
    ss = valueList[0]
    lineLen = nchar
    for item in valueList[1:]:
        if len(ss) >= lineLen:
            ss = ", ".join([ss] + ["\n" + item])
            lineLen += nchar
        else:
            ss = ", ".join([ss] + [item])
    return(ss)


def getFileName(site, param=None):
    '''
    get the list of file name of the LTSP files
    and offer a table for selection
    :param site: site code
    :param param: V for velocity, T for temperature
    :return: str: file name
    '''

    webRoot = 'http://thredds.aodn.org.au/thredds/dodsC/'

    if param == 'V':
        paramCheck = 'has_sea_water_velocity'
    elif param == 'T':
        paramCheck = 'has_water_temperature'
    else:
        print('ERROR: {0} is a wrong parameter. Must be T or V'.format(param))
        sys.exit()

    url = ("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='%s')" % site)
    df = pd.read_csv(url)
    fileList = df['url'].loc[(df[paramCheck]==True) & (df['site_code']==site) &
                             (df['file_version']==1) &
                             ((df['data_category'] == 'Temperature') |
                              (df['data_category'] == 'Velocity'))].to_list()

                             # ((df['data_category'] != 'aggregated_timeseries') &
                             #  (df['data_category'] != 'hourly_timeseries') &
                             #  (df['data_category'] != 'gridded_timeseries') &
                             #  (df['data_category'] != 'Biogeochem_timeseries'))].to_list()

    fileList.sort()

    ## parse file name and make a table for selection
    table = []
    for ff in fileList:
        ffParse = ff.split("_")
        deployment = ff.split("/")[-1].split("_")[6].split("-")[1]
        instrument = " ". join(ff.split("/")[-1].split("_")[6].split("-")[2:-1])
        nominalDepth = ff.split("/")[-1].split("_")[6].split("-")[-1]
        startDate = datetime.strptime(ff.split("/")[-1].split("_")[3], "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d")
        endDate = datetime.strptime(ff.split("/")[-1].split("_")[7], "END-%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d")
        creationDate = datetime.strptime(ff.split("/")[-1].split("_")[8], "C-%Y%m%dT%H%M%SZ.nc").strftime("%Y-%m-%d")
        table.append([deployment, instrument, nominalDepth, startDate, endDate, creationDate])

    #table.sort(key=lambda row: row[3])

    print(tabulate(table, showindex='always', headers=["Deployment", "Instrument", "Depth", "Start Date", "End Date", "Creation Date"]))

    selectedFile = -1
    while selectedFile > len(table) or selectedFile < 0:
        selectedFile = input("Select file number ('s' to save the list or 'e' to exit): ")
        if selectedFile == 'e':
            print("EXIT")
            sys.exit()
        elif selectedFile == 's':
            outDF = pd.DataFrame(table, columns=["Deployment", "Instrument", "Depth", "Start Date", "End Date", "Creation Date"], index=None)
            outDF['Filename'] = fileList
            outDF = outDF[['Filename', "Deployment", "Instrument", "Depth", "Start Date", "End Date", "Creation Date"]]
            outFilename = site + "_" + param + "_filelist.csv"
            outDF.to_csv(outFilename, index=False)
            print('File list and attributes saved to', outFilename)
            sys.exit()
        else:
            selectedFile = int(selectedFile)

    print("Selected file: {}".format(fileList[selectedFile]))

    return os.path.join(webRoot,fileList[selectedFile])





def exploreMooring(fileName, makePlot=False):
    '''
    Explore AODN selected file. TEMP or Velocity only
    :param fileName: openDAP url
    :return:
    '''

    print("IMOS ANMN Explorer")
    print("File: {}".format(fileName))
    table = []
    with xr.open_dataset(fileName) as nc:

        # ## convert HEIGHT_ABOVE_SENSOR to DEPTH
        # if nc['HEIGHT_ABOVE_SENSOR'].positive =='up':
        #     nc['HEIGHT_ABOVE_SENSOR'] = nc.instrument_nominal_depth - nc['HEIGHT_ABOVE_SENSOR']
        # else:
        #     nc['HEIGHT_ABOVE_SENSOR'] = nc.instrument_nominal_depth + nc['HEIGHT_ABOVE_SENSOR']


        table.append(["Title:", nc.title])
        table.append(["Site code:", nc.site_code])
        table.append(["Deployment code:", nc.deployment_code])
        table.append(["Start Date:", nc.time_deployment_start])
        table.append(["End Data:", nc.time_deployment_end])
        table.append(["Instrument:", nc.instrument])
        table.append(["Instrument S/N:", nc.instrument_serial_number])
        table.append(["Instrument sampling interval", nc.instrument_sample_interval])
        table.append(["Instrument Nominal Depth:", nc.instrument_nominal_depth])

        cellDepths = splitStr(list(nc['HEIGHT_ABOVE_SENSOR'].values.astype(str)))
        table.append(['Cell depths Above Sensor:', cellDepths])

        dataVars = nc.data_vars
        dataVars = splitStr([item for item in dataVars if "quality_control" not in item])
        table.append(["Data Variables:", dataVars])


        print(tabulate(table))


        if makePlot:

            plotWidth = 10
            plotHeight = 6
            nRows = len(nc.HEIGHT_ABOVE_SENSOR)
            nc.UCUR.plot(col="HEIGHT_ABOVE_SENSOR", col_wrap=1, figsize=(plotHeight*nRows, plotWidth))

            fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(14,11))
            nc.UCUR.T.plot(ax=ax1)
            ax1.invert_yaxis()
            axes.get_legend().remove()

            plt.title(nc.site_code)
            plt.xlabel("")
            plt.ylabel("")
            nc.VCUR.T.plot(ax=axes[1])
            plt.gca().invert_yaxis()
            plt.title("")
            plt.xlabel("")
            plt.ylabel("DEPTH (m)")
            nc.WCUR.T.plot(ax=axes[2])
            plt.gca().invert_yaxis()
            plt.title("")
            plt.xlabel("")
            plt.ylabel("")
            plt.show()
            # nc.T.plot(yincrease=False, robust=True, figsize=(11,7), aspect=1.6, add_labels=False,
            #           cbar_kwargs={
            #               "orientation": "horizontal",
            #               "label": nc.UCUR.standard_name + " (" + nc.UCUR.units + ")",
            #               "pad": 0.2,
            #           })

    return






if __name__ == "__main__":
    vargs = args()
    fileName = getFileName(vargs.site, vargs.param)
    exploreMooring(fileName)




