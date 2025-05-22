from sys import argv
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.fft import fftfreq

def readAverages(year, path):
    yearInt = int(year)
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    ohYearmonths = []  # this is the year and then some multiple of 1/12 to be the month
    ohAvgs = []
    ohStdevs = []
    for line in lines:
        cols = line.split(",")

        yearmonth = yearInt
        yearmonth += int(cols[0]) / 366  # Divide the day of year by the number of days possibly in the year

        ohAvgs.append(float(cols[2]))
        ohStdevs.append(float(cols[3]))
        ohYearmonths.append(yearmonth)

    file.close()
    return ohYearmonths, ohAvgs, ohStdevs


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


def computeFFTGraph(time, avgs, window_size=19):
    residualTime, residualAvgs = computeResidualGraph(time, avgs, window_size)
    residualAvgs = residualAvgs.tolist()

    # TODO: fix this and use the other kind of fft that's similar but has uneven sampling
    # I think it's lombscargle
    N = len(residualAvgs)  # Number sample points
    T = 1 / 12  # sample spacing (1/12 of a year)
    fftData = np.abs(fft(residualAvgs))[:N // 2]
    frequencyData = fftfreq(N, T)[:N // 2]

    return frequencyData, fftData


def makeAndSaveGraph(ohFrequencies, ohPowers, averagesPath):
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Frequency (1/Year)", fontsize=20)
    ax1.set_ylabel("OH Power ", fontsize=20)
    ax1.plot(ohFrequencies, ohPowers, color="blue", label="OH Temp")
    ax1.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM 2009-2024 Daily OH Temp Residual Frequency Analysis"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    outPath = "all_time_oh_daily_average_frequencies.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    alltimeYearmonths = []
    alltimeAvgs = []
    alltimeStdevs = []

    dailyAveragesStub = "dailyAverages.csv"
    years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    for year in years:
        # NOTE: This is meant to be run at the ChileMTM folder, with all the years
        averagesFile = year + "/" + year + dailyAveragesStub
        currentYearmonths, currentAvgs, currentStdevs = readAverages(year, averagesFile)
        alltimeYearmonths += currentYearmonths
        alltimeAvgs += currentAvgs
        alltimeStdevs += currentStdevs

    ohFrequencies, ohPowers = computeFFTGraph(alltimeYearmonths, alltimeAvgs)

    makeAndSaveGraph(ohFrequencies, ohPowers, averagesPath)

