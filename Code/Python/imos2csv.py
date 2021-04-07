## transform IMOS LTSP netCDF to cvs, with metadata on the top
import argparse
import os
import xarray as xr
import pandas as pd


def imos2csv(fileName, output_path):
    with xr.open_dataset(fileName) as nc:
        siteCode = nc.site_code
        dateStart = fileName.split("/")[-1].split("_")[3]
        dateEnd = fileName.split("/")[-1].split("_")[7].replace('END','')
        fileNameCSV = os.path.join(output_path, "_".join([siteCode, dateStart+dateEnd])+'.csv')

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

        df = nc.to_dataframe()
        df['source_file'] = df['source_file'].str.decode('utf-8')
        df['instrument_id'] = df['instrument_id'].str.decode('utf-8')
        df.to_csv(fileNameCSV, sep='\t', index=False, mode='a')

    return [fileNameCSV, len(metadata)]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert IMOS hourly LTSP to tab separated file with metadata on top")
    parser.add_argument('-file', dest='fileName', help="name of hourly netCDF LTSP", required=True)
    parser.add_argument('-path', dest='output_path', help="path where the result file will be written. Default ./",
                        default="./", required=False)
    args = parser.parse_args()
    result = imos2csv(args.fileName, args.output_path)
    print('CONVERSION DONE!')
    print('TSV file name: ' + result[0])
    print('metadata from line 1 thru line ' + str(result[1]))
    print('data start at line ' + str(result[1]+1))




