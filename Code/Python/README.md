# Python tools for extracting TEMP timeseries form gridded product

Set of functions to extract information and data from AODN ANMN gridded product

## Get gridded LTSP information

Print a table of basic information about the gridded product. Just pass the site code.

`infoLTSP.py`

```
usage: infoLTSP.py [-h] -site SITE

Produce information about LTSP gridded product

optional arguments:
  -h, --help  show this help message and exit
  -site SITE  site code, like NRMMAI

```

## Extract temperature timeseries at depth

`NRSgetTS.py`

```
python NRSgetTS.py --help
usage: NRSgetTS.py [-h] -site SITE -depth DEPTH [-ts DATESTART] [-te DATEEND]

Get a TEMP timeseries from the gridded product at specified DEPTH

optional arguments:
  -h, --help     show this help message and exit
  -site SITE     site code, like NRMMAI
  -depth DEPTH   selecyted depth, like 10
  -ts DATESTART  start time like 2015-12-01
  -te DATEEND    end time like 2018-06-30
```

## Get product filename from THREDDS

This return the file name or a list of file names of particular products according to many filters

`geoserverCatalog.py` 

```
usage: geoserverCatalog.py [-h] [-var VARNAME] [-site SITE] [-ft FEATURETYPE]
                           [-fv FILEVERSION] [-ts TIMESTART] [-te TIMEEND]
                           [-dc DATACATEGORY] [-realtime]
                           [-exc FILTEROUT [FILTEROUT ...]]
                           [-inc FILTERIN [FILTERIN ...]] [-url WEBURL]

Get a list of urls from the AODN geoserver

optional arguments:
  -h, --help            show this help message and exit
  -var VARNAME          name of the variable of interest, like TEMP
  -site SITE            site code, like NRMMAI
  -ft FEATURETYPE       feature type, like timeseries
  -fv FILEVERSION       file version, like 1
  -ts TIMESTART         start time like 2015-12-01
  -te TIMEEND           end time like 2018-06-30
  -dc DATACATEGORY      data category like Temperature
  -realtime             indicates you also want realtime files
  -exc FILTEROUT [FILTEROUT ...]
                        regex to filter out the url list. Case sensitive
  -inc FILTERIN [FILTERIN ...]
                        regex to include files in the url list. case sensitive
  -url WEBURL           S3 -> amazon S3 prefix, opendap -> AODN OPeNDAP,
                        thredds -> AODN HTML THREDDS server

```

## get the file name of the LTSP

it returns the url of the LTSP product for remote open (opendap) or download (wget or Amazon S3)

`getLTSPname.py`

```
usage: getLTSPname.py [-h] -site SITE -product PRODUCT [-QC QC] [-param PARAM]
                      [-weburl WEBURL]

Get LTSP file name

optional arguments:
  -h, --help        show this help message and exit
  -site SITE        site code, like NRMMAI
  -product PRODUCT  product type: aggregated, hourly, velocity-hourly or
                    gridded
  -QC QC            for the hourly, QCed data only. Default True
  -param PARAM      for the aggregated, parameter, like TEMP, or "velocity"
  -weburl WEBURL    url root for the file: S3: Amazon AWS (for download,
                    fastest), wget (AODN THREDDS, for download), opendap (AODN
                    THREDDS to open remotely). Default opendap

```

## Convert an hourly aggregated time series file into a tab-separated file with metadata on top

This small script will extract variables from IMOS hourly aggregated netCDF file into a tab separated file, between two dates. The metadata extracted from the file global attributes is at the top. 
The missing value for all the variables is set to -99999.
The run will return the TSV file name, the lines corresponding the metadata and the start line of the data.
If the date range is too big it will crash due to memory limitations.

`imos2csv.py`

```
usage: imos2csv.py [-h] -file FILENAME -param PARAM [PARAM ...] -ds STARTDATE
                   -de ENDDATE [-path OUTPUT_PATH]

Convert IMOS hourly LTSP to tab separated file with metadata on top

optional arguments:
  -h, --help            show this help message and exit
  -file FILENAME        name of hourly netCDF LTSP
  -param PARAM [PARAM ...]
                        parameter to extract. Default TEMP
  -ds STARTDATE         start date in YYYY-MM-DD
  -de ENDDATE           end date in YYYY-MM-DD
  -path OUTPUT_PATH     path where the result file will be written. Default ./

```

