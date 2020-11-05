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