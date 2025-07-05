from sys import argv
from textwrap import wrap
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lombscargle


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
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    ohDoys = []
    ohAvgs = []
    ohStdevs = []
    for line in lines:
        cols = line.split(",")

        ohDoys.append(int(cols[0]))
        ohAvgs.append(float(cols[2]))
        ohStdevs.append(float(cols[3]))
    file.close()

    # NOTE: Getting daily SF data
    sfDoys = []
    sfAvgs = []
    file = open("solarFlux.txt")
    lines = file.readlines()
    for line in lines:
        lineYear = line[0:4]
        if year != lineYear:
            if int(year) < int(lineYear):
                break
            else:
                continue
        sfDoys.append(getDoy(int(year), int(line[5:7]), int(line[8:10])))
        sfAvgs.append(float(line[139 : 149]))
    file.close()
    return ohDoys, ohAvgs, ohStdevs, sfDoys, sfAvgs


def makeAndSaveSmoothGraph(time, dailyAvgs, smoothTime, smoothDailyAvgs, window_size, year, isOH):
    if isOH:
        datastub = "oh"
        datastublong = "OH Temp"
        unit = "K"
    else:
        datastub = "sf"
        datastublong = "Solar Flux"
        unit = "SFU"
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Day of Year", fontsize=20)
    ax1.set_ylabel(f"{datastublong} ({unit})", fontsize=20)
    ax1.plot(time, dailyAvgs, color="blue", label=f"Daily Average {datastublong}")
    ax1.plot(smoothTime, smoothDailyAvgs, color="red", label=f"Smoothed Daily Average {datastublong}")
    ax1.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = f"ChileMTM {year} Daily {datastublong} with Smoothed Curve (window size: {window_size})"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    outPath = f"yearly_frequencies_graphs/{year}_{datastub}_daily_average_smooth_on_top_win{window_size}.png"
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


def computeResidualGraph(time, avgs, window_size, year, isOH):
    # NOTE: Make sure window_size is odd
    smoothTime = doEndCutoffFromSmoothing(time, window_size)
    smoothAvgs = doSmoothing(avgs, window_size)
    cutoffAvgs = doEndCutoffFromSmoothing(avgs, window_size)

    makeAndSaveSmoothGraph(time, avgs, smoothTime, smoothAvgs, window_size, year, isOH)

    residualAvgs = np.array(cutoffAvgs) - np.array(smoothAvgs)
    return smoothTime, residualAvgs


def computeLombScargleGraph(time, avgs, window_size, year, isOH):
    residualTime, residualAvgs = computeResidualGraph(time, avgs, window_size, year, isOH)

    t = np.array(residualTime)
    x = np.array(residualAvgs)

    minFreq = 1 / (t.max() - t.min())
    maxFreq = 0.5 * (1 / np.mean(np.diff(t)))  # Don't ask me why this

    frequencyData = np.linspace(minFreq / 2, maxFreq * 1.5, 1000)
    powerData = lombscargle(t, x, frequencyData, normalize=True)
    frequencyData = frequencyData / (2*np.pi) # Convert from angular to regular freq for graphing
    periodData = 1 / frequencyData

    return frequencyData, periodData, powerData


def makeAndSaveFFTGraph(frequencies, powers, window_size, year, isOH):
    if isOH:
        datastub = "oh"
        datastubcap = "OH"
        datastublong = "OH Temp"
    else:
        datastub = "sf"
        datastubcap = "SF"
        datastublong = "Solar Flux"

    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Frequency (1/Day)", fontsize=20)
    ax1.set_ylabel(f"{datastubcap} Power", fontsize=20)
    ax1.plot(frequencies, powers, color="blue", label=datastublong)
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_xlim(np.min(frequencies), np.max(frequencies))

    ax2 = ax1.twiny()
    ax2.set_xlabel("Period (Days/Oscillation)", fontsize=20)

    # NOTE: set the period tick markers
    frequencyTicks = ax1.get_xticks()
    periodTickLabels = []
    for freq in frequencyTicks:
        if freq == 0:
            periodTickLabels.append("Inf")
        else:
            periodTickLabels.append(f'{1/freq:.2f}')
    ax2.set_xticks(frequencyTicks)
    ax2.set_xticklabels(periodTickLabels)
    ax2.set_xlim(ax1.get_xlim())

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = f"ChileMTM {year} Daily {datastublong} Residual Frequency Analysis (window size: {window_size})"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    outPath = f"yearly_frequencies_graphs/{year}_{datastub}_daily_average_frequencies_win{window_size}.png"
    plt.savefig(outPath)
    plt.close()
    print(f"File saved to {outPath} .")
    plt.close()


def saveDataCSV(frequencies, periods, powers, window_size, year, isOH):
    if isOH:
        datastub = "oh"
        datastubcap = "OH"
        datastublong = "OH Temp"
    else:
        datastub = "sf"
        datastubcap = "SF"
        datastublong = "Solar Flux"

    lines = []
    for i in range(len(frequencies)):
        lines.append(f"{frequencies[i]},{periods[i]},{powers[i]}\n")
    outpath = f"yearly_frequencies_graphs/{year}_{datastub}_daily_average_frequencies_win{window_size}.csv"
    file = open(outpath, "w")
    file.writelines(lines)
    file.close()
    print(f"File saved to {outpath} .")


if __name__ == "__main__":
    makedirs("yearly_frequencies_graphs", exist_ok=True)

    dailyAveragesStub = "dailyAverages.csv"
    years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    for year in years:
        # NOTE: This is meant to be run at the ChileMTM folder, with all the years
        averagesFile = year + "/" + year + dailyAveragesStub
        currentOHDoys, currentOHAvgs, currentOHStdevs, currentSfDoys, currentSfAvgs = readAverages(year, averagesFile)

        # NOTE: Solar cycle is 27 days, but in 27 days there's usually about 21 OH data points
        oh_window_sizes = [21]
        sf_window_sizes = [27]
        for window_size in oh_window_sizes:
            ohFrequencies, ohPeriods, ohPowers = computeLombScargleGraph(currentOHDoys, currentOHAvgs, window_size, year, isOH=True)
            makeAndSaveFFTGraph(ohFrequencies, ohPowers, window_size, year, isOH=True)
            saveDataCSV(ohFrequencies, ohPeriods, ohPowers, window_size, year, isOH=True)

        for window_size in sf_window_sizes:
            sfFrequencies, sfPeriods, sfPowers = computeLombScargleGraph(currentSfDoys, currentSfAvgs, window_size, year, isOH=False)
            makeAndSaveFFTGraph(sfFrequencies, sfPowers, window_size, year, isOH=False)
            saveDataCSV(sfFrequencies, sfPeriods, sfPowers, window_size, year, isOH=False)

