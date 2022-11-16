#!/bin/env python3
# Roni Koitermaa 2022
# Plotting code using Matplotlib
# Line/scatter plots, subplots, histogram plot, bar plot

import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# line + scatter plot of multiple data sets a
# with different labels and styles
def linescatter(a, titles=["", "", ""], labels=[], styles=[], fpath="", show=True, log=[False, False]):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    #colors = plt.cm.hsv(np.linspace(0.66, 0.0, len(a)))
    if len(a) > 5:
        colors = plt.cm.plasma(np.linspace(0, 0.95, len(a)))
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    f = plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))
    if log[0]:
        ax.set_xscale('log')
    if log[1]:
        ax.set_yscale('log')

    i = 0
    for ai in a:
        alabel = str(i)
        amarker = ""
        alinestyle = "-"
        amarkersize = 1.0
        
        if len(labels) > 0:
            alabel = labels[i]
            
        if len(styles) > 0:
            if styles[i] == 1:
                amarker = "o"
                alinestyle = ""
                amarkersize = 3.0
                
        plt.plot(ai[:, 0], ai[:, 1], label=alabel, marker=amarker, markersize=amarkersize, linestyle=alinestyle)
        i += 1
        
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    
    plt.grid(True)

    if len(labels) > 0 or (len(a) > 1 and len(a) <= 10):
        plt.legend(fontsize='xx-small')

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight') # save to file

    if show:
        plt.show()
        plt.close()
    
# line plot with two subplots
def linesub2(a, titles=["", "", ""], labels=["", ""], fpath="", show=True):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 10))

    ax1.plot(a[0][:, 0], a[0][:, 1], label=labels[0])
    ax2.plot(a[1][:, 0], a[1][:, 1], color="tab:orange", label=labels[1])
    
    ax1.set_title(titles[0])
    plt.xlabel(titles[1])
    ax1.set_ylabel(titles[2])
    if len(titles) > 3:
        ax2.set_ylabel(titles[3])
    else:
        ax2.set_ylabel(titles[2])
        
    ax1.grid(True)
    ax2.grid(True)
    if len(labels[0]) > 0:
        ax1.legend(fontsize='xx-small')
    if len(labels[1]) > 0:
        ax2.legend(fontsize='xx-small')

    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))
    ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight')

    if show:
        plt.show()
        plt.close()

# line plot with three subplots
def linesub3(a, titles=["", "", ""], labels=["", "", ""], fpath="", show=True):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 10))
    
    ax1.plot(a[0][:, 0], a[0][:, 1], label=labels[0])
    ax2.plot(a[1][:, 0], a[1][:, 1], color="tab:orange", label=labels[1])
    ax3.plot(a[2][:, 0], a[2][:, 1], color="tab:green", label=labels[2])
    
    ax1.set_title(titles[0])
    plt.xlabel(titles[1])
    ax1.set_ylabel(titles[2])
    if len(titles) > 4:
        ax2.set_ylabel(titles[3])
        ax3.set_ylabel(titles[4])
    else:
        ax2.set_ylabel(titles[2])
        ax3.set_ylabel(titles[2])
        
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    if len(labels[0]) > 0:
        ax1.legend(fontsize='xx-small')
    if len(labels[1]) > 0:
        ax2.legend(fontsize='xx-small')
    if len(labels[2]) > 0:
        ax3.legend(fontsize='xx-small')
    
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))
    ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))
    ax3.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight')

    if show:
        plt.show()
        plt.close()

# scatter plot of multiple data sets a with errorbars
# with different labels and styles
def scatterr(a, errs, titles=["", "", ""], labels=[], styles=[], fpath="", show=True):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    colors = plt.cm.hsv(np.linspace(0.66, 0.0, len(a)))
    #colors = plt.cm.plasma(np.linspace(0, 0.95, len(a)))
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    xd = np.amin(np.abs(a[0][1:, 0] - a[0][:-1, 0]))
    xmm = np.amax(a[0][:, 0]) - np.amin(a[0][:, 0])
    plt.rcParams['errorbar.capsize'] = np.min([xd / 2. / 4., xmm / 100. / 4.])
    f = plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.5g'))

    i = 0
    for i in range(len(a)):
        ai = a[i]
        ei = errs[i]
        alabel = str(i)
        amarker = "o"
        alinestyle = ""
        amarkersize = 5.0
        
        if len(labels) > 0:
            alabel = labels[i]

        if len(ei[0]) == 1:
            plt.errorbar(ai[:, 0], ai[:, 1], yerr=ei[:, 0], label=alabel, marker=amarker, markersize=amarkersize, linestyle=alinestyle)
        elif len(ei[0]) == 2:
            plt.errorbar(ai[:, 0], ai[:, 1], yerr=ei[:, 0], xerr=ei[:, 1], label=alabel, marker=amarker, markersize=amarkersize, linestyle=alinestyle)
        i += 1
        
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    
    plt.grid(True)

    if len(labels) > 0 or (len(a) > 1 and len(a) <= 10):
        plt.legend(fontsize='xx-small')

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight') # save to file

    if show:
        plt.show()
        plt.close()
                
# histogram plot
def histplt(x, nbins, theor=None, titles=["Histogram", "x", "N"], label="", fpath="", show=True):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    f = plt.figure(figsize=(10, 10))
    # generate histogram of data x
    plt.hist(x, nbins, ec="tab:blue", label=label) #, density=True
    if theor is not None:
        tx = np.linspace(np.min(x), np.max(x), 1000)
        plt.plot(tx, theor(tx), label="Theory")

    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    
    #plt.grid(True)
    if len(label) > 0:
        plt.legend(fontsize='xx-small')

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight') # save to file

    if show:
        plt.show()
        plt.close()

# bar plot
def barplt(a, titles=["", "", ""],  label="", fpath="", show=True):
    plt.style.use('default')
    plt.rcParams.update({'font.size': 22})
    f = plt.figure(figsize=(10, 10))
    
    plt.bar(a[:, 0], a[:, 2], (a[:, 1]-a[:,0]), label=label, alpha=1.0, align="edge")

    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])

    #plt.grid(True)

    if len(fpath) > 0:
        f.savefig(fpath, bbox_inches='tight') # save to file

    if show:
        plt.show()
        plt.close()
        
