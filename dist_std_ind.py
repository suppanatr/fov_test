#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 06:12:21 2018

@author: suppanatr
"""

import numpy as np
import pandas as pd
from multiprocessing import Pool
import time


#idx = pd.Index(SR);
#data_c = pd.DataFrame(np.zeros((5,5)),index=idx,columns=AR);
def process(arg):
    (sr,ar,sarg) = arg
    folder = '/Volumes/HDD_6TB/as_both_c/'
    fnameM = folder + 'Dist_std_' + str(sarg) + '_' + str(sr) + '_' + str(sr + ar) + '.txt'
    fws = open(fnameM,"w")
    for n in range(1,501):
        fnameX = folder + 'sim1_time_' + str(sarg) + '_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_X.txt';
        fnameY = folder + 'sim1_time_' + str(sarg) + '_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_Y.txt';
        tmpX = pd.read_csv(fnameX,sep=' ',header=None);
        tmpY = pd.read_csv(fnameY,sep=' ',header=None);

        tmpX = tmpX.iloc[4000:5000,0:50].as_matrix()
        cX = tmpX.mean(axis = 1).reshape(1000,1)
        X = (tmpX.transpose() - cX.transpose())

        tmpY = tmpY.iloc[4000:5000,0:50].as_matrix()
        cY = tmpY.mean(axis = 1).reshape(1000,1)
        Y = (tmpY.transpose() - cY.transpose())

        D = np.sqrt(np.power(X,2) + np.power(Y,2))

        std_D = D.std(axis = 0)
        for i in range(5000):
            print("%d " %(std_D[i]), file=fws, end=" " )
        print("%d" %(n), file=fws, end="\n" )
    fws.close()

def generate_arg(SR,AR,ARG):
    a = []
    b = []
    c = []
    for sr in SR:
        for ar in AR:
            for arg in ARG:
                a.append(sr)
                b.append(ar)
                c.append(arg)
    return zip(a,b,c,d)

if __name__ == "__main__":
    SR = [8,9,10,11,12]
    AR = np.arange(-2,3,1)
    ARG = [500]
    #No = range(1,501)
    arg = generate_arg(SR,AR,ARG)

    pool = Pool(processes=4)
    now = time.time()
    pool.map(grouping_prepare,arg)
    print(time.time() - now)
