#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 06:12:21 2018

@author: suppanatr
"""

import numpy as np
import pandas as pd
import time

SR = [8,9,10,11,12]
AR = np.arange(-2,3,1)
N = np.arange(1,101)

#idx = pd.Index(SR);
#data_c = pd.DataFrame(np.zeros((5,5)),index=idx,columns=AR);
now = time.time()
for sr in SR:
    res = np.zeros((1,99))
    for ar in AR:
        for n in N:
            fnameX = 'sim1_time_500_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_X.txt';
            fnameY = 'sim1_time_500_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_Y.txt';
            tmpX = pd.read_csv(fnameX,sep=' ',header=None);
            tmpY = pd.read_csv(fnameY,sep=' ',header=None);

            tmpX = tmpX.iloc[4000:5000,0:50].as_matrix()
            cX = tmpX.mean(axis = 1).reshape(1000,1)
            X = (tmpX.transpose() - cX.transpose())

            tmpY = tmpY.iloc[4000:5000,0:50].as_matrix()
            cY = tmpY.mean(axis = 1).reshape(1000,1)
            Y = (tmpY.transpose() - cY.transpose())

            D = np.sqrt(np.power(X,2) + np.power(Y,2))

            hist_tmp, be = np.histogram(D,np.arange(0,100))
            res += hist_tmp.reshape(1,99)
    fname = '111_hist' + str(sr) + '.txt';
    np.savetxt(fname, res, delimiter=',')
print(time.time() - now)
