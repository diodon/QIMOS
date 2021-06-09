## get MMM and DHWmax from a vector of coordinates
## requires raster
## requires DHWmax and MMM netcdf files
## input lat,lon
## return list with MMM and DHWmax for each year
## E Klein. eklein@ocean-analytics.com.au 

getDHWmax = function(lat, lon, yMin = 1985, yMax=2020){
  ## check packages
  require(raster)

  ## read MMM and DHW files. Change the path as needed
  MMMFile = "MMM.nc"
  DHWmaxFile = "DHWGBR_all.nc"
  
  xyPoint = SpatialPoints(cbind(lon, lat))
  DHW = stack(DHWmaxFile)
  yearList = as.numeric(substr(names(DHW),2,5))
  DHWList = as.numeric(raster::extract(DHW, xyPoint))
  
  MMM = raster(MMMFile)
  MMMvalue = raster::extract(MMM, xyPoint)
  DHWmax = data.frame(year= yearList, 
                      DHWmax = DHWList)
  DHWmax = DHWmax[DHWmax$year>=yMin & DHWmax$year<=yMax,]
  
  return(list(MMM=MMMvalue, DHWmax = DHWmax))

}
