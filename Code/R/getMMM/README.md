# getMMM funtion

This function will extract the MMM and the DHW maximum values for years 1985-2020. It is restricted to the Great Barrier Reef area.

It needs the MMM.nc and DHWGBR_all.nc located in the same directory of the function. For windows users please use the netCDF "classic" format version (DHWGBR_all.nc.old, and modify the code to read this file). Apparently, windows' implementation of the ncdf4 package has problems reading the more modern netCDF version 4 format.

## Call: 

`getMMM(lat, lon)`


## Arguments: 

*`lat`* = vector of latitudes, in decimalk degrees (negative)  
*`lon`* = vector of longitudes in decimal degrees  

It returns a named list with MMM as numeric and DHWmax as a dataframe with year and its corresponding DHWmax

## Example:

```
getMMM(lat=-15.5, lon=155.0)

$MMM  
28.69 

$DHWmax
   year DHWmax
1  1985   0.69
2  1986   0.50
3  1987   1.23
4  1988   0.77
5  1989   0.70
6  1990   0.00
7  1991   3.57
8  1992   0.36
9  1993   0.00
10 1994   0.88
11 1995   0.61
12 1996   4.82
13 1997   0.78
14 1998   0.78
15 1999   0.00
16 2000   0.00
17 2001   2.70
18 2002   5.16
19 2003   0.00
20 2004   7.11
21 2005   2.83
22 2006   0.00
23 2007   0.84
24 2008   4.03
25 2009   9.47
26 2010   1.99
27 2011   1.94
28 2012   2.12
29 2013   1.83
30 2014   0.21
31 2015   0.15
32 2016   4.20
33 2017  12.15
34 2018   1.67
35 2019   0.31
36 2020   6.10
```
