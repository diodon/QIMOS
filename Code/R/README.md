# R Tools for gridded products

this is a set of function to extract data and information fron AODN ANMN temperature gridded product.

- `getGriddedFileName`: return the name of the temperature gridded product based on site code. Note that every time the product is updated the name of tha file changes
- `fileDescrition`: extract metadata from the gridded file
- `getGriddedTemp`: extract the temperature timeseries from the gridded product at on particular depth. Optionally the output could be filtered by date

