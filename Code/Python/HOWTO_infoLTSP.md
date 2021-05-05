## HOW-TO: get information from LTSP files

<a id='TOC'></a>
### Table of Contents

* [Introduction](#ZERO)
* [File Types](#ONE)
* [Format of the Files](#TWO)
* [Getting the File Name](#THREE)
* [Hourly Product INFO](#FOUR)
* [Gridded Product INFO](#FIVE)


<a name="ZERO"></a>
### INTRODUCTION

----------------------- 

IMOS-AODN regularly publish a set of products that combine and aggregate the values of the oceanographic variables collected at the ANMN mooring arrays. Normally, every deployment from each of the instruments are stored in individual files and that makes difficult to analyse different deployments and/or parameter together. 

This guide hows how to use a set of functions that allows to discover the LTSP files and extract some information valuable for future anaysis.

<a name="ONE"></a> 
### FILE TYPES

----------------------
IMOS LTSP comprises five different products: 

- Non-velocity products (exclude all velocity related parameters):
    - Aggregated file: one parameter aggregated into one file with all the deployments from a site. 
    - Hourly aggregated file: all parameters from all instruments deployed at one site, aggregated (mean or median depending on the parameter) into one-hour bins. This product has two variants: one that includes only good-quality data and another with all the data, disregarding the QC performed on the values.
    - Gridded aggregated. Only Temperature. The file contains a regular grid of interpolated temperature values in the water column. The depth intervals depend on the location of the instruments in the mooring array.
    
- Velocity products (only water current components):
    - Aggregated file: velocity related parameters (u, v, w and scalar water speed) aggregated into one file with all the deployments from a site. 
    - Hourly aggregated file: velocity related parameters (u, v, w and scalar water speed) from all instruments deployed at one site, aggregated (mean or median depending on the parameter) into one-hour bins. This product has two variants: one that includes only good-quality data and another with all the data, disregarding the QC performed on the values.
    
<a name="TWO"></a> 
### FILE FORMAT 

-------------------------

Normally, every instrument recovered from a mooring array represents an individual file in the [IMOS THREDDS server](http://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/catalog.html). This characteristic that facilitates the individual quality control and metadata handling pose some challenges for the analysis of long time series: 

- Many files for one time series
- Instruments deployed to varying depths
- Instruments sample at different times
- Significant work and expert knowledge required to view and analyse time series
- Different user groups need different products (gridded density, MLD, data combined from multiple sources, plots, etc…)

The hourly aggregated product is a file that aggregates all the variables from one site into one-hour bins. 

The aggregated file is a netCDF 4 file organised in an [Indexed Ragged Array](http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_indexed_ragged_array_representation) structure that follows the Climate-Forecast conventions and IMOS netCDF file conventions (*diagram by M. Hidas*): 

![Indexed Ragged Array](./img/indexedraggedarray.png)

Some characteristics of this structure:

- `TIME` is no longer a dimension. That means that the ordinary selecting and plotting methods for CF netCDF are no longer available. `TIME` is one of the variables in the file.
- the dimensions of the file are `OBSERVATION` and `INSTRUMENT`. As the aggregation process combine instruments that normally have common timestamps, the time variable could have repeated values. Also each deployment (instrument) is identified by and index and the compound instrument name, make, serial. In this way it is easy to filter according to specific instruments.


The aggregation takes the variable values half an hour before the hour and half an hour after the hour and reduce the variable values by calculating the mean or the median. Additional variables resulting from the aggregation process are also available in the file, as ancillary variables.

![hourly aggregation](./img/BurstAveraging.png)



