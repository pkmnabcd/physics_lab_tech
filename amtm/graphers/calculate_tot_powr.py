#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:46:30 2023

@author: jennywhiteley
    originally Power_w_time.py
Changed it a lot. I got rid of code that would make total power files
for the whole month or year since that info is redundant and not used.
"""

#Have this code in the AMTM_McMurdo folder, then it extracts the total power
# and writes to a textfile.
#Code is for taking the OH#_TOTAL.csv files that are generated for every
#half-hour and summing all power values to get the total power — as one
#numerical result. The cvs files basically corresponds to the FFT transformed 
#image, so each cell (pixel) has a numerical value, the image/array size is 
# 301x301 and the values of interest are contained in the circle of the lens.
# The "corners" of the image have no information. In the cvs file these cells 
#are filled with "-22". This code removes all cells with a -22 value and sums
#any other cells

import numpy as np
import math as math
import csv
from os.path import exists, join

L1 = 301 #numbers of rows in csv file
L2 = 301 #numbers of column in csv file


def getDaysTxtData(days_path):
    split_lines = []
    with open(days_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            line = line.strip("\n\r")
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split()
            if i == 0: # The first line should be the month stub
                if len(parts) != 1:
                    print("WARNING! The first line should be the month stub like Nov or Apr. Make sure days.txt is formatted correctly.")
                continue
            if len(parts) != 3:
                print(f"WARNING! parts has a length of {len(parts)} instead of 3. Make sure days.txt is formatted correctly.")
            split_lines.append(parts)

    data = []
    for line in split_lines:
        data.append((line[0], int(line[1]), int(line[2])))
    return data


def getWindowIndex(days_data, night, begin, end):
    window_found = False
    index = -1
    for i in range(len(days_data)):
        if days_data[i][0] == night and days_data[i][1] == begin and days_data[i][2] == end:
            index = i
            window_found = True
            break

    return window_found, index


# NOTE: make sure begin and end are strings
def calcWindowTotalPowerOverTime(year, month, mon, night, begin, end, mainpath):
    dayframe = f'{mon}{night}_{begin}-{end}'

    days_path = join(mainpath, year, f'{month}{year}', 'days.txt')
    timestamp_path = join(mainpath, year, f'{month}{year}', 'timestamp.txt')
    save_path = join(mainpath, year, f'{month}{year}', dayframe, "T_and_power.txt")

    days_data = getDaysTxtData(days_path)
    timestamp_data = np.loadtxt(timestamp_path)

    if timestamp_data.ndim == 1:
        timestamp_data = np.array([timestamp_data])  # This covers when np.loadtxt automatically reshapes single-row files

    if not len(days_data) == len(timestamp_data):
        print(f"WARNING: The length of days.txt: {len(days_data)} does not equal the length of timestamp.txt: {len(timestamp_data)}")
        return

    myear = timestamp_data[:,0]
    mmonth = timestamp_data[:,1]
    mday = timestamp_data[:,2]
    mhour = timestamp_data[:,3]
    mmin = timestamp_data[:,4]
    msec = timestamp_data[:,5]

    tL = len(timestamp_data) # Length of the columns in the file
    # creates a numpy array containing the starting time in decimal hours
    tmp_dec_hour_holder = []
    for i in range(0,tL):
        replace = mhour[i] + mmin[i]/60 + msec[i]/3600
        tmp_dec_hour_holder.append(replace)
    dec_hour = np.array(tmp_dec_hour_holder)

    found, window_index = getWindowIndex(days_data, night, begin, end)
    if not found:
        print(f"WARNING!! The window {mon}{night} [{begin},{end}] was not found in days.txt. Make sure everything in days.txt is present and formatted correctly.")
        return

    dyear = myear[window_index]
    dmonth = mmonth[window_index]
    day = mday[window_index]
    hour = dec_hour[window_index]

    perd_power = []
    perd_exponent = []
    perd_timelist = []
    perd_y, perd_m, perd_d, perd_df = [],[],[], []
    perd_timelist = []
    perd_power = []
    perd_exponent = []

    # Iterating over each possible TempOH _TOTAL.csv file
    for i in range(0,50):
        csv_path = join(mainpath, year, f"{month}{year}", dayframe, f"TempOH{i}_TOTAL.csv")
        if not exists(csv_path):
            break
        tally = hour + i*0.5 #Gets the time associated with the power file

        perd_timelist.append(tally)
        perd_y.append(dyear)
        perd_m.append(dmonth)
        perd_d.append(day)
        perd_df.append(dayframe)

        #creating an empty 301x301 array to import the csv file to.
        array1 = np.empty([L1,L2])
        rows = [] # creating an empty list to hold csv row
        with open(csv_path, 'r') as file: #opening and reading csv
            datafile = csv.reader(file)
            for row in datafile:         #taking each row of the csv and putting into
                rows.append(row)         # a list, which results in a nested list

            # Takes each element that is not a value of -22 of the nested list (row[i][j]
            # and places it the cooresponding array location (array[i,j]), the values of
            # -22 are replaced by zero,

            for i in range(0,L1):
                for j in range(0,L2):
                    value = float(rows[i][j])
                    if -22 != value:
                        #Takes value from txt file and makes it the power 10 it is raised to
                        array1[i,j] = 10**value
                    elif -22 == value:
                        array1[i,j] = 0

        powerval = np.sum(array1) #this sum gives the total power
        perd_power.append(powerval)
        perd_exponent.append(math.log10(powerval))


    perd_yrs = np.array(perd_y)
    perd_monts = np.array(perd_m)
    perd_days = np.array(perd_d)
    perd_hrs = np.array(perd_timelist)
    perd_powr = np.array(perd_power)
    perd_exp = np.array(perd_exponent)

    # Make a T_and_power.txt file for each day
    perday_datetime = np.column_stack([perd_yrs,perd_monts, perd_days, perd_hrs, perd_powr, perd_exp])

    words = 'Total power for every half-hour of avalible data\n of'\
        f' {mon} {year} {day} where the columns are 0-year 1-month 2-day 3-time in decimal hour\n'\
            '4- power value(x) 5-exponent(y) of power in base 10'

    np.savetxt(save_path, perday_datetime, fmt ='%4d %2d %2d %1.6f %1.20f %1.5f'\
                ,header = words, comments = '#')
