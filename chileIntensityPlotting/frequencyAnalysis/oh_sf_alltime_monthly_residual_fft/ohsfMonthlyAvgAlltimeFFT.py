from sys import argv
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.fft import fftfreq

def readAverages(path):
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    ohYearmonths = []  # this is the year and then some multiple of 1/12 to be the month
    sfYearmonths = []  # this is the year and then some multiple of 1/12 to be the month
    ohAvgs = []
    solarAvgs = []
    ohStdevs = []
    solarStdevs = []
    for line in lines:
        cols = line.split(",")

        yearmonth = int(cols[0])
        month = int(cols[1]) - 1
        yearmonth += (1/12) * month

        ohAvg = cols[2]
        if not ohAvg == '':
            ohAvgs.append(float(ohAvg))
            ohStdevs.append(float(cols[4]))
            ohYearmonths.append(yearmonth)

        solarAvgs.append(float(cols[3]))
        solarStdevs.append(float(cols[5]))
        sfYearmonths.append(yearmonth)

    file.close()
    return ohYearmonths, sfYearmonths, ohAvgs, solarAvgs, ohStdevs, solarStdevs


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


def computeResidualGraph(time, avgs, window_size):
    # NOTE: Make sure window_size is odd
    smoothTime = doEndCutoffFromSmoothing(time, window_size)
    smoothAvgs = doSmoothing(avgs, window_size)
    cutoffAvgs = doEndCutoffFromSmoothing(avgs, window_size)

    residualAvgs = np.array(cutoffAvgs) - np.array(smoothAvgs)
    return smoothTime, residualAvgs


def computeFFTGraph(time, avgs, window_size=19, isOH=False):
    residualTime, residualAvgs = computeResidualGraph(time, avgs, window_size)
    residualAvgs = residualAvgs.tolist()

    if isOH:
        # Need to add 0s to OH data since it is missing a couple months

        # Add 0 to May, June 2015
        new2015Index = residualTime.index(2015.5)
        residualTime.insert(new2015Index, (2015 + ((6-1)*(1/12))))
        residualTime.insert(new2015Index, (2015 + ((5-1)*(1/12))))
        residualAvgs.insert(new2015Index, 0)
        residualAvgs.insert(new2015Index, 0)

        # Add 0 to June 2022
        new2022Index = residualTime.index(2022.5)
        residualTime.insert(new2022Index, (2022 + ((6-1)*(1/12))))
        residualAvgs.insert(new2022Index, 0)

    N = len(residualAvgs)  # Number sample points
    T = 1 / 12  # sample spacing (1/12 of a year)
    fftData = np.abs(fft(residualAvgs))[:N // 2]
    frequencyData = fftfreq(N, T)[:N // 2]

    return frequencyData, fftData


def makeAndSaveGraph(ohFrequencies, sfFrequencies, ohPowers, sfPowers, averagesPath):
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Frequency (1/Year)", fontsize=20)
    ax1.set_ylabel("Solar Flux Power", fontsize=20)
    ax1.plot(sfFrequencies, sfPowers, color="red", label="Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Power ", fontsize=20)
    ax2.plot(ohFrequencies, ohPowers, color="blue", label="OH Temp")
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM 2009-2024 Monthly OH Temp and Solar Flux Residual Frequency Analysis"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    plt.tight_layout()

    outPath = "all_time_oh_sf_month_average_frequencies.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, sfStdevs = readAverages(averagesPath)

    ohFrequencies, ohPowers = computeFFTGraph(ohYearmonths, ohAvgs, isOH=True)
    sfFrequencies, sfPowers = computeFFTGraph(sfYearmonths, sfAvgs)

    makeAndSaveGraph(ohFrequencies, sfFrequencies, ohPowers, sfPowers, averagesPath)

