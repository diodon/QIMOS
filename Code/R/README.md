# R Tools for gridded products

this is a set of functions to extract data and information from AODN ANMN temperature gridded product.

- `getGriddedFileName`: return the name of the temperature gridded product file based on site code. Note that every time the product is updated the name of the file changes
- `fileDescrition`: extract metadata from the gridded file
- `getGriddedTemp`: extract the temperature timeseries from the gridded product at a particular depth. Optionally, the output could be filtered by date
- `getProfileTS`: extract variables from biogeochem profiles files and integrate into a data frame. Also provides a metadata dataframe for each profile
- `getMMM` is a small function to retrieve MMM and DHWmax from NOAA coral reef watch product. The files are conveniently packed into one aggregated file that covers the GBR region


