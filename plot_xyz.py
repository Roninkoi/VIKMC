#!/bin/env python3
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys

from plot import *

show = True # show plots?
dfpath = "vi.xyz"
tn = 10000 # number of time steps
dt = 1 # read frequency
if len(sys.argv) > 1:
    dfpath = sys.argv[1]
if len(sys.argv) > 2:
    tn = int(sys.argv[2])
if len(sys.argv) > 3:
    dt = int(sys.argv[3])
if len(sys.argv) > 2:
    show = bool(int(sys.argv[4]))

def parsexyz(path, tn, dt):
    df = open(path, "r")
    start = False
    atoms = 0 # number of atoms
    
    time = [] # time
    pos = [] # xyz position

    i = 0
    j = 0
    tj = 0
    t = 0
    posj = []
    for l in df: # parse dump file
        if "Time=" in l:
            if start:
                j += 1
                tj = j * dt
                time.append(t)
                pos.append(np.array(posj))
                posj = []
                start = False
                continue
                
            if i == tj:
                ts = l.split(",")[0].split("=")[1]
                t = float(ts)
                start = True
                i += 1
                continue
            i += 1
        
        if len(l.split()) == 1:
            atoms = int(l)
        elif start: # append data to array
            words = l.split()
            try:
                w0 = int(words[0])
                w1 = float(words[1])
                w2 = float(words[2])
                w3 = float(words[3])
                w4 = float(words[4])
            except Exception as e:
                print(e)
                
            posj.append([w2, w3, w4])

    return np.array(time), pos

times, r = parsexyz(dfpath, tn, dt)

msd = []
for i in range(len(times)):
    ri = r[i]
    msd.append(np.mean(np.square(ri[:, 0])+np.square(ri[:, 1])+np.square(ri[:, 2])))

msd = np.array(msd)
linescatter([np.array([times, msd]).T], titles=["Mean squared displacement", "$t$ (fs)", "MSD (Å$^2$)"], fpath="msd.pdf")

