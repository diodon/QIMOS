import argparse
import pandas as pd

pd.set_option('display.max_colwidth', None)

def args():
    parser = argparse.ArgumentParser(description="Get LTSP file name")
    parser.add_argument('-site', dest='site', help='site code, like NRMMAI',  type=str, default=None, required=True)
    parser.add_argument('-product',dest='product', help='product type: aggregated, hourly, velocity-hourly or gridded', type=str, default='hourly', required=True)
    parser.add_argument('-QC',dest='QC', help='for the hourly, QCed data only. Default True', type=bool, default=True, required=False)
    parser.add_argument('-param',dest='param', help='for the aggregated, parameter, like TEMP, or "velocity"', type=str, default='TEMP', required=False)
    parser.add_argument('-weburl',dest='webURL', help='url root for the file: S3: Amazon AWS (for download, fastest), wget (AODN THREDDS, for download), opendap (AODN THREDDS to open remotely). Default opendap', type=str, default='opendap', required=False)

    vargs = parser.parse_args()
    return(vargs)


def getLTSPfileName(site, product="gridded", QC=True, param="TEMP", webURL="opendap"):
    '''
    get the url of the LTSP files
    
    require: pandas
    site: the site_code
    product: product type )aggregated, hourly or gridded)
    QC: for the hourly, include only good data (default True)
    param: for aggregated product, parameter code as IMOS standard (e.g. TEMP)
    webURL: web source of the file (S3: Amazon AWS (fastest), wget (AODN THREDDS, to download),
            opendap (AODN THREDDS to open remotely)
    E. Klein. eklein at ocean-analytics dot com dot au
    '''
    
    if webURL == "opendap": 
        WEBROOT = 'http://thredds.aodn.org.au/thredds/dodsC/'
    elif webURL == "wget":
        WEBROOT = 'http://thredds.aodn.org.au/thredds/fileServer/'
    elif webURL == "S3":
        WEBROOT = 'https://s3-ap-southeast-2.amazon.com/imos-data/'
    else:
        print("ERROR: wrong webURL: it must be one of S3, opendap or wget")

  
    urlGeoServer = "http://geoserver-123.aodn.org.au/geoserver/ows?typeName=moorings_all_map&SERVICE=WFS&REQUEST=GetFeature&VERSION=1.0.0&outputFormat=csv&CQL_FILTER=(realtime='FALSE')and(site_code='" + site + "')"
    df = pd.read_csv(urlGeoServer)
    url = df['url']
    
    #fileName = df$url[grepl(paste0(product,"-timeseries"), df$url)]
    fileName = "TEST"
    
    
    if product == "gridded": 
        fileName = url[url.str.contains("gridded")]
    elif product=="velocity-hourly":
        fileName = url[url.str.contains("velocity-hourly")]
    elif product=="hourly":
        if QC:
            fileName = url[url.str.contains("(?<!velocity-)hourly-timeseries(?!-including)", regex=True)]
        else:
            fileName = url[url.str.contains("including-non")]
    elif product=="aggregated":
        fileName = url[url.str.contains(param) & url.str.contains("aggregated")]
    else:
        print("ERROR: invalid combination of arguments or wrong names")

    
    return WEBROOT + fileName.to_string(index=False, header=False).strip()


if __name__ == "__main__":
    vargs = args()
    print(getLTSPfileName(**vars(vargs)))
    


