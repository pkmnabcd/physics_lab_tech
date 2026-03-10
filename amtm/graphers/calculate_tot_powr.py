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


#mainpath = 'C:/Users/Domi/OneDrive/Desktop/AMTM_McMurdo' # replace with path to AMTM_McMurdo folder.
mainpath = 'C:/Gabes_stuff/AMTM_ALOMAR'
months = ['January', 'February', 'April'] # full month folder names
#months = ['September', 'October', 'November', 'December'] # full month folder names

mons = ['Jan', 'Feb', 'Apr'] # abbreviated months
#mons = ['Sep', 'Oct', 'Nov', 'Dec'] # abbreviated months

#years = ['2015']
years = ['2014']

def getDaysTxtData(days_path):
    pass

def calcWindowTotalPowerOverTime(year, month, mon, night, begin, end, mainpath):
    days_path = join(mainpath, year, f'{month}{year}', 'days.txt')
    # TODO: Add code to make sure days.txt and timestamp.txt have the same amount of data
    # Look for the given day's index in the timestamp data

for i in range(np.size(years)): # Tells code go into each year folder
    year = years[i]
    print(year)


    for i in range(np.size(months)): # once inside the year, go into each month folder
        month = months[i]
        mon = mons[i]
        days_path = join(mainpath, year, f'{month}{year}', 'days.txt')
        print(month)


        with open(days_path, 'r') as dayfile:            # opens the days.txt file to get the names                .
            daysf =[]                                #of the day folders within each month
            for line in dayfile:
                if line[0] != '#':
                    if line.rstrip() != mon: # take away the \n, 
                        a =  mon+line.rstrip()    #a and b are used because I ran out of meaningful names
                        b = a.replace(" ","_",1) #this replacement is necessary as the txt file has whitespace
                        entry = b.replace(" ","-",1) #where the folders have _ and -'s
                        daysf.append(entry)
        timestamp_path = join(mainpath, year, f'{month}{year}', 'timestamp.txt')
 
        timefile = np.loadtxt(timestamp_path)
        if timefile.ndim == 1:
            timefile = np.array([timefile])  # This covers when np.loadtxt automatically reshapes single-row files

        tL = len(timefile) # Length of the columns in the file


        myear = timefile[:,0]
        mmonth = timefile[:,1]
        mday = timefile[:,2]
        mhour = timefile[:,3]
        mmin = timefile[:,4]
        msec = timefile[:,5]





        holder = [] 

        for i in range(0,tL):

            replace = mhour[i] + mmin[i]/60 + msec[i]/3600
            holder.append(replace)

        dec_hour = np.array(holder) #creates a numpy array containing the 
                                    #starting time in decimal hours
        for n in range(np.size(daysf)): #  Use the days list to get to the path each .csv file
            dyear = myear[n]
            dmonth = mmonth[n]
            dayframe = daysf[n] #day and frame range
            day = mday[n]
            hour = dec_hour[n]

            dayofinterest = mainpath+f'/{year}/{month}{year}/{dayframe}/'
            perd_power = [] # do exactly what I did for the month, but for the day
            perd_exponent = [] # so that I can have a time and power text file per day
            perd_timelist = []
            perd_y, perd_m, perd_d, perd_df = [],[],[], []
            perd_timelist = []
            perd_power = []
            perd_exponent = []


            for i in range(0,50):
                filenumber = i
                array1 = np.empty([L1,L2]) #creating an empty 301x301 array to import the 
                                            # csv file to.

                rows = [] # creating an empty list to hold csv row

                filename = f'TempOH{filenumber}_TOTAL.csv' 
                wholepath = dayofinterest+ filename

                if exists(wholepath) == True: #since each day has different number of .csv file, this only uses the ones that exist
                                      #code above was to get to the right location, everthing below is gets the power 
                    tally = hour + i*0.5 #Gets the time associated with the power file


                    perd_timelist.append(tally)
                    perd_y.append(dyear)
                    perd_m.append(dmonth)
                    perd_d.append(day)
                    perd_df.append(dayframe)





                    with open( wholepath, 'r') as file: #opening and reading csv
                        datafile = csv.reader(file)
                        for row in datafile:         #taking each row of the csv and putting into 
                            rows.append(row)         # a list, which results in a nested list

            #         #Takes each element that is not a value of -22 of the nested list (row[i][j] 
            #         #and places it the cooresponding array location (array[i,j]), the values of
            #         #-22 are repalced by zero, 

                        for i in range(0,L1):
                            for j in range(0,L2):
                                value = float(rows[i][j])
                                if -22 != value: 
                                    array1[i,j] = 10**value  #Takes value from txt file and makes it the power 10 it is raised to
                                    #print(array1[i,j])
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

                  #To make a file for each day
            perday_datetime = np.column_stack([perd_yrs,perd_monts, perd_days, perd_hrs, perd_powr, perd_exp])

            save_dayfile = mainpath +f'/{year}/{month}{year}/{dayframe}/T_and_power.txt'
            words = 'Total power for every half-hour of avalible data\n of'\
                f' {mon} {year} {day} where the columns are 0-year 1-month 2-day 3-time in decimal hour\n'\
                    '4- power value(x) 5-exponent(y) of power in base 10'

            np.savetxt(save_dayfile, perday_datetime, fmt ='%4d %2d %2d %1.6f %1.20f %1.5f'\
                        ,header = words, comments = '#')



