# A lot of code from https://physoce.github.io/physoce-py/_modules/physoce/tseries.html
# _filt (here _filt_conv), pl64

# https://pyoceans.github.io/python-oceans/filters.html
# pl33tn

from logging import raiseExceptions
#import matplotlib
#import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

#from numba import jit

####
#@jit(nopython=True, parallel=True)
#@jit(nopython=True)
def _filt_conv(x,wts):
    """
    Private function to filter a time series and pad the ends of the filtered 
    time series with NaN values. For N weights, N/2 values are padded at each 
    end of the time series. The filter weights are normalized so that the sum 
    of weights = 1.

    Inputs:

        x - the time series (may be 2d, will be filtered along columns)
        wts - the filter weights

    Output: the filtered time series
    """

    # convert to 2D array if necessary (general case)
    #ndims = np.ndim(x)
    ndims = x.ndim
    #breakpoint()
    if ndims == 1:
        x = np.expand_dims(x,axis=1)

    # normalize weights
    #wtsn = wts*sum(wts)**-1 # normalize weights so sum = 1
    wtsn = wts*np.power(np.sum(wts),-1) # normalize weights so sum = 1

    # Convolve using 'direct' method. In older versions of scipy, this has to
    # be specified because the default 'auto' method could decide to use the
    # 'fft' method, which does not work for time series with NaNs. In newer
    # versions, there is no method option.
    try:
        xf = signal.convolve(x,wtsn[:,np.newaxis],mode='same',method='direct')
    except:
        xf = signal.convolve(x,wtsn[:,np.newaxis],mode='same')

    # note: np.convolve may be faster
    # http://scipy.github.io/old-wiki/pages/Cookbook/ApplyFIRFilter

    # pad ends of time series
    nwts = len(wts) # number of filter weights
    npad = int(np.ceil(0.5*nwts))
    xf[:npad,:] = np.nan
    xf[-npad:,:] = np.nan

    # return array with same number of dimensions as input
    if ndims == 1:
        xf = xf.flatten()
    return xf

#%%
#@jit(nopython=True)
#@jit(nopython=True, parallel=True)
def _filt_conv_np(x, wts):
    """
    Private function to filter a time series and pad the ends of the filtered 
    time series with NaN values. For N weights, N/2 values are padded at each 
    end of the time series. The filter weights are normalized so that the sum 
    of weights = 1.

    Inputs:

        x - the time series (may be 2d, will be filtered along columns)
        wts - the filter weights

    Output: the filtered time series
    """
    ndims = x.ndim
    if ndims > 2:
        raise Exception("x can only up to 2-dimensional")
    if ndims == 1:
        x = np.expand_dims(x,axis=1)

    # normalize weights
    #wtsn = wts*sum(wts)**-1 # normalize weights so sum = 1
    wtsn = wts*np.power(np.sum(wts),-1) # normalize weights so sum = 1

    xf = np.apply_along_axis(np.convolve, 0, x, wts, mode='same')

    # pad ends of time series
    nwts = len(wts) # number of filter weights
    npad = int(np.ceil(0.5*nwts))
    xf[:npad,:] = np.nan
    xf[-npad:,:] = np.nan

    # return array with same number of dimensions as input
    if ndims == 1:
        xf = xf.flatten()

    return xf


#%%
#@jit(nopython=True, parallel=True)
def _filt_lfilter(x,wts):
    """
    Private function to filter a time series and pad the ends of the filtered 
    time series with NaN values. For N weights, N/2 values are padded at each 
    end of the time series. The filter weights are normalized so that the sum 
    of weights = 1.

    Inputs:

        x - the time series (may be 2d, will be filtered along columns)
        wts - the filter weights

    Output: the filtered time series
    """

    # convert to 2D array if necessary (general case)
    #ndims = np.ndim(x)
    ndims = x.ndim
    #if ndims == 1:
    #    x = np.expand_dims(x,axis=1)

    # normalize weights
    #wtsn = wts*sum(wts)**-1 # normalize weights so sum = 1
    wtsn = wts/np.sum(wts) # normalize weights so sum = 1

    nwts = len(wts) # number of filter weights
    nwts2 = 2*nwts

    jp = np.arange(0,nwts)
    jm = np.flip(jp)
    t = np.pi * (jp + 1)
    cs = np.cos(t/(2*nwts))

    #if ndims == 1:
    #    cs = np.expand_dims(cs,axis=1)

    _x = np.r_[np.multiply(cs[jm], x[jm]), x,
               np.multiply(cs[jp], x[len(x)-jp-1])]

    #xf = signal.lfilter(wtsn[:,np.newaxis], [1.0], _x)
    xf = signal.lfilter(wtsn, [1.0], _x)
    xf = xf[nwts2:len(x)+nwts2]

    # return array with same number of dimensions as input
    #if ndims == 1:
    #    xf = xf.flatten()
    return xf

####

#@jit(nopython=True, parallel=True)
def pl33tn(x, dt=1.0, T=33.0):
    """
    Computes low-passed series from `x` using pl33 filter, with optional
    sample interval `dt` (hours) and filter half-amplitude period T (hours)
    as input for non-hourly series.

    The PL33 filter is described on p. 21, Rosenfeld (1983), WHOI
    Technical Report 85-35.  Filter half amplitude period = 33 hrs.,
    half power period = 38 hrs.  The time series x is folded over
    and cosine tapered at each end to return a filtered time series
    xf of the same length.  Assumes length of x greater than 67.

    Examples
    --------
    >>> from oceans.filters import pl33tn
    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(500)  # Time in hours.
    >>> x = 2.5 * np.sin(2 * np.pi * t / 12.42)
    >>> x += 1.5 * np.sin(2 * np.pi * t / 12.0)
    >>> x += 0.3 * np.random.randn(len(t))
    >>> filtered_33 = pl33tn(x, dt=4.0)   # 33 hr filter
    >>> filtered_33d3 = pl33tn(x, dt=4.0, T=72.0)  # 3 day filter
    >>> fig, ax = plt.subplots()
    >>> l1, = ax.plot(t, x, label='original')
    >>> pad = [np.NaN]*8
    >>> l2, = ax.plot(t, np.r_[pad, filtered_33, pad], label='33 hours')
    >>> pad = [np.NaN]*17
    >>> l3, = ax.plot(t, np.r_[pad, filtered_33d3, pad], label='3 days')
    >>> legend = ax.legend()

    Now
    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(500)  # Time in hours.
    >>> x = 2.5 * np.sin(2 * np.pi * t / 12.42)
    >>> x += 1.5 * np.sin(2 * np.pi * t / 12.0)
    >>> x += 0.3 * np.random.randn(len(t))
    >>> filtered_33 = pl33tn(x, dt=4.0)   # 33 hr filter
    >>> filtered_33d3 = pl33tn(x, dt=4.0, T=72.0)  # 3 day filter
    >>> fig, ax = plt.subplots()
    >>> l1, = ax.plot(t, x, label='original')
    >>> l2, = ax.plot(t, filtered_33, label='33 hours')
    >>> l3, = ax.plot(t, filtered_33d3, label='3 days')
    >>> legend = ax.legend()
    """

    pl33 = np.array(
        [
            -0.00027, -0.00114, -0.00211, -0.00317, -0.00427, -0.00537,
            -0.00641, -0.00735, -0.00811, -0.00864, -0.00887, -0.00872,
            -0.00816, -0.00714, -0.00560, -0.00355, -0.00097, +0.00213,
            +0.00574, +0.00980, +0.01425, +0.01902, +0.02400, +0.02911,
            +0.03423, +0.03923, +0.04399, +0.04842, +0.05237, +0.05576,
            +0.05850, +0.06051, +0.06174, +0.06215, +0.06174, +0.06051,
            +0.05850, +0.05576, +0.05237, +0.04842, +0.04399, +0.03923,
            +0.03423, +0.02911, +0.02400, +0.01902, +0.01425, +0.00980,
            +0.00574, +0.00213, -0.00097, -0.00355, -0.00560, -0.00714,
            -0.00816, -0.00872, -0.00887, -0.00864, -0.00811, -0.00735,
            -0.00641, -0.00537, -0.00427, -0.00317, -0.00211, -0.00114,
            -0.00027
        ]
    )

    padlen = np.int(np.ceil(T/dt - 1))

    _dt = np.linspace(-33, 33, 67)

    dt = float(dt) * (33.0 / T)

    filter_time = np.arange(0.0, 33.0, dt, dtype='d')
    # N = len(filter_time)
    filter_time = np.hstack((-filter_time[-1:0:-1], filter_time))

    pl33 = np.interp(filter_time, _dt, pl33)
    pl33 /= np.sum(pl33)
    
    #breakpoint()
    # filter with numpy.convolve and pad, mode must be 'same'
    xf = _filt_conv_np(x, pl33)

    return xf

####

def pl33tn_tapered(x, dt=1.0, T=33.0, mode="valid"):
    """
    Computes low-passed series from `x` using pl33 filter, with optional
    sample interval `dt` (hours) and filter half-amplitude period T (hours)
    as input for non-hourly series.

    The PL33 filter is described on p. 21, Rosenfeld (1983), WHOI
    Technical Report 85-35.  Filter half amplitude period = 33 hrs.,
    half power period = 38 hrs.  The time series x is folded over
    and cosine tapered at each end to return a filtered time series
    xf of the same length.  Assumes length of x greater than 67.

    Examples
    --------
    >>> from oceans.filters import pl33tn
    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(500)  # Time in hours.
    >>> x = 2.5 * np.sin(2 * np.pi * t / 12.42)
    >>> x += 1.5 * np.sin(2 * np.pi * t / 12.0)
    >>> x += 0.3 * np.random.randn(len(t))
    >>> filtered_33 = pl33tn(x, dt=4.0)   # 33 hr filter
    >>> filtered_33d3 = pl33tn(x, dt=4.0, T=72.0)  # 3 day filter
    >>> fig, ax = plt.subplots()
    >>> l1, = ax.plot(t, x, label='original')
    >>> pad = [np.NaN]*8
    >>> l2, = ax.plot(t, np.r_[pad, filtered_33, pad], label='33 hours')
    >>> pad = [np.NaN]*17
    >>> l3, = ax.plot(t, np.r_[pad, filtered_33d3, pad], label='3 days')
    >>> legend = ax.legend()
    """

    pl33 = np.array([
            -0.00027, -0.00114, -0.00211, -0.00317, -0.00427, -0.00537,
            -0.00641, -0.00735, -0.00811, -0.00864, -0.00887, -0.00872,
            -0.00816, -0.00714, -0.00560, -0.00355, -0.00097, +0.00213,
            +0.00574, +0.00980, +0.01425, +0.01902, +0.02400, +0.02911,
            +0.03423, +0.03923, +0.04399, +0.04842, +0.05237, +0.05576,
            +0.05850, +0.06051, +0.06174, +0.06215, +0.06174, +0.06051,
            +0.05850, +0.05576, +0.05237, +0.04842, +0.04399, +0.03923,
            +0.03423, +0.02911, +0.02400, +0.01902, +0.01425, +0.00980,
            +0.00574, +0.00213, -0.00097, -0.00355, -0.00560, -0.00714,
            -0.00816, -0.00872, -0.00887, -0.00864, -0.00811, -0.00735,
            -0.00641, -0.00537, -0.00427, -0.00317, -0.00211, -0.00114,
            -0.00027
            ])

    cutoff = T/dt
    fq =1.0/cutoff
    nw = np.int(np.round(2.0*T/dt))
    nw2 = 2*nw

    _dt = np.linspace(-33, 33, 67)

    dt = float(dt) * (33.0 / T)
    # make sure 33.0 is included in range
    filter_time = np.arange(0.0, 33.0+dt, dt, dtype="d")
    N = len(filter_time)
    filter_time = np.hstack((-filter_time[-1:0:-1], filter_time))

    pl33 = np.interp(filter_time, _dt, pl33)
    pl33 /= np.sum(pl33)

    N = np.int(len(pl33))
    NF = np.int(np.ceil(N/2))
    N2 = np.int(2*N)

    jp = np.arange(0, N)
    jm = np.flip(jp)
    t = np.pi * jp
    cs = np.cos(t/(2*N))

    _x = np.r_[np.multiply(cs[jm], x[jm]), x,
               np.multiply(cs[jp], x[len(x)-jp-1])]
    
    #breakpoint()
    #xf = np.convolve(_x, pl33, mode='valid')
    #return xf[NF:len(xf)-NF]

    #xf = np.convolve(_x, pl33, mode='same')
    #return xf[N2:len(x)+N2]

    #xf = np.convolve(x, pl33, mode='valid')
    #return xf

    xf = signal.lfilter(pl33, [1.0], _x)
    return xf[nw2:len(x)+nw2]

#%%
def pl64(x,dt=1,T=33):
    """
    Filter a time series x with the PL64 filter. If x is 2D, the time series will be filtered along columns.

    Inputs:
    x - a numpy array to be filtered.
    dt - sample interval (hours), default = 1
    T - half-amplitude period (hours), default = 33

    Output: numpy array of filtered time series, same size as input with ends NaN values at start and end.

    Reference: CODE-2: Moored Array and Large-Scale Data Report, WHOI 85-35
    """

    Tn=float(T)/dt # normalized cutoff period
    fqn=1./Tn # normalized cutoff frequency
    nw = int(np.round(64/dt)) # number of weights on one side

    # create filter weights
    j = np.arange(1,nw)
    tn = np.pi*j
    den = fqn*fqn*tn**3
    wts = (2*np.sin(2*fqn*tn) - np.sin(fqn*tn) - np.sin(3*fqn*tn))/den

    # make symmetric
    wts = np.hstack((wts[::-1], 2*fqn,wts))

    xf = _filt_conv_np(x, wts)
    return xf

##%
def pl66tn(x, dt=1.0, T=33.0):
    """
    Computes low-passed series from `x` using pl33 filter, with optional
    sample interval `dt` (hours) and filter half-amplitude period T (hours)
    as input for non-hourly series.

    NOTE: both pl64 and pl66 have the same 33 hr filter
    half-amplitude period. pl66 includes additional filter weights
    upto and including the fourth zero crossing at 2*T hrs.

    The PL64 filter is described on p. 21, Rosenfeld (1983), WHOI
    Technical Report 85-35. Filter half amplitude period = 33 hrs.,
    half power period = 38 hrs. The time series x is folded over
    and cosine tapered at each end to return a filtered time series
    xf of the same length. Assumes length of x greater than 132.
    """

    cutoff = T/dt
    fq = 1.0/cutoff
    nw = np.int(np.round(2.0*T/dt))

    # generate filter weights
    j = np.linspace(1,nw,nw)
    t = j * np.pi
    den = fq * fq * t**3
    pl66 = np.divide(2.0*np.sin(2.0*fq*t) - np.sin(fq*t) - np.sin(3.0*fq*t), den)
    # make symmetric filter weights and normalize to exactly one
    pl66 = np.r_[pl66[::-1], 2.0*fq, pl66]
    pl66 /= np.sum(pl66)

    xf = _filt_conv_np(x,pl66)
    return xf

####

def pl66tn_tapered(x, dt=1.0, T=33.0):
    """
    Computes low-passed series from `x` using pl33 filter, with optional
    sample interval `dt` (hours) and filter half-amplitude period T (hours)
    as input for non-hourly series.

    NOTE: both pl64 and pl66 have the same 33 hr filter
    half-amplitude period. pl66 includes additional filter weights
    upto and including the fourth zero crossing at 2*T hrs.

    The PL64 filter is described on p. 21, Rosenfeld (1983), WHOI
    Technical Report 85-35. Filter half amplitude period = 33 hrs.,
    half power period = 38 hrs. The time series x is folded over
    and cosine tapered at each end to return a filtered time series
    xf of the same length. Assumes length of x greater than 132.
    """

    cutoff = T/dt
    fq = 1.0/cutoff
    nw = np.int(np.round(2.0*T/dt))
    #disp(['number of weights = ',int2str(nw)]);
    nw2 = 2*nw

    # generate filter weights
    j = np.linspace(1,nw,nw)
    t = np.pi * j
    den = fq * fq * t**3
    wts = np.divide(2.0*np.sin(2.0*fq*t) - np.sin(fq*t) - np.sin(3.0*fq*t), den)
    # make symmetric filter weights and normalize to exactly one
    wts = np.r_[np.flip(wts), 2.0*fq, wts]
    wts /= np.sum(wts)

    N = np.int(len(wts))
    N2 = np.int(2*N)

    jp = np.arange(0, N)
    jm = np.flip(jp)
    t = np.pi * jp
    cs = np.cos(t/(2*N))

    _x = np.r_[np.multiply(cs[jm], x[jm]), x,
               np.multiply(cs[jp], x[len(x)-jp-1])]
    xf = signal.lfilter(wts, [1.0], _x)
    #xf = signal.filtfilt(wts, [1.0], _x, method='gust')
    return xf[nw2+1:len(x)+nw2+1] #check

####

##%
def pl66tn_filtfilt(x, dt=1.0, T=33.0):
    """
    Computes low-passed series from `x` using pl33 filter, with optional
    sample interval `dt` (hours) and filter half-amplitude period T (hours)
    as input for non-hourly series.

    NOTE: both pl64 and pl66 have the same 33 hr filter
    half-amplitude period. pl66 includes additional filter weights
    upto and including the fourth zero crossing at 2*T hrs.

    The PL64 filter is described on p. 21, Rosenfeld (1983), WHOI
    Technical Report 85-35. Filter half amplitude period = 33 hrs.,
    half power period = 38 hrs. The time series x is folded over
    and cosine tapered at each end to return a filtered time series
    xf of the same length. Assumes length of x greater than 132.
    """

    cutoff = T/dt
    fq = 1.0/cutoff
    nw = np.int(np.round(2.0*T/dt))

    # generate filter weights
    j = np.linspace(1,nw,nw)
    t = np.pi * j
    den = fq * fq * t**3
    pl66 = np.divide(2.0*np.sin(2.0*fq*t) - np.sin(fq*t) - np.sin(3.0*fq*t), den)
    # make symmetric filter weights and normalize to exactly one
    pl66 = np.r_[pl66[::-1], 2.0*fq, pl66]
    pl66 /= np.sum(pl66)

    #xf = _filt_conv_np(x,pl66)
    xf = signal.filtfilt(pl66, [1.0], x, method='gust')

    ## need zeros, poles and gain
    #sos = signal.tf2sos(z, p, k)
    #xf = signal.sosfiltfilt(sos, x)

    return xf

#%%
def thompson1983(x, dt=1.0, return_filter_weights=False):
    """
    NOT WORKING YET!

    Computes low-passed series from `x` using Thompson 1983 filter, with optional
    sample interval `dt` (hours) as input for non-hourly series.
    """
    thompson1983 = np.array([
        -0.0001255975169529, -0.0000576566212960,  0.0000008772625492,
        0.0000504990701605,   0.0000942800339363,  0.0001364265309623,
        0.0001806489560515,   0.0002287678672126,  0.0002798969463550,
        0.0003303767333693,   0.0003744359684560,  0.0004053797177045,
        0.0004169878608051,   0.0004047781247945,  0.0003668456031790,
        0.0003041148023638,   0.0002199949519143,  0.0001195739580541,
        0.0000085859812592,  -0.0001075788384422, -0.0002245893905455,
        -0.0003394700761412, -0.0004504529871661, -0.0005564737287697,
        -0.0006564810771678, -0.0007487640159512, -0.0008304804428853,
        -0.0008975096399215, -0.0009446647583862, -0.0009662152532209,
        -0.0009566032233169, -0.0009112054794798, -0.0008269984668252,
        -0.0007030198466382, -0.0005405755511982, -0.0003431986285532,
        -0.0001164119731874,  0.0001326280681766,  0.0003955286488028,
        0.0006630371369789,   0.0009253655622452,  0.0011724606875113,
        0.0013942402966371,   0.0015808268731708,  0.0017228077359594,
        0.0018115390102654,   0.0018394947886009,  0.0018006478593020,
        0.0016908582800693,   0.0015082421867801,  0.0012534944537684,
        0.0009301425178768,   0.0005447120097246,  0.0001067860560333,
        -0.0003710606763679, -0.0008734730218081, -0.0013826893388516,
        -0.0018790889539334, -0.0023419092817862, -0.0027501090943452,
        -0.0030833325127995, -0.0033229093511619, -0.0034528166570604,
        -0.0034605274105611, -0.0033376862901474, -0.0030805767616674,
        -0.0026903730907849, -0.0021731981753985, -0.0015400265393673,
        -0.0008064767996314,  0.0000074716137969,  0.0008778237149054,
        0.0017769884931807,   0.0026743079755453,  0.0035367432067438,
        0.0043297607266505,   0.0050184423729522,  0.0055688071033572,
        0.0059492933454438,   0.0061323134445715,  0.0060957669907227,
        0.0058243933643957,   0.0053108576334068,  0.0045564950198581,
        0.0035716805257987,   0.0023758326599445,  0.0009970943319706,
        -0.0005282469392941, -0.0021565360734941, -0.0038376759144109,
        -0.0055161769150466, -0.0071323330124128, -0.0086235450735164,
        -0.0099258193929847, -0.0109754587308147, -0.0117109387968976,
        -0.0120749292502215, -0.0120163829300949, -0.0114925883575559,
        -0.0104710651532758, -0.0089311834319159, -0.0068654061760652,
        -0.0042800842603486, -0.0011957709551415,  0.0023529406613552,
        0.0063180240999614,   0.0106390172601230,  0.0152443519297012,
        0.0200529580916656,   0.0249760952599217,  0.0299193737696328,
        0.0347849368494655,   0.0394737763693820,  0.0438881502843118,
        0.0479340588587595,   0.0515237222033966,  0.0545779867795019,
        0.0570285766902611,   0.0588200995238596,  0.0599117179373416,
        0.0602784024045874,   0.0599117179373416,  0.0588200995238596,
        0.0570285766902611,   0.0545779867795019,  0.0515237222033966,
        0.0479340588587595,   0.0438881502843118,  0.0394737763693820,
        0.0347849368494655,   0.0299193737696328,  0.0249760952599217,
        0.0200529580916656,   0.0152443519297012,  0.0106390172601230,
        0.0063180240999614,   0.0023529406613552, -0.0011957709551415,
        -0.0042800842603486, -0.0068654061760652, -0.0089311834319159,
        -0.0104710651532758, -0.0114925883575559, -0.0120163829300949,
        -0.0120749292502215, -0.0117109387968976, -0.0109754587308147,
        -0.0099258193929847, -0.0086235450735164, -0.0071323330124128,
        -0.0055161769150466, -0.0038376759144109, -0.0021565360734941,
        -0.0005282469392941,  0.0009970943319706,  0.0023758326599445,
        0.0035716805257987,   0.0045564950198581,  0.0053108576334068,
        0.0058243933643957,   0.0060957669907227,  0.0061323134445715,
        0.0059492933454438,   0.0055688071033572,  0.0050184423729522,
        0.0043297607266505,   0.0035367432067438,  0.0026743079755453,
        0.0017769884931807,   0.0008778237149054,  0.0000074716137969,
        -0.0008064767996314, -0.0015400265393673, -0.0021731981753985,
        -0.0026903730907849, -0.0030805767616674, -0.0033376862901474,
        -0.0034605274105611, -0.0034528166570604, -0.0033229093511619,
        -0.0030833325127995, -0.0027501090943452, -0.0023419092817862,
        -0.0018790889539334, -0.0013826893388516, -0.0008734730218081,
        -0.0003710606763679,  0.0001067860560333,  0.0005447120097246,
        0.0009301425178768,   0.0012534944537684,  0.0015082421867801,
        0.0016908582800693,   0.0018006478593020,  0.0018394947886009,
        0.0018115390102654,   0.0017228077359594,  0.0015808268731708,
        0.0013942402966371,   0.0011724606875113,  0.0009253655622452,
        0.0006630371369789,   0.0003955286488028,  0.0001326280681766,
        -0.0001164119731874, -0.0003431986285532, -0.0005405755511982,
        -0.0007030198466382, -0.0008269984668252, -0.0009112054794798,
        -0.0009566032233169, -0.0009662152532209, -0.0009446647583862,
        -0.0008975096399215, -0.0008304804428853, -0.0007487640159512,
        -0.0006564810771678, -0.0005564737287697, -0.0004504529871661,
        -0.0003394700761412, -0.0002245893905455, -0.0001075788384422,
        0.0000085859812592,   0.0001195739580541,  0.0002199949519143,
        0.0003041148023638,   0.0003668456031790,  0.0004047781247945,
        0.0004169878608051,   0.0004053797177045,  0.0003744359684560,
        0.0003303767333693,   0.0002798969463550,  0.0002287678672126,
        0.0001806489560515,   0.0001364265309623,  0.0000942800339363,
        0.0000504990701605,   0.0000008772625492, -0.0000576566212960,
        -0.0001255975169529
    ])

    T = 120.0
    padlen = np.int(np.ceil(T/dt - 1))

    _dt = np.linspace(-120, 120, 241)

    dt = float(dt) * (120.0 / T)

    filter_time = np.arange(0.0, 120.0, dt, dtype='d')
    # N = len(filter_time)
    filter_time = np.hstack((-filter_time[-1:0:-1], filter_time))

    thompson1983 = np.interp(filter_time, _dt, thompson1983)
    thompson1983 /= np.sum(thompson1983)

    if return_filter_weights:
        return thompson1983
        
    xf = _filt_conv_np(x, thompson1983)
    return xf

####

def thompson1983_lfilter(x, dt=1.0, return_filter_weights=False):
    """
    NOT WORKING YET!
    
    Computes low-passed series from `x` using Thompson 1983 filter, with optional
    sample interval `dt` (hours) as input for non-hourly series.
    """
    thompson1983 = np.array([
        -0.0001255975169529, -0.0000576566212960,  0.0000008772625492,
        0.0000504990701605,   0.0000942800339363,  0.0001364265309623,
        0.0001806489560515,   0.0002287678672126,  0.0002798969463550,
        0.0003303767333693,   0.0003744359684560,  0.0004053797177045,
        0.0004169878608051,   0.0004047781247945,  0.0003668456031790,
        0.0003041148023638,   0.0002199949519143,  0.0001195739580541,
        0.0000085859812592,  -0.0001075788384422, -0.0002245893905455,
        -0.0003394700761412, -0.0004504529871661, -0.0005564737287697,
        -0.0006564810771678, -0.0007487640159512, -0.0008304804428853,
        -0.0008975096399215, -0.0009446647583862, -0.0009662152532209,
        -0.0009566032233169, -0.0009112054794798, -0.0008269984668252,
        -0.0007030198466382, -0.0005405755511982, -0.0003431986285532,
        -0.0001164119731874,  0.0001326280681766,  0.0003955286488028,
        0.0006630371369789,   0.0009253655622452,  0.0011724606875113,
        0.0013942402966371,   0.0015808268731708,  0.0017228077359594,
        0.0018115390102654,   0.0018394947886009,  0.0018006478593020,
        0.0016908582800693,   0.0015082421867801,  0.0012534944537684,
        0.0009301425178768,   0.0005447120097246,  0.0001067860560333,
        -0.0003710606763679, -0.0008734730218081, -0.0013826893388516,
        -0.0018790889539334, -0.0023419092817862, -0.0027501090943452,
        -0.0030833325127995, -0.0033229093511619, -0.0034528166570604,
        -0.0034605274105611, -0.0033376862901474, -0.0030805767616674,
        -0.0026903730907849, -0.0021731981753985, -0.0015400265393673,
        -0.0008064767996314,  0.0000074716137969,  0.0008778237149054,
        0.0017769884931807,   0.0026743079755453,  0.0035367432067438,
        0.0043297607266505,   0.0050184423729522,  0.0055688071033572,
        0.0059492933454438,   0.0061323134445715,  0.0060957669907227,
        0.0058243933643957,   0.0053108576334068,  0.0045564950198581,
        0.0035716805257987,   0.0023758326599445,  0.0009970943319706,
        -0.0005282469392941, -0.0021565360734941, -0.0038376759144109,
        -0.0055161769150466, -0.0071323330124128, -0.0086235450735164,
        -0.0099258193929847, -0.0109754587308147, -0.0117109387968976,
        -0.0120749292502215, -0.0120163829300949, -0.0114925883575559,
        -0.0104710651532758, -0.0089311834319159, -0.0068654061760652,
        -0.0042800842603486, -0.0011957709551415,  0.0023529406613552,
        0.0063180240999614,   0.0106390172601230,  0.0152443519297012,
        0.0200529580916656,   0.0249760952599217,  0.0299193737696328,
        0.0347849368494655,   0.0394737763693820,  0.0438881502843118,
        0.0479340588587595,   0.0515237222033966,  0.0545779867795019,
        0.0570285766902611,   0.0588200995238596,  0.0599117179373416,
        0.0602784024045874,   0.0599117179373416,  0.0588200995238596,
        0.0570285766902611,   0.0545779867795019,  0.0515237222033966,
        0.0479340588587595,   0.0438881502843118,  0.0394737763693820,
        0.0347849368494655,   0.0299193737696328,  0.0249760952599217,
        0.0200529580916656,   0.0152443519297012,  0.0106390172601230,
        0.0063180240999614,   0.0023529406613552, -0.0011957709551415,
        -0.0042800842603486, -0.0068654061760652, -0.0089311834319159,
        -0.0104710651532758, -0.0114925883575559, -0.0120163829300949,
        -0.0120749292502215, -0.0117109387968976, -0.0109754587308147,
        -0.0099258193929847, -0.0086235450735164, -0.0071323330124128,
        -0.0055161769150466, -0.0038376759144109, -0.0021565360734941,
        -0.0005282469392941,  0.0009970943319706,  0.0023758326599445,
        0.0035716805257987,   0.0045564950198581,  0.0053108576334068,
        0.0058243933643957,   0.0060957669907227,  0.0061323134445715,
        0.0059492933454438,   0.0055688071033572,  0.0050184423729522,
        0.0043297607266505,   0.0035367432067438,  0.0026743079755453,
        0.0017769884931807,   0.0008778237149054,  0.0000074716137969,
        -0.0008064767996314, -0.0015400265393673, -0.0021731981753985,
        -0.0026903730907849, -0.0030805767616674, -0.0033376862901474,
        -0.0034605274105611, -0.0034528166570604, -0.0033229093511619,
        -0.0030833325127995, -0.0027501090943452, -0.0023419092817862,
        -0.0018790889539334, -0.0013826893388516, -0.0008734730218081,
        -0.0003710606763679,  0.0001067860560333,  0.0005447120097246,
        0.0009301425178768,   0.0012534944537684,  0.0015082421867801,
        0.0016908582800693,   0.0018006478593020,  0.0018394947886009,
        0.0018115390102654,   0.0017228077359594,  0.0015808268731708,
        0.0013942402966371,   0.0011724606875113,  0.0009253655622452,
        0.0006630371369789,   0.0003955286488028,  0.0001326280681766,
        -0.0001164119731874, -0.0003431986285532, -0.0005405755511982,
        -0.0007030198466382, -0.0008269984668252, -0.0009112054794798,
        -0.0009566032233169, -0.0009662152532209, -0.0009446647583862,
        -0.0008975096399215, -0.0008304804428853, -0.0007487640159512,
        -0.0006564810771678, -0.0005564737287697, -0.0004504529871661,
        -0.0003394700761412, -0.0002245893905455, -0.0001075788384422,
        0.0000085859812592,   0.0001195739580541,  0.0002199949519143,
        0.0003041148023638,   0.0003668456031790,  0.0004047781247945,
        0.0004169878608051,   0.0004053797177045,  0.0003744359684560,
        0.0003303767333693,   0.0002798969463550,  0.0002287678672126,
        0.0001806489560515,   0.0001364265309623,  0.0000942800339363,
        0.0000504990701605,   0.0000008772625492, -0.0000576566212960,
        -0.0001255975169529
    ])

    T = 120.0
    _dt = np.linspace(-120, 120, 241)

    dt = float(dt) * (120.0 / T)
    # make sure 33.0 is included in range
    filter_time = np.arange(0.0, 120.0+dt, dt, dtype="d")
    N = len(filter_time)
    filter_time = np.hstack((-filter_time[-1:0:-1], filter_time))

    thompson1983 = np.interp(filter_time, _dt, thompson1983)
    thompson1983 /= np.sum(thompson1983)

    if return_filter_weights:
        return thompson1983
        
    xf = _filt_lfilter(x, thompson1983)
    return xf

#%%
if __name__ == "__main__":
    #import pl33_pl66_thompson as lpf

	t = np.arange(1000)  # Time in hours.
	x = 2.5 * np.sin(2.0 * np.pi * t / 12.42)
	x += 1.5 * np.sin(2.0 * np.pi * t / 12.0)
	x += 0.3 * np.random.randn(len(t))

	xf33 = pl33tn(x, dt=1.0, T=33.0)   # 33 hr filter
	xf33d3 = pl33tn(x, dt=1.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf33, label='33 hours')
	l3, = ax.plot(t, xf33d3, label='3 days')
	legend = ax.legend()

	xf64 = pl64(x, dt=1.0)   # 33 hr filter
	xf64d3 = pl64(x, dt=1.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf64, label='33 hours')
	l3, = ax.plot(t, xf64, label='3 days')
	legend = ax.legend()

	xf66 = pl66tn(x, dt=1.0)   # 33 hr filter
	xf66d3 = pl66tn(x, dt=1.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf66, label='33 hours')
	l3, = ax.plot(t, xf66d3, label='3 days')
	legend = ax.legend()

	xf33 = pl33tn_tapered(x, dt=4.0)   # 33 hr filter
	xf33d3 = pl33tn_tapered(x, dt=4.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf33, label='33 hours')
	l3, = ax.plot(t, xf33d3, label='3 days')
	legend = ax.legend()

	xf66 = pl66tn_tapered(x, dt=4.0)   # 33 hr filter
	xf66d3 = pl66tn_tapered(x, dt=4.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf66, label='33 hours')
	l3, = ax.plot(t, xf66d3, label='3 days')
	legend = ax.legend()

	xf66 = pl66tn_filtfilt(x, dt=4.0)   # 33 hr filter
	xf66d3 = pl66tn_filtfilt(x, dt=4.0, T=72.0)  # 3 day filter
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf66, label='33 hours')
	l3, = ax.plot(t, xf66d3, label='3 days')
	legend = ax.legend()

	xf1 = pl33tn(x, dt=1.0)
	xf2 = pl66tn(x, dt=1.0)
	xf3 = thompson1983(x, dt=1.0)
	xf4 = thompson1983_lfilter(x, dt=1.0)
	#xf4 = thompson1983_layered(x, dt=1.0)
	fig, ax = plt.subplots()
	l1, = ax.plot(t, x, label='original')
	l2, = ax.plot(t, xf1, label='pl33tn')
	l3, = ax.plot(t, xf2, label='pl66tn')
	l3, = ax.plot(t, xf3, label='thompson')
	l4, = ax.plot(t, xf4, label='thompson_lfilter')
	legend = ax.legend()
# %%
