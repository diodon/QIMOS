## Extract a variable from hourly LTSP
## return a rectangular masked array with nominal depth as rows and time as columns
import sys
from datetime import datetime
import xarray as xr
import numpy as np
from numpy import ma

def getVariable(fileName, varname):
    '''
    Extract a single variable from hourly LTSP
    E Klein 20210823
    :param fileName: name of the LTSP hourly file
    :param varname: nae of the variable, like TEMP
    :return: netCDF dataset
    '''

    try:
        with xr.open_dataset(fileName) as nc:
            if 'Hourly Time Series Product' not in nc.abstract:
                print("ERROR: the file is not an hourly LTSP")
                return

            ## get variables
            param = nc[varname].values
            depth = nc.DEPTH.values
            time = nc.TIME.values.astype('datetime64[h]')
            nominalDepth = nc.NOMINAL_DEPTH.values
            instrumentID = nc.instrument_index.values
            instrumentUnique = np.unique(instrumentID)

            param_attrs = nc[varname].attrs
            depth_attrs = nc['DEPTH'].attrs
            nominalDepth_attrs = nc['NOMINAL_DEPTH'].attrs

            ## update global attrs
            todayDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            global_attrs = nc.attrs
            global_attrs['author_email'] = 'e.klein@aims.gov.au'
            global_attrs['date_created'] = todayDate
            global_attrs['keywords'] = 'DEPTH, ' + varname + ', HOURLY, AGGREGATED'
            global_attrs['history'] = global_attrs['history'] + ' ' + todayDate + \
                                      ': Transformed into rectangular array using https://github.com/diodon/QIMOS/blob/main/Code/Python/extractVariable.py'



        ## create empty matrix full depth/time range
        dateStart = min(time)
        dateEnd = max(time) + np.timedelta64(1, "h")
        timeSeq = np.arange(dateStart, dateEnd, dtype='datetime64[h]')

        ndSeq = np.unique(nominalDepth)

        ## uncomment to produce equally spaced depths
        # ndInc = 0.1
        # ndStart = min(nominalDepth)
        # ndEnd = max(nominalDepth) + ndInc
        # ndSeq = np.arange(ndStart, ndEnd, 0.1)


        param_fullMat = np.full([len(ndSeq), len(timeSeq)], np.nan)
        depth_fullMat = np.full([len(ndSeq), len(timeSeq)], np.nan)

        for i, instrument in enumerate(instrumentUnique):
            mask = ma.make_mask(instrumentID==instrument)
            timeMasked = time[mask]
            paramMasked = param[mask]
            depthMasked = depth[mask]

            timeIdx = (np.searchsorted(timeSeq, timeMasked))
            nominaldepthIdx = (np.searchsorted(ndSeq, nominalDepth[i]))
            param_fullMat[nominaldepthIdx, timeIdx] = paramMasked
            depth_fullMat[nominaldepthIdx, timeIdx] = depthMasked

        param_DA = xr.DataArray(param_fullMat, coords=[ndSeq, timeSeq],
                                dims=['NOMINAL_DEPTH', "TIME"],
                                attrs=param_attrs)
        depth_DA = xr.DataArray(depth_fullMat, coords=[ndSeq, timeSeq],
                                dims=['NOMINAL_DEPTH', "TIME"],
                                attrs=nominalDepth_attrs)
        param_DS = xr.Dataset({varname: param_DA, 'DEPTH': depth_DA},
                              attrs=global_attrs)

        return param_DS
    except:
        print("ERROR: bad file name, or bad variable name?")
        return




