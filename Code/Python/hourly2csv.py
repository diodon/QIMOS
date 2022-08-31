#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import pandas as pd
import xarray as xr


def args():
    parser = argparse.ArgumentParser(description="Convert LSTP hourly file to CSV file")
    parser.add_argument('-filename', dest='fileName', help='filename of the hourly product',
                        type=str, default=None, required=True)
    vargs = parser.parse_args()
    return(vargs)

def hourly2csv(fileName):
    """
    Convert an hourly LTSP file into a csv file.
    It will produce the same file name but with a csv extension
    and metadata in _MD.csv file
    :param fileName: name of the file to convert
    :return: nothing
    """

    outFileName = (fileName.split('.nc')[0]).split('/')[-1]
    with xr.open_dataset(fileName) as nc:

        ## get metadata
        nObs = []
        timeStart = []
        timeEnd = []
        nInstruments =list(nc.INSTRUMENT.values)
        instrumentsID = list(np.unique(nc.instrument_id))
        instrumentsID = [i.decode('UTF8') for i in instrumentsID]
        latList = list(nc.LATITUDE.values)
        lonList = list(nc.LONGITUDE.values)
        ndepthList = list(nc.NOMINAL_DEPTH.values)
        siteCode = nc.site_code

        nc = nc.drop_vars(['instrument_id', 'source_file'])
        gg = nc.groupby('instrument_index')

        ## do the first instrument
        print('Processing site {site} INSTRUMENT 0'.format(site=siteCode), end=' ', flush=True)
        nc0 = gg[0]
        ## get metadata
        nObs.append(len(gg[0].OBSERVATION))
        timeStart.append(str(gg[0].TIME.min().dt.strftime('%Y-%m-%dT%H:%M:%S').values))
        timeEnd.append(str(gg[0].TIME.max().dt.strftime('%Y-%m-%dT%H:%M:%S').values))
        ## get data
        nc0 = nc0.drop_dims('INSTRUMENT')
        df = nc0.to_pandas()
        df.to_csv(outFileName + '.csv', header=True, index=False, mode='w')

        #loop over the rest of the instruments
        for i in range(1, len(gg)):
            print(i, end=' ', flush=True)
            ## get metadata
            nObs.append(len(gg[i].OBSERVATION))
            timeStart.append(str(gg[i].TIME.min().dt.strftime('%Y-%m-%dT%H:%M:%S').values))
            timeEnd.append(str(gg[i].TIME.max().dt.strftime('%Y-%m-%dT%H:%M:%S').values))
            ## get data
            nc0 = gg[i]
            nc0 = nc0.drop_dims('INSTRUMENT')
            df = nc0.to_pandas()
            df.to_csv(outFileName + 'csv', header=False, index=False, mode='a')

    dfMetadata = pd.DataFrame({'instrumentID': nInstruments,
                               'instrumentName': instrumentsID,
                               'nominalDepth': ndepthList,
                               'latitude': latList,
                               'longitude': lonList,
                               'startTime': timeStart,
                               'endTime': timeEnd,
                               'nObservations': nObs})

    dfMetadata.to_csv(outFileName + '_MD.csv', header=True, index=False, mode='w')

    print(flush=True)
    print('LTSP hourly product for {site} was written to {fname}'.format(site=siteCode, fname=outFileName + '.csv'))
    print('LTSP hourly product METADATA for {site} was written to {fname}'.format(site=siteCode, fname=outFileName + '_MD.csv'))

    return


if __name__ == "__main__":
    vargs = args()
    fileName = vargs.fileName
    if "hourly" not in fileName:
        print("not a LTSP hourly file. EXIT")
    else:
        hourly2csv(fileName)


