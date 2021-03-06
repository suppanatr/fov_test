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

def grouping(X,Y):
    to_process_list = list(range(0,51))
    to_process_queue = []
    label = 0
    group_size = []
    #group = [0] * 50
    tmp = to_process_list.pop(50)
    to_process_queue.append(tmp)
    count = 0
    while len(to_process_queue) > 0:
        tmp = to_process_queue.pop(0)
        #group[tmp] = label
        count += 1
        diff_x = X - X[tmp]
        diff_y = Y - Y[tmp]
        for other in to_process_list:
            xc = diff_x[other]
            yc = diff_y[other]
            if (xc*xc + yc*yc) < 900:
                to_process_queue.append(other)
                to_process_list.remove(other)
    group_size.append(count)
    label += 1
    while len(to_process_list) > 0:
        tmp = to_process_list.pop(0)
        to_process_queue.append(tmp)
        count = 0
        while len(to_process_queue) > 0:
            tmp = to_process_queue.pop(0)
            #group[tmp] = label
            count += 1
            diff_x = X - X[tmp]
            diff_y = Y - Y[tmp]
            for other in to_process_list:
                xc = diff_x[other]
                yc = diff_y[other]
                if (xc*xc + yc*yc) < 900:
                    to_process_queue.append(other)
                    to_process_list.remove(other)
        group_size.append(count)
        label += 1
    c_max = group_size[0]
    r_max = np.max(group_size)
    return (c_max,r_max)

def grouping_prepare(arg):
    (sr,ar) = arg
    folder = ''
    fnameW = folder + 'Fragment_' + str(sr) + '_' + str(sr + ar) + '.txt'
    fw = open(fnameW,"w")
    for n in range(1,501):
        fnameX = folder + 'sim1_time_500_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_X.txt';
        fnameY = folder + 'sim1_time_500_' + str(sr) + '_' + str(ar + sr) + '_' + str(n) + '_Y.txt';
        tmpX = pd.read_csv(fnameX,sep=' ',header=None);
        tmpY = pd.read_csv(fnameY,sep=' ',header=None);

        X = tmpX.iloc[4000,0:51].as_matrix()
        Y = tmpY.iloc[4000,0:51].as_matrix()
        (A,B) = grouping(X,Y)
        X = tmpX.iloc[4500,0:51].as_matrix()
        Y = tmpY.iloc[4500,0:51].as_matrix()
        (C,D) = grouping(X,Y)
        X = tmpX.iloc[4999,0:51].as_matrix()
        Y = tmpY.iloc[4999,0:51].as_matrix()
        (E,F) = grouping(X,Y)
        print("%d %d %d %d %d %d" %(A,B,C,D,E,F), file=fw, end="\n" )
    fw.close()

def generate_arg(SR,AR):
    a = []
    b = []
    for sr in SR:
        for ar in AR:
            a.append(sr)
            b.append(ar)
    return zip(a,b)

if __name__ == "__main__":
    SR = [8,9,10,11,12]
    AR = np.arange(-2,3,1)
    arg = generate_arg(SR,AR)

    pool = Pool(processes=1)
    now = time.time()
    pool.map(grouping_prepare,arg)
    print(time.time() - now)
