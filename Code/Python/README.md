# Python tools for AODN ANMN files

Set of functions to extract information and data from AODN ANMN products


## Explore AODN Velocity or Temperature files

Discover the individual files (velocity or temperature) from one ANMN site. Get basic metadata and optionally save the list of file names


`exploreMooring.py`

``` 
usage: exploreMooring.py [-h] -site SITE -param PARAM

Explore velocity or temperature AODN individual files

optional arguments:
  -h, --help    show this help message and exit
  -site SITE    site code, like NRMMAI
  -param PARAM  parameter, like V for velocity, T temperature

```


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


## Convert hourly LTSP to a csv file with accompanying metadata file

given the hourly aggregated file URL, the tools extract all variables and write a tabular csv file. An additional file with metadata for each instrument is also produced

`hourly2csv.py`

```
usage: hourly2csv.py [-h] -filename FILENAME

Convert LSTP hourly file to CSV file

optional arguments:
  -h, --help          show this help message and exit
  -filename FILENAME  filename of the hourly product
```



[//]: # (## Convert an hourly aggregated time series file into a tab-separated file with metadata on top)

[//]: # ()
[//]: # (This small script will extract variables from IMOS hourly aggregated netCDF file into a tab separated file, between two dates. The metadata extracted from the file global attributes is at the top. )

[//]: # (The missing value for all the variables is set to -99999.)

[//]: # (The run will return the TSV file name, the lines corresponding the metadata and the start line of the data.)

[//]: # (If the date range is too big it will crash due to memory limitations.)

[//]: # ()
[//]: # (`imos2csv.py`)

[//]: # ()
[//]: # (```)

[//]: # (usage: imos2csv.py [-h] -file FILENAME -param PARAM [PARAM ...] -ds STARTDATE)

[//]: # (                   -de ENDDATE [-path OUTPUT_PATH])

[//]: # ()
[//]: # (Convert IMOS hourly LTSP to tab separated file with metadata on top)

[//]: # ()
[//]: # (optional arguments:)

[//]: # (  -h, --help            show this help message and exit)

[//]: # (  -file FILENAME        name of hourly netCDF LTSP)

[//]: # (  -param PARAM [PARAM ...])

[//]: # (                        parameter to extract. Default TEMP)

[//]: # (  -ds STARTDATE         start date in YYYY-MM-DD)

[//]: # (  -de ENDDATE           end date in YYYY-MM-DD)

[//]: # (  -path OUTPUT_PATH     path where the result file will be written. Default ./)

[//]: # ()
[//]: # (```)

## Extract one variable from hourly LTSP 

This function will extract one variable (e.g. TEMP) from the ragged array structured hourly LTPS and returns a netCDF file with NOMINAL_DEPTH and TIME as dimensions in a rectangular array.  The attributes of the original file are preserved and updated. To run the function, call it from a python script with the following arguments: 

`extractVariable.py`

```
getVariable(fileName, varname):
    Extract a single variable from hourly LTSP
    E Klein 20210823
    :param fileName: name of the LTSP hourly file
    :param varname: nae of the variable, like TEMP
    :return: netCDF dataset
```

Example: 

```buildoutcfg
ds = getVariable('http://thredds.aodn.org.au/thredds/dodsC/IMOS/ANMN/QLD/PIL050/hourly_timeseries/IMOS_ANMN-QLD_BOSTZ_20120221_PIL050_FV02_hourly-timeseries_END-20140816_C-20210428.nc', 'TEMP')

print(ds)
<xarray.Dataset>
Dimensions:        (NOMINAL_DEPTH: 16, TIME: 21771)
Coordinates:
  * NOMINAL_DEPTH  (NOMINAL_DEPTH) float32 17.0 23.0 24.8 ... 49.8 51.0 54.0
  * TIME           (TIME) datetime64[ns] 2012-02-21T04:00:00 ... 2014-08-16T0...
Data variables:
    TEMP           (NOMINAL_DEPTH, TIME) float64 30.21 30.22 30.1 ... nan nan
    DEPTH          (NOMINAL_DEPTH, TIME) float64 17.54 17.05 16.52 ... nan nan
Attributes:
    Conventions:                 CF-1.6,IMOS-1.4
    abstract:                    Hourly Time Series Product: This file contai...
    acknowledgement:             Any users of IMOS data are required to clear...
    author:                      Klein, Eduardo
    author_email:                e.klein@aims.gov.au
    citation:                    The citation in a list of references is: "IM...
    contributor_email:           adc@aims.gov.au; c.steinberg@aims.gov.au
    contributor_name:            Australian Institute of Marine Science; AIMS...
    contributor_role:            author; principal_investigator
    data_centre:                 Australian Ocean Data Network (AODN)
    data_centre_email:           info@aodn.org.au
    date_created:                2021-08-24T19:59:36
    disclaimer:                  Data, products and services from IMOS are pr...
    featureType:                 timeSeries
    file_version:                Level 2 - Quality Controlled Data
    generating_code_version:     1.4.7
    geospatial_lat_max:          -20.0544333333
    geospatial_lat_min:          -20.0547833333
    geospatial_lon_max:          116.4161833333
    geospatial_lon_min:          116.4158166667
    geospatial_vertical_max:     50.79277801513672
    geospatial_vertical_min:     14.894384384155273
    history:                     2021-04-28T08:29:02Z: Hourly aggregated file...
    included_values_flagged_as:  Good_data, Probably_good_data
    institution_references:      http://imos.org.au/facilities/aodn/
    keywords:                    DEPTH, TEMP, HOURLY, AGGREGATED
    keywords_vocabulary:         IMOS parameter names. See https://github.com...
    license:                     http://creativecommons.org/licenses/by/4.0/
    lineage:                     The variables of interest (VoI) are produced...
    naming_authority:            IMOS
    project:                     Integrated Marine Observing System (IMOS)
    references:                  http://www.imos.org.au
    rejected_files:              
    site_code:                   PIL050
    source:                      Mooring
    standard_name_vocabulary:    NetCDF Climate and Forecast (CF) Metadata Co...
    time_coverage_end:           2014-08-16T06:00:00Z
    time_coverage_start:         2012-02-21T04:00:00Z
    title:                       Long time series Hourly Aggregated product: ...
    DODS.strlen:                 256
    DODS.dimName:                string256

```
