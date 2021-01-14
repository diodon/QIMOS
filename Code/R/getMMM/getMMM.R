## get MMM and DHWmax for a coordinate
## requires raster
## requires DHWmax and MMM netcdf files
## input lat,lon
## return list with MMM and DHWmax for each year
## E Klein. eklein@ocean-analytics.com.au 

getMMM = function(lat, lon){
  ## check packages
  require(raster)

  MMMFile = "/home/eklein/Proyectos/AIMS/SST/NOAA/MMM.nc"
  DHWmaxFile = "/home/eklein/Proyectos/AIMS/NOAA/DHWmax/DHWGBR_all.nc"
  
  xyPoint = SpatialPoints(cbind(lon, lat))
  DHW = stack(DHWmaxFile)
  yearList = as.numeric(substr(names(DHW),2,5))
  DHWList = as.numeric(raster::extract(DHW, xyPoint))
  
  ## get DHW2020. This is temporal while NOAA publishs the 2020 file
  # DHW2020File = "/home/eklein/Proyectos/AIMS/NOAA/DHW2020/GBRDHWmax_2020.nc"
  # DHW2020 = raster(DHW2020File, varname="DHWmax")
  # DHW2020value = raster::extract(DHW2020, xyPoint)
  # DHWList = c(DHWList, DHW2020value)
  
  
  MMM = raster(MMMFile)
  MMMvalue = raster::extract(MMM, xyPoint)
  
  return(list(MMM=MMMvalue, DHWmax = data.frame(year = yearList, DHWmax = DHWList)))
}
