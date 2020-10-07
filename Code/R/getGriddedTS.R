## Get time series from gridded
library(ncdf4)

getGriddedFileName = function(site){
  urlGeoServer = paste0("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='", site, "')")
  df = read.csv(url(urlGeoServer))
  fileName = df$url[grepl("gridded_timeseries", df$url)]
  return(fileName)
}


fileDescription = function(nc){
  sourceFile = ncatt_get(nc,0,"source_file")$value
  print(paste0("SOURCE FILE: ", sourceFile))
  print(paste0("SITE: ", ncatt_get(nc,0,"site_code")$value))
  print(paste0("FACILITY: ", strsplit(sourceFile, "/")[[1]][[3]]))
  latMean = mean(ncatt_get(nc,0,"geospatial_lat_min")$value, ncatt_get(nc,0,"geospatial_lat_max")$value)
  lonMean = mean(ncatt_get(nc,0,"geospatial_lon_min")$value, ncatt_get(nc,0,"geospatial_lon_max")$value)
  print(paste0("LOCATION: ", latMean, " / ", lonMean))
  print(paste0("TIME COVERAGE: ", ncatt_get(nc,0,"time_coverage_start")$value, " - ", ncatt_get(nc,0,"time_coverage_end")$value))
  print(paste0("AVAILABLE DEPTHS: ", paste0(ncvar_get(nc, "DEPTH"), collapse=", ")))
}

getGriddedTemp = function(site, depth, dateStart="1970-01-01", dateEnd = Sys.Date(), saveFile=FALSE){
  #site="GBRPPS"
  #depth = 20
  
  webRoot = 'http://thredds.aodn.org.au/thredds/dodsC/'
  fileName = getGriddedFileName(site)
  nc = nc_open(paste0(webRoot, fileName))
  
  depthList = ncvar_get(nc, 'DEPTH')
  
  if (!depth %in% depthList){
    print(paste0("ERROR: requested DEPTH (", depth, "m) is not available"))
    fileDescription(nc)
  }else {
    ## get depth index
    depthIndex = which(depthList==depth)
    ## get variables
    TS.time = ncvar_get(nc, "TIME")
    TS.time = as.POSIXct(TS.time*60*60*24, origin = "1950-01-01")
    TS.temp = ncvar_get(nc, "TEMP")[depthIndex,]
    nc_close(nc)
    df = data.frame(TIME=TS.time, TEMP=TS.temp)
    ## filter dates
    df = df[df$TIME>=as.POSIXct(dateStart) & df$TIME<=as.POSIXct(dateEnd),]
  
    ## write file
    outFileName = NA
    if (saveFile){
      outFileName = paste0(paste(site,"TEMP", paste0(depth,"m"), 
                          paste0(format(min(TS.time), "%Y%m%d"),"-", format(max(TS.time), "%Y%m%d")),
                          sep = "_"),".csv")
      write.csv(file=outFileName, df, row.names = FALSE)
    }
    
    return(list(DATA=df, outputFileName=outFileName))
  }
}


