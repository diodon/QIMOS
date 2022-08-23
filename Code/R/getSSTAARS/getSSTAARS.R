## get SSTAARS climatology for a coordinate
## requires raster
## requires SSTAARS netcdf file in the same directory
## input lat,lon
## return data frame with SSTAARS TEMP climatology
## E Klein. eklein@ocean-analytics.com.au 

getSSTAARS = function(lat, lon){
  ## check packages
  require(raster)
  SSTAARSFile = "./SSTAARS_climatology_GBR.nc"
  xyPoint = SpatialPoints(cbind(lon, lat))
  SST = stack(SSTAARSFile)
  temp = extract(SST, xyPoint)
  return(data.frame(yday = 1:365, temp = temp[1,], row.names = NULL))
}
