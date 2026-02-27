# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:03:43 2019

@author: Kenneth
version 3: Connor Waite
version 4: Gabriel Decker
    This version is intended to be hooked up with the power_spectrum_runner.py
    This version lacks the monthly average power spectrum since we're not interested in that
"""

# The purpose of this code is to create power spectrums for each of the windows
# using the output of the FFT analysis. The program iterates through the specified
# months and creates one power spectrum per window. It also makes an average 
# power spectrum for each month and a plot for each month showing the total power 
# of each window in the month.

from calendar import monthrange
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob as glob
import os
from os.path import exists


plt.rcParams.update({'font.size': 15})

year = '2016'

# For ALOMAR End of Year
month1 = ['August','September', 'October', 'November', 'December']
month2 = ['Aug','Sep', 'Oct', 'Nov', 'Dec']

# For ALOMAR Start of Year
#month1 = ['January', 'February', 'March','April']
#month2 = ['Jan', 'Feb', 'Mar','Apr']


month1 = ['September', 'October', 'November']
month2 = ['Sep', 'Oct', 'Nov']

doWholeMonth = False


def month_to_number(string):
    m = {
         'Jan':1,
         'Feb':2,
         'Mar':3,
         'Apr':4,
         'May':5,
         'Jun':6,
         'Jul':7,
         'Aug':8,
         'Sep':9,
         'Oct':10,
         'Nov':11,
         'Dec':12
        }
    out = m[string]
    return out


for r in range(np.size(month1)):
    #Path of csv files but also need to mkdir Figures to save all these figure to.
    month=month1[r]
    months=month2[r] # Short month names
    monthz=month+year
    Filez=os.path.join(r"C:\Gabes_stuff\\AMTM_ALOMAR",year,month+year,months)
    MonFilez=os.path.join(r"C:\Gabes_stuff\\AMTM_ALOMAR",year,month+year)
    days=glob.glob(Filez+'*')
    numDays=np.size(days)

    winTotals = []  # Stores the total power for each window
    winDays = []  # Stores the day of each window

    totdata=np.zeros((300,301,numDays))

    #Loops through days that were analyzed
    for z in range(numDays):
        d=days[z]
        a=os.path.split(d)
        b=str(a[1])
        a=b.split('_')

        perpath=d
        date=months+d[0]

        patha=perpath+'\OH_TOTAL.csv'

        filesa=patha

        data=np.zeros((300,301))
        Avgdata=np.zeros((300,301))
        data3=np.zeros((300,301))
        data1=np.zeros((300,301))

        print(filesa)
        if not exists(filesa):
            print("WARNING! File missing: " + filesa)
            continue
        data2 = pd.read_csv(filesa)
        data1[:,:]=(data2.values)
        #To keep range from 5-150 m/s
        data1[149-3:149+3,150-3:150+3]=np.full((6,6),-22.0)

        winTotals.append(np.sum(10**data1[:,:]))  # Stores the total power of the window
        winDays.append(int(b[3:5]))  # Stores the day of the month of the window

        x=np.arange(-len(data)/2,len(data)/2,1)
        y=np.arange(-len(data)/2,len(data)/2,1)
        x0=np.zeros(len(data))
        y0=np.zeros(len(data))

        #Produces figure of Phase Speed PSD for that clean window
        plt.figure(figsize=(10,8))
        data[:,:]=np.log10(10**data1[:,:])
        t=np.sum((data[:,:]))

        ind = np.unravel_index(np.argmax(data, axis=None), data.shape)
        xmax=float(int(ind[1])-150)
        ymax=float(int(ind[0])-150)
        psmax=np.sqrt(xmax**2+ymax**2)
        theta=np.arctan2(ymax,xmax)*180.0/(np.pi)

        circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
        circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
        circle3 = plt.Circle((0, 0), 150, color='k', fill=False)

        circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
        circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
        circle3 = plt.Circle((0, 0), 150, color='k', fill=False)

        circle11 = plt.Circle((0, 0), 10,linestyle=':', color='k', fill=False)
        circle21 = plt.Circle((0, 0), 20,linestyle=':', color='k', fill=False)
        circle31 = plt.Circle((0, 0), 30,linestyle=':', color='k', fill=False)
        circle41 = plt.Circle((0, 0), 40,linestyle=':', color='k', fill=False)

        circle12 = plt.Circle((0, 0), 110,linestyle=':', color='k', fill=False)
        circle22 = plt.Circle((0, 0), 120,linestyle=':', color='k', fill=False)
        circle32 = plt.Circle((0, 0), 130,linestyle=':', color='k', fill=False)
        circle42 = plt.Circle((0, 0), 140,linestyle=':', color='k', fill=False)

        circle13 = plt.Circle((0, 0), 60,linestyle=':', color='k', fill=False)
        circle23 = plt.Circle((0, 0), 70,linestyle=':', color='k', fill=False)
        circle33 = plt.Circle((0, 0), 80,linestyle=':', color='k', fill=False)
        circle43 = plt.Circle((0, 0), 90,linestyle=':', color='k', fill=False)

        ####################Actual Mesh Plot
        # This is probaly responsible for the log power scale changing with each graph.
        plt.pcolormesh(x,y,(data[:,:-1]),cmap='jet',vmin=-10, vmax = -6.5)
        plt.colorbar(label='log$_{10}$(PSD)')

        totdata[:,:,z]=data[:,:]
        plt.plot()
        plt.title('Average')

        plt.plot(x0,y,color='k',lw='0.5')
        plt.plot(x,y0,color='k',lw='0.5')
        plt.gcf().gca().add_artist(circle1)
        plt.gcf().gca().add_artist(circle2)
        plt.gcf().gca().add_artist(circle3)
        plt.gcf().gca().add_artist(circle11)
        plt.gcf().gca().add_artist(circle21)
        plt.gcf().gca().add_artist(circle31)
        plt.gcf().gca().add_artist(circle41)
        plt.gcf().gca().add_artist(circle12)
        plt.gcf().gca().add_artist(circle22)
        plt.gcf().gca().add_artist(circle32)
        plt.gcf().gca().add_artist(circle42)
        plt.gcf().gca().add_artist(circle13)
        plt.gcf().gca().add_artist(circle23)
        plt.gcf().gca().add_artist(circle33)
        plt.gcf().gca().add_artist(circle43)

        plt.xticks(np.arange(-150,150,50))
        plt.yticks(np.arange(-150,150,50))

        plt.xlim(-150,150)
        plt.ylim(-150,150)
        plt.xlabel('W-E [m/s]')
        plt.ylabel('N-S [m/s]')

        plt.show()
        b0= b.split("_")[0]
        b1 = b.split("_")[1]

        # Save Name and Location !!!!
        plt.savefig(os.path.join(MonFilez,b0+"OH_"+b1+".jpg"))
