#' GetLTSPfilename
#' General function to get to name of the LTSP file
#' 
#' @param site The site name according to IMOS conventions
#' @param product aggregated, hourly, velocity-hourly or gridded (default)
#' @param QC for the hourly product include only QC data
#' @param param for the aggretated, the name of the parameter, like TEMP (default). For the hourly select VELOCITY or non-VELOCITY (default)
#' @param webURL webroot for the file. returns S3, opendap (default) or wget url path root
#'
#' @details 
#' The file name of the LTSP aggregated product will change everytime the product is updated. 
#' The file could be downloaded or accessed from Amazon S3, or AODN THREDDS server. The later provides HTTP and openDAP access.
#' If the product requested is hourly and parameter is velocity, hourly velocity product filenam,e will be returned, otherwise, the nopn-velocity product.
#' If the product is aggregated you must specify the parameter required using IMOS naming standards (TEMP by default).
#' the webroot url selected will be pasted to the the filename
#' 
#' @return character: name of the file
#'
#' @author Eduardo Klein. ekleins@gmail.com
#' @source 
#' QIMOS - tools for Queensland IMOS subfacility 
#' https://github.com/diodon/QIMOS/tree/main/Code/R
#' 
#' @examples
#' 
#' 
#' 
#' 
getLTSPfileName = function(site, product="gridded", QC=TRUE, param="TEMP", webURL="opendap"){
  if (webURL == "opendap"){ 
    WEBROOT = 'http://thredds.aodn.org.au/thredds/dodsC/'
  }else if (webURL == "wget"){
    WEBROOT = 'http://thredds.aodn.org.au/thredds/fileServer/'
  }else if (webURL == "S3"){
    WEBROOT = 'https://s3-ap-southeast-2.amazon.com/imos-data/'
  }else {
    print("ERROR: wrong webURL: it must be one of S3, opendap or wget")
  }
  
  urlGeoServer = paste0("http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='", site, "')")
  df = read.csv(url(urlGeoServer))
  fileName = df$url[grepl(paste0(product,"-timeseries"), df$url)]
  
  if (product == "gridded"){
    fileName = fileName[grepl("gridded-timeseries", fileName)]
  }else if(product=="velocity-hourly"){
    fileName = fileName[grepl("velocity-hourly", fileName)]
  }else if(product=="hourly"){
    if (QC){
      fileName = fileName[grepl("(?<!velocity-)hourly-timeseries(?!-including)", fileName, perl = TRUE)]
    }else {
      fileName = fileName[grepl("including-non", fileName)]
    }
  }else if (product=="aggregated"){
      fileName = fileName[grepl(param, fileName)]
    }else {
    print("ERROR: invalid combination of arguments or wrong names")
  }
  return(paste0(WEBROOT,fileName))
}
