## create a character block plot
from itertools import groupby
import numpy as np

def blockPlot(x, lineLength = 80):
    '''
    Print a line block-plot of data availability of specified length
    E. Klein. ekleins@gmail.com 2020-10-20
    :param x: numpy array of dim 1
    :param lineLength: lenght of the line plot
    :return: string
    '''
    blockSymbols = ['\u2591', '\u2593']
    ## make boolean vector 1-nodata 0-data
    x_bool = np.isnan(x.values).astype(int).tolist()
    ## run-length encoder
    x_rle = [[key, len(list(group))] for key, group in groupby(x_bool)]
    ## list of number of symbols
    x_sum = sum(x[1] for x in x_rle)
    x_symbols = list(round(lineLength * x[1]/x_sum) for x in x_rle)
    return ''.join(list(blockSymbols[x_rle[i][0]] * x_symbols[i] for i in range(len(x_rle))))

