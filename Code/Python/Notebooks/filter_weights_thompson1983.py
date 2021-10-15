#%%
if False:
    import importlib, sys

    sys.path.append(r'C:\Projects\aims-gitlab\aims-python')
    import filter_weights_thompson1983 as fw
    
    importlib.reload(fw)
    # trying to recreate 120i913 filter, which is of length 120 h for Sydney as per paper
    filtb = fw.filter_weights_thompson1983(1.0, latitude=-33.86, show_info=True)

import numpy as np

# function filtb = filter_thompson1983( dt, varargin )
def filter_weights_thompson1983( dt, **kwargs ):
    # filter_thompson1983 : normalized LOW PASS FILTER weights FOLLOWING THE METHOD OF THOMPSON (1983)
    #
    # RECREATE A LOW PASS FILTER weights FOLLOWING THE METHOD OF
    # THOMPSON (1983); FILTER HAS ZEROES AT SPECIFIED TIDAL AND
    # optional INERTIAL FREQUENCy AND APPROXIMATES AN IDEAL FILTER WITH A
    # COSINE TAPER. Based on FILDSN.FOR by Church, Burrage. 
    # REF:  Thompson, Rory O. R. Y., 1983: Low-Pass Filters to Suppress 
    # Inertial and Tidal Frequencies. J. Phys. Oceanogr., 13, 1077–1083.
    # doi: http://dx.doi.org/10.1175/1520-0485(1983)013<1077:LPFTSI>2.0.CO;2 
    #
    # The default settings will produce normalized filter weights for '120i913' 
    # with zeroes at L1, Q1, O1, K1, N2, M2 and S2 (constraint eq 13) and 
    # constraint eq 21, with upper pass band at 8.6 deg/h and lower pass band
    # at 12.9 deg/h.
    #
    # INPUTS:
    # dt : delta time of data, hours
    # **kwargs
    # latitude : decimal degree (-ve S) latitude, if present also try to filter
    #   inertial frequency
    # T1 : upper end of pass band (hours), default=41.379 h (8.7 deg/h)
    # T2 : lower end of stop band (hours), default=27.907 h (12.9 deg/h)
    # filter_length : filter length in hours, default=120 h
    # show_info : 0/1, show some info, default=0
    # use_eq10 : True/False, additionally use constraint eq 10, default=False, 
    #
    # OUTPUTS
    # weights : normalized weights, can apply too signal using
    # filter(filtb, 1, rawsignal). NOTE using these weights introduces a phase
    # shift so you will have to throw away the first 120h worth of points.
    #
    # TODO
    # - check if wgt should always be normalized?
    #
    # passband : 0 -- OM1
    # transition region : OM1 -- OM2
    # stop band : OM2 -- nyquist frequency
    #
    # filtb = filter_weights_thompson1983(1.0, latitude=-33.558, show_info=True)
    #
    # Wnames : default list of constituent names to optimize, default list
    #   Q1 : Larger lunar elliptic diurnal Q1
    #   O1 : Lunar diurnal O1
    #   K1 : Lunar diurnal K1
    #   N2 : Larger lunar elliptic semidiurnal N2
    #   M2 : Principal lunar semidiurnal M2
    #   L2 : Smaller lunar elliptic semidiurnal L2
    #   S2 : Principal solar semidiurnal S2
    # latitude : 
    # OM1 : upper end of pass band, 8.7 degrees/hour
    # OM2 : lower end of stop band, 12.9 degree/hour
    # filter_length : filter length in hours, 120.0
    # show_info : some info, False
    # use_eq10 : by default will use constraint eq 21 in paper, if you want to use eq 10 as well, False

    defaultKwargs = { 'Wnames': ['Q1', 'O1', 'K1', 'N2', 'M2', 'L2', 'S2'], # default list of constituents
        'latitude': np.NaN,
        'T1': 41.379, # upper end of pass band, 41.379 hours (8.7 degrees/hour)
        'T2': 27.907, # lower end of stop band, 27.907 hours (12.9 degree/hour)
        'filter_length': 120, # filter length in hours
        'show_info': False,
        'use_eq10': False
    }
    # kwargs = merge_two_dicts(defaultKwargs, kwargs) # python 2
    kwargs = { **defaultKwargs, **kwargs } # Python 3.5
    # kwargs = defaultKwargs | kwargs  # Python 3.9+ ONLY

    Wnames = kwargs.pop('Wnames')
    latitude = kwargs.pop('latitude')
    T1 = kwargs.pop('T1')
    T2 = kwargs.pop('T2')
    filter_length = kwargs.pop('filter_length')
    show_info = kwargs.pop('show_info')
    use_eq10 = kwargs.pop('use_eq10')

    has_latitude = np.isfinite(latitude)
    if has_latitude and (np.abs(latitude) > 90.0):
        raise Exception('Latitude out of bounds.')

    OM1 = 360.0/T1 # default 8.7 degrees/hour
    OM2 = 360.0/T2 # default 12.9 degree/hour

    if show_info:
        import matplotlib.pyplot as plt

    nLength = np.int(np.round(filter_length/dt) + 1)

    tidal = constructCons()
    Wnames = np.array(Wnames)
    Wknown = np.array(list(tidal.keys()))
    if np.any(np.isin(Wnames, Wknown, invert=True)):
        print('Wname  : ' + str(Wnames))
        print('Wknown : ' + str(Wknown))
        raise Exception('Uknown constituent in Wnames.')

    W = np.array([tidal[w]['speed'] for w in Wnames])
    if has_latitude:
        W = np.append(W, 2.0*np.sin(np.abs(latitude)*np.pi/180.0)*360.0/24.0)
        Wnames = np.append(Wnames, 'local intertial')

    # not sure if sorting in order is important
    ind = np.argsort(W)
    W = W[ind]
    Wnames = Wnames[ind]

    nConstituents = len(W)

    # The paper uses constraint eq 21. But the code FILDSN.FOR was using eq 10.
    # Don't know why, if you wanted normalized weights w
    if use_eq10:
        print('Eq10 constraint works for dt=1 hour, but not for other dt values. Currently Eq10 causes incorrect frequency reponse curve')
        nConstraints = nConstituents + 2 #number of contraints (eq 13 & 21 & 10)
        ieq13 = 2 #index into constraint matrix where set of eq13 start
    else:
        nConstraints = nConstituents + 1 #number of contraints (eq 13 & eq 21)
        ieq13 = 1

    #%C  SET UP ARRAY D INVERSE (used in eq 20)
    Dinv = 0.5 * np.eye(nLength)
    Dinv[0,0] = 1.0

    # check what am I supposed to print
    if np.min(W) < OM2:
        print('OM1 = ' + str(OM1) + ' deg/h')
        print('OM2 (' + str(OM2)  + 'deg/h) is greater than minimum W (' + str(np.min(W)) + ' deg/h)')

    #C  SET UP THE MATRIX A AND ITS TRANSPOSE
    A  = np.zeros((nConstraints,nLength))
    # eq 21
    A[0,:] = np.square(np.arange(1,nLength+1))
    # eq 10
    if use_eq10:
        A[1, 0] = 1.0
        A[1, 1:] = 2.0

    # eq 13
    A[ieq13:, 0] = 1.0
    avec = W*dt*np.pi/180
    for ii in np.arange(1,nLength,dtype=np.int32):
        #%for jj=ieq10:MMP1
        #%    A(jj,ii)=2.0*cosd((ii-1)*W(jj-1)*dt);
        #%end
        A[ieq13::, ii] = 2.0 * np.cos(ii*avec)

    AT = np.transpose(A)

    #C  SET UP THE VECTOR B
    B = np.zeros(nConstraints) # eq 13
    B[0] = 0.0 # eq 21
    if use_eq10:
        B[1] = 1.0 # eq 10

    #C  SET UP THE VECTOR S
    SS = np.zeros(nLength)
    OM2M1 = OM2 - OM1
    ROMSQ = 180.0 * 180.0/(OM2M1*OM2M1)
    SS[0] = OM1/180.0 + OM2M1/360.0

    #% for ii=2:nLength
    #%     jj=ii-1;
    #%     SINE=sind(OM1*jj*dt) + sind(OM2*jj*dt);
    #%     %C CHECK FOR ZERO DIVIDE FOR CERTAIN COMBINATIONS OF PARAMETERS
    #%     %C       E.G. J=30, OM2M1 =6.0 WAS FOUND, THERE MAY BE OTHERS! WHY?
    #%     JSQ=jj*jj*dt*dt;
    #%     if (JSQ == ROMSQ)
    #%         disp(['THIS OM2-OM1 VALUE CAUSES ZERO DIV AT EL' num2str(J) '  WHILE FORMING S: ' num2str(OMSM1)]);
    #%         error('INVALID COMBINATION OF PARAMETERS (OM2-OM1) IN FILDSN');
    #%     end
    #%     S(ii)=SINE/(jj*dt) - (jj*dt)*SINE/(JSQ-ROMSQ);
    #%     S(ii)=S(ii)/pi;
    #% end

    avec = dt*np.arange(1,nLength)
    SINE = np.sin(np.pi/180.0*OM1*avec) + np.sin(np.pi/180.0*OM2*avec)
    JSQ = np.square(avec)
    SS[1::] = (SINE/avec - (avec*SINE)/(JSQ-ROMSQ)) / np.pi

    #C  GET SD=DI*S AND STORE IN SD(NN)
    #C  GET A*DS AND STORE IN BD(MMP1)
    #C  GET B-BD=B-A*DI*S AND STORE IN B
    #C  GET DI*AT AND STORE IN TEMP1(NN,MMP1)
    #C  GET A*TEMP1=A*A*DI*AT AND STORE IN TEMP2(MMP1,MMP1)
    #C  GET INVERSE OF A*DI*AT AND STORE IN TEMP2(MMP1,MMP1)
    #C  GET DIAT*INVERSE(A*DI*AT) AND STORE IN TEMP3(NN,MMP1)
    #C  GET DIAT(INV(ADIAT))*(B-ADIS) AND STORE IN WGT(NN)

    wgt = np.zeros(nLength)
    ADinv = np.matmul(A, Dinv)
    #breakpoint()
    wgt = np.matmul(Dinv, SS) + np.matmul(np.matmul(Dinv,AT), np.linalg.solve(np.matmul(ADinv, AT), B-np.matmul(ADinv,SS)))

    # Can't see why you wouldn't normalize the weights?
    # sum weights and weights^2 ~=1.0 and 0.0 respectively
    wgt = wgt / ( wgt[0] + 2.0*np.sum(wgt[1:]) )

    if show_info:
        normw = wgt[0] + 2.0*np.sum(wgt[1::])
        #C  NOW CHECK THE FILTER CHARACTERISTICS
        print('Sum of weights is %15.10f' % (normw))
        print('Sum of k^2 weights is %15.10f' % (np.sum(np.square(np.arange(1,len(wgt)+1))*wgt)))
        
        #C  GET FILTER RESPONSE
        #C  FIRST CHECK THE requested FREQUENCIES
        RT = np.full(nConstituents, np.NaN)
        avec = np.pi/180.0 * np.arange(1,len(wgt))
        for ii in np.arange(nConstituents):
            RT[ii] = wgt[0] + 2.0*np.sum( wgt[1::] * np.cos(avec*W[ii]) )
        
        print('  OM1 tidal speed = %9.7f deg/h' % OM1)
        print('  OM2 tidal speed = %9.7f deg/h' % OM2)
        print('FILTER RESPONSE AT')
        for ii, wc in zip(np.arange(len(Wnames)), Wnames):
            if wc == 'local intertial':
                print('  %s : tidal speed = %9.7f deg/h, RT = %9.6g' % (wc, W[ii], RT[ii]))    
            else:
                print('  %s : tidal speed = %9.7f deg/h, RT = %9.6g' % (wc, tidal[wc]['speed'], RT[ii]))

        #C  NOW GET THE THE RESPONSE AT FREQUENCIES BETWEEN 1CYCLE/15DAYS TO THE NYQUIST
        #C  FIRST GET THE FREQUENCIES; FREQUENCY STEP IS deltaf DEGREE/HOUR
        deltaf = 0.01
        NFF = np.int(np.fix(180.0 / deltaf))
        F = deltaf*np.arange(1,NFF+1)

        RS = np.zeros(NFF)
        avec = np.pi/180.0*np.arange(1,len(wgt-1))
        for ii in np.arange(len(F)):
            RS[ii] = (wgt[0] + 2.0*np.sum( wgt[1::] * np.cos(avec*F[ii]) )) / normw

        xx = np.array([0, OM1, OM2, 360.0/(1/dt/2)])
        yy = np.array([1, 1, 0, 0])

        # what is the patch supposed to highlight?
        # figure;
        # pH = patch([0 dt/180],[0 0],[1 0 0],'edgecolor','r','linewidth',1);
        # alpha(pH,0.5);
        # hold('on');
        fh, ax = plt.subplots(2,1)
        ax[0].plot([0, dt/180], [0, 1.0], 'r-', linewidth=1)
        ax[0].plot([dt/180, dt/180], [0.0, 1.0], 'r-', linewidth=1)
        ax[0].plot(xx, yy, 'g-', linewidth=1)
        ax[0].plot(F/dt, RS)
        ax[0].plot(W, np.zeros(np.shape(W)), 'kx')
        for xs,ys,ws in zip(W,np.zeros(np.shape(W))+0.01, Wnames):
            ax[0].text(xs, ys+0.1*ys, ws, rotation=90)
        ax[0].set_xlabel('degrees/hour')
        ax[0].set_ylabel(r'$R(\omega)$')
        ax[0].set_xlim([0, 48])
        ax[0].set_title(r'Filter Response Factor $R(\omega$)')

        ax[1].plot(xx, yy, 'g-', linewidth=1)
        ax[1].plot(F/dt, np.square(RS))
        ax[1].plot(W, np.zeros(np.shape(W)),'kx')
        for xs,ys,ws in zip(W,np.zeros(np.shape(W))+0.01, Wnames):
            ax[1].text(xs, ys+0.1*ys,ws, rotation=90)        
        ax[1].set_xlabel('degrees/hour')
        ax[1].set_ylabel(r'$R(\omega)^2$')
        ax[1].set_xlim([0, 48])
        ax[1].set_title(r'Relative Power Transmitted $R(\omega)^2$')
        
        plt.show(block=False)

        #C  NOW GET THE DEPARTURE OF THE RESPONSE FRON THE IDEAL FOR THE
        #C  LOW AND HIGH FREQUENCY BAND
        ind1 = F < OM1
        i1 = np.argwhere(ind1)[-1]
        theSum1 = np.sqrt( np.sum(np.square(RS[ind1] - 1.0)) / np.sum(ind1) )

        ind2 = F > OM2
        i2 = np.argwhere(ind2)[0]
        theSum2 = np.sqrt( np.sum(np.square(RS[ind2])) / np.sum(ind2) )

        print('OM1 tidal speed = %9.7f deg/h' % OM1)
        print('OM2 tidal speed = %9.7f deg/h' % OM2)
        print('RMS DEPARTURE OF FILTER \n  FROM 1.0 FOR FREQUENCIES BELOW %6.2f DEGREES/HOUR IS %9.6g' % (F[i1], theSum1))
        print('RMS DEPARTURE OF FILTER \n  FROM 0.0 FOR FREQUENCIES FROM %6.2f DEGREES/HOUR TO 180 DEGREES/HOUR IS %9.6g' % (F[i2], theSum2))

    #% construct symetric weight set
    filtb = np.hstack([wgt[::-1], wgt[1::]])
    filtb = filtb / np.sum(filtb)
    return filtb

#%%
#function tidal = constructCons()
def constructCons():
    # load up a simple constituent speed list
    #% from https://www.mathworks.com/matlabcentral/fileexchange/19099-tidal-fitting-toolbox
    ## TODO
    # - maybe try using utide.py constituents

    T  = 15.0
    s  = 0.54901653
    h  = 0.04106864
    p  = 0.00464183
    p1 = 0.00000196

    # good high precision table:
    # http://www.mhl.nsw.gov.au/www/tide_glossary.htmlx
    # [sbs 2020] which now redirects to
    #   http://www.mhl.nsw.gov.au/data/realtime/oceantide/Glossary
    #   but https://en.wikipedia.org/wiki/Theory_of_tides has info
    #
    # key west:
    # http://tidesandcurrents.noaa.gov/cgi-bin/co-ops_qry.cgi?stn=8724580 Key West, FL&dcp=1&ssid=WL&pc=P2&datum=NULL&unit=0&bdate=20080306&edate=20080307&date=1&shift=0&level=-4&form=0&data_type=har&format=View+Data

    #%initialize struct to avoid dynamic re-allocation.
    #tidal=struct('name','.','speed',num2cell(nan(38,1)),'period',nan,'amp',nan,'phase',nan);
    # speed : deg/hour
    tidal = {
        'M2':   {'name': 'M2',  'speed': 2*T - 2*s + 2*h },
        'S2':   {'name': 'S2', 	'speed': 2*T },
        'N2':   {'name': 'N2', 	'speed': 2*T - 3*s + 2*h + p },
        'K1':   {'name': 'K1', 	'speed': 15.0410686 },
        'M4':   {'name': 'M4', 	'speed': 4*(T - s + h) },
        'O1':   {'name': 'O1', 	'speed': T - 2*s + h },
        'M6':   {'name': 'M6', 	'speed': 6*(T - s + h) },
        'MK3':  {'name': 'MK3', 'speed': 44.0251729 },
        'S4':   {'name': 'S4',  'speed': 4*T },
        'MN4':  {'name': 'MN4', 'speed': 57.4238337 },
        'NU2':  {'name': 'NU2', 'speed': 28.5125831 },
        'S6':   {'name': 'S6', 	'speed': 6*T },
        'MU2':  {'name': 'MU2', 'speed': 27.9682084 },
        '2N2':  {'name': '2N2', 'speed': 2*T - 4*s + 2*h + 2*p },
        'OO1':  {'name': 'OO1', 'speed': T + 2*s + h },
        'LAM2': {'name': 'LAM2','speed': 29.4556253 },
        'S1':   {'name': 'S1',  'speed': T },
        'M1':   {'name': 'M1', 	'speed': T - s + h + p },
        'J1':   {'name': 'J1', 	'speed': 15.5854433 },
        'MM':   {'name': 'MM', 	'speed': s-p },
        'SSA':  {'name': 'SSA', 'speed': 2*h },
        'SA':   {'name': 'SA', 	'speed': h },
        'MSF':  {'name': 'MSF', 'speed': 2*s-2*h },
        'MF':   {'name': 'MF',  'speed': 2*s },
        'RHO':  {'name': 'RHO', 'speed': T - 3*s + 3*h - p },
        'Q1':   {'name': 'Q1', 	'speed': T - 3*s + h + p },
        'T2':   {'name': 'T2', 	'speed': 2*T - h + p1 },
        'R2':   {'name': 'R2', 	'speed': 2*T + h - p1 },
        '2Q1':  {'name': '2Q1', 'speed': T - 4*s + h + 2*p },
        'P1':   {'name': 'P1', 	'speed': T - h },
        '2SM2': {'name': '2SM2','speed': 31.0158958 },
        'M3':   {'name': 'M3', 	'speed': 3*T - 3*s + 3*h },
        'L2':   {'name': 'L2', 	'speed': 29.5284789 },
        '2MK3': {'name': '2MK3','speed': 42.9271398 },
        'K2':   {'name': 'K2', 	'speed': 30.0821373 },
        'M8':   {'name': 'M8', 	'speed': 8*(T - s + h) },
        'MS4':  {'name': 'MS4', 'speed': 58.9841042},
        'N':    {'name': 'N',  	'speed': 0.00220641 } # sbs: what is N?
    }

    return tidal
