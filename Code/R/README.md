# R Tools for gridded products

this is a set of functions to extract data and information from AODN ANMN temperature gridded product.

-   `getGriddedFileName`: return the name of the temperature gridded product file based on site code. Note that every time the product is updated the name of the file changes
-   `fileDescrition`: extract metadata from the gridded file
-   `getGriddedTemp`: extract the temperature timeseries from the gridded product at a particular depth. Optionally, the output could be filtered by date
-   `getProfileTS`: extract variables from biogeochem profiles files and integrate into a data frame. Also provides a metadata dataframe for each profile
-   `getMMM` is a small function to retrieve MMM and DHWmax from NOAA coral reef watch product. The files are conveniently packed into one aggregated file that covers the GBR region. The DHWmax file `DHWGBR_all.nc` is in netCDF classic format. The .old version is the same file but in ncdf4 version. Apparently, windows implementation of the ncdf4 package has problems with this more compact format.
-   `getSSTAARS` is a small function to retrieve the [SSTAARS climatology](https://doi.org/10.1016/j.jmarsys.2018.07.005) from a coordinate pair. It needs the nc file in the same directory of the code. The climatology file for the GBR can be downloaded from [here](https://drive.google.com/drive/folders/1mtkG0rWfbjRMyd7EnDfWA7R7arn6EdW_?usp=sharing) (as it is too big for GitHub). For windows user please use the "classic" version ( and modify the code to read this file). Apparently, windows implementation of the ncdf4 package has problems with the more modern version 4 format.
