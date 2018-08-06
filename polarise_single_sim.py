#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 06:12:21 2018

cluster by neighbour

@author: suppanatr
"""

import numpy as np
import pandas as pd
from multiprocessing import Pool
import time

def grouping_prepare(arg):
    (sr,ar,sarg) = arg
    folder = '/Volumes/HDD_6TB/as_both_c/'
    fnameM = folder + 'Polarise_mean_' + str(sarg) + '_' + str(sr) + '_' + str(sr + ar) + '.txt'
    fnameS = folder + 'Polarise_sdiv_' + str(sarg) + '_' + str(sr) + '_' + str(sr + ar) + '.txt'
    fwm = open(fnameM,"w")
    fws = open(fnameS,"w")
    for n in range(1,501):
        fnameX = folder + 'sim1_time_' + str(sarg) + '_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_X.txt';
        fnameY = folder + 'sim1_time_' + str(sarg) + '_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_Y.txt';
        tmpX = pd.read_csv(fnameX,sep=' ',header=None);
        tmpY = pd.read_csv(fnameY,sep=' ',header=None);

        Xb = tmpX.iloc[0:4999,0:51].as_matrix()
        Xa = tmpX.iloc[1:5000,0:51].as_matrix()
        Xd = Xa - Xb;
        Yb = tmpY.iloc[0:4999,0:51].as_matrix()
        Ya = tmpY.iloc[1:5000,0:51].as_matrix()
        Yd = Ya - Yb;

        dir = np.atan2(Yd,Xd);
        mean_dir = dir.mean(axis=0);
        std_dir = dir.std(axis=0);

        for i in range(5000):
            print("%d " %(mean_dir[i]), file=fwm, end=" " )
            print("%d " %(std_dir[i]), file=fws, end=" " )
        print("%d" %(n), file=fwm, end="\n" )
        print("%d" %(n), file=fws, end="\n" )

    fwm.close()
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
