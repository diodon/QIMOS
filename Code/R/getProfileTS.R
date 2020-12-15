## function to get a timeseries of parameters from biogeochemical profiles files
## requires ncdf4, dplyr, stringr
## requires a list of (opendap) files. Use geoserverCatalog.py to get the file names
## requires parameters name vector 
## verbose.TRUE to print info
## return a list of dataframes with data and metadata
## Eduardo Klein. ekleins@gmail.com
# Tue Dec 15 17:41:05 2020 ------------------------------

getProfileTS = function(paramList, fileList, verbose=TRUE){

  ## check packages
  require(ncdf4)
  require(stringr)
  require(dplyr)
  
  df = data.frame()
  dfMD = data.frame()
  for (profileID in 1:length(fileList)){
    if (verbose){print(fileList[profileID])}
    nc = nc_open(fileList[profileID])
    
    ## get TIME and DEPTH
    DEPTH = ncvar_get(nc, "DEPTH")
    nDepths = length(DEPTH)
    TIME = ncvar_get(nc, "TIME")
    TIMEorigin = gsub("days since ", "", ncatt_get(nc, "TIME")$units)
    TIME = as.POSIXct(TIME*60*60*24, origin=TIMEorigin, tz="UTC")
    dfTemp = data.frame(profileID = rep(profileID, nDepths), TIME, DEPTH)
    
    ## get metadata
    ncAttr = ncatt_get(nc, 0)
    dfMD = bind_rows(dfMD,
                     data.frame(profileID,
                                site_code = ncAttr$site_code,
                                latitude = mean(as.numeric(ncAttr$geospatial_lat_min), as.numeric(ncAttr$geospatial_lat_max)),
                                longitude = mean(as.numeric(ncAttr$geospatial_lon_min), as.numeric(ncAttr$geospatial_lon_max)),
                                time_start = ncAttr$time_deployment_start,
                                time_end = ncAttr$time_deployment_end,
                                instrument = ncAttr$instrument,
                                instrument_sn = ncAttr$instrument_serial_number,
                                file_name = str_split(fileList[profileID], "/", simplify = T)[11]))
    
    ## get variables from file
    varNames = names(nc$var)
    for (param in paramList){
      if (verbose) print(param)
      if (param %in% varNames){
        varValue = ncvar_get(nc, param)
        varValueQC = ncvar_get(nc, paste0(param,"_quality_control"))
      }else {
        varValue = rep(NA, nDepths)
        varValueQC = rep(NA, nDepths)
        if (verbose) print(paste0("Parameter ", param, " not found in file"))
      }
      dfTemp = bind_cols(dfTemp, varValue=varValue, varValueQC=varValueQC)
      names(dfTemp)[names(dfTemp)=="varValue"] = param
      names(dfTemp)[names(dfTemp)=="varValueQC"] = paste0(param, "_quality_control")
    }
    nc_close(nc)
    df = bind_rows(df, dfTemp)
  }
  return(list(data=df, dfMetadata=dfMD))
}
