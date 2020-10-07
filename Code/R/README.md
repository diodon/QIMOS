# R Tools for gridded products

this is a set of functions to extract data and information from AODN ANMN temperature gridded product.

- `getGriddedFileName`: return the name of the temperature gridded product file based on site code. Note that every time the product is updated the name of the file changes
- `fileDescrition`: extract metadata from the gridded file
- `getGriddedTemp`: extract the temperature timeseries from the gridded product at a particular depth. Optionally, the output could be filtered by date

