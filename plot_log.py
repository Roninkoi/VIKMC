#!/bin/env python3
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys
import re

from plot import *

show = True # show plots?
dfpath = "out.log"
tn = 10000 # number of time steps
dt = 1 # read frequency
if len(sys.argv) > 1:
    dfpath = sys.argv[1]
if len(sys.argv) > 2:
    tn = int(sys.argv[2])
if len(sys.argv) > 3:
    dt = int(sys.argv[3])
if len(sys.argv) > 4:
    show = bool(int(sys.argv[4]))

def parselog(path, tn, dt):
    df = open(path, "r")
    start = False
    time = [] # time
    nd = [] # number of defects
    jv = [] # number of vacancy jumps
    ji = [] # number of interstitial jumps

    ti = 0
    i = 0
    for l in df: # parse dump file
        if "t=" in l:
            if i == ti:
                words = re.split(',|\||=|\n', l)
                #print(words)
                
                try:
                    w1 = float(words[1])
                    w3 = int(words[3])
                    w5 = int(words[5])
                    w7 = int(words[7])
                    w9 = int(words[9])
                except Exception as e:
                    print(e)

                time.append(w1)
                nd.append(w3+w5)
                jv.append(w7)
                ji.append(w9)
            
            i += 1
            ti = i * dt

    return np.array(time), np.array(nd), np.array(jv), np.array(ji)

# take mean across 3 runs
def meanj(jvs, i):
    x = np.linspace(np.min(jvs[0+i][:, 0]), np.max(jvs[0+i][:, 0]), 1000)
    j0 = np.array([x, np.interp(x, jvs[0+i][:, 0], jvs[0+i][:, 1])]).T
    j1 = np.array([x, np.interp(x, jvs[1+i][:, 0], jvs[1+i][:, 1])]).T
    j2 = np.array([x, np.interp(x, jvs[2+i][:, 0], jvs[2+i][:, 1])]).T
    return (j0 + j1 + j2) / 3.

if len(sys.argv) > 1:
    times, nd, jv, ji = parselog(dfpath, tn, dt)
    linescatter([np.array([times, nd]).T], titles=["Number of defects", "$t$ (fs)", "$n_v+n_i$"], log=[True, True], fpath="defects.pdf")
    linescatter([np.array([times, jv]).T, np.array([times, ji]).T], titles=["Number of jumps", "$t$ (fs)", "n"], labels=["Vacancy", "Interstitial"], log=[True, True], fpath="jumps.pdf")
else:
    nds=[]
    jvs=[]
    jis=[]
    for f in ["out500_1.log", "out500_2.log", "out500_3.log",
              "out1500_1.log", "out1500_2.log", "out1500_3.log",
              "out2500_1.log", "out2500_2.log", "out2500_3.log"]:
        times, nd, jv, ji = parselog(f, tn, dt)
        nds.append(np.array([times, nd]).T)
        jvs.append(np.array([times, jv]).T)
        jis.append(np.array([times, ji]).T)
    linescatter(nds, titles=["Number of defects", "$t$ (fs)", "$n_v+n_i$"], labels=["500 K", "500 K", "500 K", "1500 K", "1500 K", "1500 K", "2500 K", "2500 K", "2500 K"], log=[True, True], fpath="defects.pdf")

    linescatter([meanj(jvs, 0), meanj(jis, 0)], titles=["Number of jumps at 500 K", "$t$ (fs)", "n"], labels=["Vacancy", "Interstitial"], log=[True, True], fpath="jumps500.pdf")
    linescatter([meanj(jvs, 3), meanj(jis, 3)], titles=["Number of jumps at 1500 K", "$t$ (fs)", "n"], labels=["Vacancy", "Interstitial"], log=[True, True], fpath="jumps1500.pdf")
    linescatter([meanj(jvs, 6), meanj(jis, 6)], titles=["Number of jumps at 2500 K", "$t$ (fs)", "n"], labels=["Vacancy", "Interstitial"], log=[True, True], fpath="jumps2500.pdf")

