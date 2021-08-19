## transform IMOS LTSP netCDF to cvs, with metadata on the top
import argparse
import os
import sys

import xarray as xr
import pandas as pd
import numpy as np


def imos2csv(fileName, param, startDate, endDate, output_path='./'):
    '''
    Extract variables from hourly aggregated LTSP between two dates
    and save it in a tsv file with metadata on top
    E. Klein. eklein at ocean-analytics.com.au
    :param fileName: name of the hourly aggregate netCDF file
    :param param: list of parameter to extract
    :param startDate: start date YYYY-MM-DD
    :param endDate: end date YYYY-MM-DD
    :param output_path: path where to write the resulting file
    :return:
    '''

    ## for file name
    dateStart = startDate.replace("-", "")
    dateEnd = endDate.replace("-", "")
    #for filtering
    startDate = np.datetime64(startDate)
    endDate = np.datetime64(endDate)
    print(param)

    with xr.open_dataset(fileName) as nc:
        ## file name
        siteCode = nc.site_code
        fileNameCSV = os.path.join(output_path, "_".join([siteCode, (dateStart+'-'+dateEnd)])+'.csv')

        ## update and save attrs
        nc.attrs['time_coverage_start'] = startDate
        nc.attrs['time_coverage_end'] = endDate
        attNames = list(nc.attrs.keys())
        attNames = [item + ': ' for item in attNames]
        attValues = list(nc.attrs.values())
        attValues = [str(item) for item in attValues]
        metadata = [i + j for i, j in zip(attNames, attValues)]
        metadata.append('missing_value: -99999')
        metadata = sorted(metadata)

        with open(fileNameCSV, 'w') as ff:
            for item in metadata:
                ff.write('%s\n' %item)

        ## select parameter and date range
        selectedParam = ['instrument_index', 'instrument_id', 'TIME', 'DEPTH']
        [selectedParam.append(item) for item in param]
        nc = nc[selectedParam]
        nc = nc.drop(['LATITUDE', 'LONGITUDE', 'NOMINAL_DEPTH'])
        nc = nc.where((nc.TIME>=startDate) & (nc.TIME<=endDate), drop=True)
        df = nc.to_dataframe()
        df['instrument_id'] = df['instrument_id'].str.decode('utf-8')
        df.to_csv(fileNameCSV, sep='\t', index=False, mode='a')

    return [fileNameCSV, len(metadata), len(df)]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert IMOS hourly LTSP to tab separated file with metadata on top")
    parser.add_argument('-file', dest='fileName', help="name of hourly netCDF LTSP", required=True)
    parser.add_argument('-param', dest='param', help="parameter to extract. Default TEMP", nargs='+', default='TEMP', required=True)
    parser.add_argument('-ds', dest='startDate', help="start date in YYYY-MM-DD", required=True)
    parser.add_argument('-de', dest='endDate', help="end date in YYYY-MM-DD", required=True)
    parser.add_argument('-path', dest='output_path', help="path where the result file will be written. Default ./",
                        default="./", required=False)
    args = parser.parse_args()
    result = imos2csv(args.fileName, args.param, args.startDate, args.endDate, args.output_path)
    print('CONVERSION DONE!')
    print('TSV file name: ' + result[0])
    print('metadata from line 1 thru line ' + str(result[1]))
    print('data start at line ' + str(result[1]+1))
    print('total number of data records: ' + str(result[2]))
    





