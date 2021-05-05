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


