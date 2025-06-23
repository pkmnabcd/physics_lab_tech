from sys import argv
from textwrap import wrap
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle


def filterPeriods(periods, frequencies, powers, maxPeriod):
    newPeriods = []
    newFrequencies = []
    newPowers = []
    for i in range(len(periods)):
        if periods[i] < maxPeriod:
            newPeriods.append(periods[i])
            newFrequencies.append(frequenices[i])
            newPowers.append(powers[i])

    return np.array(newPeriods), np.array(newFrequenices), np.array(newPowers)


def getDoy(year, month, day):
    if year % 4 == 0:
        leapYearAdd = 1
    else:
        leapYearAdd = 0
    match month:
        case 1:
            return 0 + day
        case 2:
            return 31 + day
        case 3:
            return 59 + leapYearAdd + day
        case 4:
            return 90 + leapYearAdd + day
        case 5:
            return 120 + leapYearAdd + day
        case 6:
            return 151 + leapYearAdd + day
        case 7:
            return 181 + leapYearAdd + day
        case 8:
            return 212 + leapYearAdd + day
        case 9:
            return 243 + leapYearAdd + day
        case 10:
            return 273 + leapYearAdd + day
        case 11:
            return 304 + leapYearAdd + day
        case 12:
            return 334 + leapYearAdd + day

def readAverages(year, path):
    # NOTE: Getting daliy OH data
    yearInt = int(year)
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    ohYeardoys = []  # this is the year and then some multiple of 1/366 to be the doy
    sfYeardoys = []
    sfAvgs = []
    ohAvgs = []
    ohStdevs = []
    for line in lines:
        cols = line.split(",")

        yeardoy = yearInt
        yeardoy += int(cols[0]) / 366  # Divide the day of year by the number of days possibly in the year

        ohAvgs.append(float(cols[2]))
        ohStdevs.append(float(cols[3]))
        ohYeardoys.append(yeardoy)

    file.close()

    # NOTE: Getting daily SF data
    file = open("solarFlux.txt")
    lines = file.readlines()
    for line in lines:
        lineYear = line[0:4]
        if year != lineYear:
            if yearInt < int(lineYear):
                break
            else:
                continue
        currentYearmonth = int(lineYear)
        currentYearmonth += getDoy(yearInt, int(line[5:7]), int(line[8:10])) / 366
        sfYeardoys.append(currentYearmonth)
        sfAvgs.append(float(line[139 : 149]))
    file.close()
    return ohYeardoys, ohAvgs, ohStdevs, sfYeardoys, sfAvgs


def makeAndSaveSmoothGraph(time, dailyAvgs, smoothTime, smoothDailyAvgs, window_size, isOH):
    if isOH:
        datastub = "oh"
        datastublong = "OH Temp"
        unit = "K"
    else:
        datastub = "sf"
        datastublong = "Solar Flux"
        unit = "SFU"
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Year", fontsize=20)
    ax1.set_ylabel(f"{datastublong} ({unit})", fontsize=20)
    ax1.plot(time, dailyAvgs, color="blue", label=f"Daily Average {datastublong}")
    ax1.plot(smoothTime, smoothDailyAvgs, color="red", label=f"Smoothed Daily Average {datastublong}")
    ax1.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = f"ChileMTM 2009-2024 Daily {datastublong} with Smoothed Curve (window size: {window_size})"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    outPath = f"all-time_frequencies_graphs/all_time_{datastub}_daily_average_smooth_on_top_win{window_size}.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")
    plt.close()


def doSmoothing(array, window_size):
    i = 0
    moving_averages = []

    while i < len(array) - window_size + 1:
        # NOTE: This is slow because I query the same data over and over again
        window_average = round(np.sum(array[i:i + window_size]) / window_size, 2)
        moving_averages.append(window_average)
        i += 1

    return moving_averages


def doEndCutoffFromSmoothing(array, window_size):
    removeCount = window_size - 1
    if removeCount % 2 == 1:
        print("WARNING!! removeCount IS NOT EVEN!!!!!!!!!!!!!!!!!")

    out_list = []
    for value in array:  # Copy the array to not modify the original
        out_list.append(value)
    front_pop_count = removeCount // 2
    back_pop_count = removeCount // 2
    for i in range(front_pop_count):
        out_list.pop(0)
    for i in range(back_pop_count):
        out_list.pop()
    return out_list


def computeResidualGraph(time, avgs, window_size, isOH):
    # NOTE: Make sure window_size is odd
    smoothTime = doEndCutoffFromSmoothing(time, window_size)
    smoothAvgs = doSmoothing(avgs, window_size)
    cutoffAvgs = doEndCutoffFromSmoothing(avgs, window_size)

    makeAndSaveSmoothGraph(time, avgs, smoothTime, smoothAvgs, window_size, isOH)

    residualAvgs = np.array(cutoffAvgs) - np.array(smoothAvgs)
    return smoothTime, residualAvgs


def computeLombScargleGraph(time, avgs, window_size, isOH):
    residualTime, residualAvgs = computeResidualGraph(time, avgs, window_size, isOH)

    t = np.array(residualTime)
    x = np.array(residualAvgs)

    minFreq = 1 / (t.max() - t.min())
    maxFreq = 0.5 * (1 / np.mean(np.diff(t)))   # Don't ask me why this

    frequencyData = np.linspace(minFreq / 2, maxFreq * 1.5, 1000)
    powerData = lombscargle(t, x, frequencyData, normalize=True)
    frequencyData = frequencyData / (2*np.pi)   # Convert from angular to regular freq for graphing
    periodData = 1 / frequencyData
    periodData = periodData * 365    # Change units to days per oscillation

    periodData, frequencyData, powerData = filterPeriods(periodData, frequencyData, powerData, 5000)

    return frequencyData, periodData, powerData


def makeAndSaveFFTGraph(frequencies, periods, powers, window_size, isOH):
    if isOH:
        datastub = "oh"
        datastubcap = "OH"
        datastublong = "OH Temp"
    else:
        datastub = "sf"
        datastubcap = "SF"
        datastublong = "Solar Flux"

    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Period (Days/Oscillation)", fontsize=20)
    ax1.set_ylabel(f"{datastubcap} Power ", fontsize=20)
    ax1.plot(periods, powers, color="blue", label=f"{datastublong}")
    ax1.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = f"ChileMTM 2009-2024 Daily {datastublong} Residual Frequency Analysis (window size: {window_size})"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    outPath = f"all-time_frequencies_graphs/all_time_{datastub}_daily_average_frequencies_win{window_size}.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")
    plt.close()


def saveDataCSV(frequencies, periods, powers, window_size, isOH):
    if isOH:
        datastub = "oh"
    else:
        datastub = "sf"
    lines = []
    for i in range(len(frequencies)):
        lines.append(f"{frequencies[i]},{periods[i]},{powers[i]}\n")
    outpath = f"all-time_frequencies_graphs/all_time_{datastub}_daily_average_frequencies_win{window_size}.csv"
    file = open(outpath, "w")
    file.writelines(lines)
    file.close()
    print(f"File saved to {outpath} .")


if __name__ == "__main__":
    makedirs("all-time_frequencies_graphs", exist_ok=True)

    alltimeOHYeardoys = []
    alltimeOHAvgs = []
    alltimeOHStdevs = []
    alltimeSfYeardoys = []
    alltimeSfAvgs = []

    dailyAveragesStub = "dailyAverages.csv"
    years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    for year in years:
        # NOTE: This is meant to be run at the ChileMTM folder, with all the years
        averagesFile = year + "/" + year + dailyAveragesStub
        currentOHYeardoys, currentOHAvgs, currentOHStdevs, currentSfYeardoys, currentSfAvgs = readAverages(year, averagesFile)
        alltimeOHYeardoys += currentOHYeardoys
        alltimeOHAvgs += currentOHAvgs
        alltimeOHStdevs += currentOHStdevs
        alltimeSfYeardoys += currentSfYeardoys
        alltimeSfAvgs += currentSfAvgs

    # NOTE: Solar cycle is 27 days, but in 27 days there's usually about 21 data points in OH
    # NOTE: 59 is just a decent window size for the size of the dataset
    # NOTE: The average number of OH data points in a year is 231
    oh_window_sizes = [21, 59, 231]
    for window_size in oh_window_sizes:
        ohFrequencies, ohPeriods, ohPowers = computeLombScargleGraph(alltimeOHYeardoys, alltimeOHAvgs, window_size, isOH=True)
        makeAndSaveFFTGraph(ohFrequencies, ohPeriods, ohPowers, window_size, isOH=True)
        saveDataCSV(ohFrequencies, ohPeriods, ohPowers, window_size, isOH=True)

    sf_window_sizes = [21, 27, 59, 231, 365]
    for window_size in sf_window_sizes:
        sfFrequencies, sfPeriods, sfPowers = computeLombScargleGraph(alltimeSfYeardoys, alltimeSfAvgs, window_size, isOH=False)
        makeAndSaveFFTGraph(sfFrequencies, sfPeriods, sfPowers, window_size, isOH=False)
        saveDataCSV(sfFrequencies, sfPeriods, sfPowers, window_size, isOH=False)

