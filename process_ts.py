from __future__ import print_function
from multiprocessing import Pool, current_process, cpu_count
import numpy as np
import time

def matmul(a,b):
    return a*b;

def diff_ang(a,b):
    r = a - b;
    if r > np.pi:
        r = r - 2 * np.pi;
    elif r < - np.pi:
        r = 2 * np.pi - r;
    return r;

def wraptopi(a):
    return (a + np.pi) % (2*np.pi) - np.pi;

'''
*********************
*********************
process min NN-dist
*********************
*********************
'''
def start_process(args):
    #set file pointer
    (ft,sRad,cRad,No) = args;
    folder = ''
    #fXname = './may/111_fov_270/res_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '.txt';
    fXname = folder + 'res_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '.txt';
    fWriteX = open(fXname,"w");

    acc = 0;
    for no in range(1,101):
        #fEname = './may/111_fov_270/sim1_time_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '_' + str(no) +'_E.txt';
        fEname = folder + 'sim1_time_' + str(ft) + '_' + str(sRad) + '_' + str(cRad) + '_' + str(no) +'_E.txt';
        fWriteE = open(fEname,"r");
        acc = 0

        for line in fWriteE:
            word = line.split();
            acc += float(word[3]);

        print("%.4f" % (acc / (5000)),file = fWriteX,end="\n");
        fWriteE.close();


    fWriteX.close();


def create_arg():
    finaltime = [0.15,0.2,0.22,0.24,0.25,0.26,0.28,0.3]
    sa_rad = [8,9,10,11,12];
    No = [1]

    a=[]
    b=[]
    c=[]
    d=[]

    for ft in finaltime:
        for sr in sa_rad:
            ca_rad = sr+ np.arange(-2,3,1);
            for cr in ca_rad:
                for no in No:
                    a.append(ft);
                    b.append(sr)
                    c.append(cr)
                    d.append(no)

    return zip(a,b,c,d)

if __name__ == "__main__":

    pool = Pool(processes=8)
    arg = create_arg();
    now = time.time();
    pool.map( start_process, arg )
    print(time.time() - now);
