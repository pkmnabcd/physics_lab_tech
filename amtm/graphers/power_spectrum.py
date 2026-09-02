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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv
from os.path import exists, join


plt.rcParams.update({'font.size': 15})

MONTH_STUBS = {
    0: "Jan",
    1: "Feb",
    2: "Mar",
    3: "Apr",
    4: "May",
    5: "Jun",
    6: "Jul",
    7: "Aug",
    8: "Sep",
    9: "Oct",
    10: "Nov",
    11: "Dec"
}


def getTimestamp(img_path):
    with open(img_path, "rb") as f:
        f.seek(247)
        second = int.from_bytes(f.read(4), "little")
        minute = int.from_bytes(f.read(4), "little")
        hour = int.from_bytes(f.read(4), "little")
        day = int.from_bytes(f.read(4), "little")
        month = int.from_bytes(f.read(4), "little")   # January is the 1st month, represented by 0.
        year = int.from_bytes(f.read(4), "little") + 1900 # year is defined relative to 1900

        timestamp = f"{MONTH_STUBS[month]} {day}, {year} {hour:02}:{minute:02}:{second:02}"
        return timestamp


def generateSpectrumPlot(oh_total_path, fig_save_path, fig_title):
    data=np.zeros((300,301))
    data1=np.zeros((300,301))
    data2 = read_csv(oh_total_path)
    data1[:,:]=(data2.values)
    #To keep range from 5-150 m/s
    data1[149-3:149+3,150-3:150+3]=np.full((6,6),-22.0)

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
    plt.pcolormesh(x,y,(data[:,:-1]),cmap='jet',vmin=-10, vmax = -7)
    plt.colorbar(label='log$_{10}$(PSD)')

    plt.plot()
    plt.title(fig_title, pad=20)

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

    plt.xlim(-100,100)
    plt.ylim(-100,100)
    plt.xlabel('W-E [m/s]')
    plt.ylabel('N-S [m/s]')

    plt.savefig(fig_save_path)
    print(f"Figure saved to {fig_save_path}!")
    plt.close()


def makeDailyPowerSpectrum(year, month, mon, night, begin, end, main_path, drivePath, p12_img_stub):
    """
    year: str: form of "2024"
    month: str: form of "December"
    mon: str: form of "Dec"
    night: str: form of "09-10"
    begin: str: form of "0000"
    end: str: form of "1462"
    main_path: str: path to main folder. Ex: "C:/Users/Ken/Desktop/AMTM_McMurdo"
        In this directory is the various year folders, summary files, winter total power graphs, etc.
    drivePath: str: path to the drive folder containing the {month}{year} directories.
    p12_img_stub: str: usually either "P12_31_" or "P12_1_"
    """
    # Prep a bunch of strings/paths I'll need later
    base_path = join(main_path, year, f"{month}{year}")
    oh_total_path = join(base_path, f"{mon}{night}_{begin}-{end}", "TempOH_TOTAL.csv")
    fig_save_path = join(base_path, f"{mon}{night}OH_{begin}-{end}.jpg")
    timestamp_start_path = join(drivePath, f"{month}{year}", f"{mon}{night}", f"{p12_img_stub}{begin}.tif")
    timestamp_end_path = join(drivePath, f"{month}{year}", f"{mon}{night}", f"{p12_img_stub}{end}.tif")

    timestamp_start = getTimestamp(timestamp_start_path)
    timestamp_end = getTimestamp(timestamp_end_path)
    fig_title = f"Power Spectrum {mon}{night}, {year}\n{timestamp_start} to {timestamp_end} (UTC)"

    if not exists(oh_total_path):
        print("WARNING! File missing: " + oh_total_path)
        return

    generateSpectrumPlot(oh_total_path, fig_save_path, fig_title)

def makeMonthlyPowerSpectrum(year, month, mon, power_spectrum_paths, main_path):
    # NOTE: define the save path based on main path and year and month, etc
    fig_save_path = join(main_path, year, f"{month}{year}", f"{mon}{year}_avg_spectrum.png")
    avg_csv_save_path = join(main_path, year, f"{month}{year}", f"{mon}{year}_TempOH_Total.csv")
    CSV_SHAPE = (300, 301)

    # Get average CSV of the month
    avg_csv = np.zeros(CSV_SHAPE)
    csv_count = len(power_spectrum_paths)
    for csv_path in power_spectrum_paths:
        csv_data = read_csv(csv_path)
        if csv_data.shape != CSV_SHAPE:
            print(f"A csv file has this shape {csv_data.shape} instead of {CSV_SHAPE}.\n\tFound at this path: {csv_path}")
            return False
        avg_csv += csv_data
    avg_csv /= csv_count
    avg_csv.to_csv(avg_csv_save_path, index=False)

    fig_title = f"Monthly Average Power Spectrum {month} {year}"
    generateSpectrumPlot(avg_csv_save_path, fig_save_path, fig_title)
    return True
