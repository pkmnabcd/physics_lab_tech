from sys import argv
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np

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


def computeSmoothGraph(time, avgs, window_size=19):
    # NOTE: Make sure window_size is odd
    smoothTime = doEndCutoffFromSmoothing(time, window_size)
    smoothAvgs = doSmoothing(avgs, window_size)

    return smoothTime, smoothAvgs


def makeAndSaveGraph(yearmonths, smoothYearmonths, avgs, smoothAvgs, averagesPath, isOH=True):
    if isOH:
        ylabel = "OH Temp (K)"
        dataLabel = "Monthly Average OH Temp"
        smoothLabel = "Smoothed OH Temp"
        title = "ChileMTM 2009-2024 Monthly OH Temp with Smoothed Graph (window: 19)"
        outPath = "all_time_oh_month_average_smooth.png"
    else:
        ylabel = "Solar Flux (SFU)"
        dataLabel = "Monthly Average Solar Flux"
        smoothLabel = "Smoothed Solar Flux"
        title = "2009-2024 Monthly Solar Flux with Smoothed Graph (window: 19)"
        outPath = "all_time_sf_month_average_smooth.png"

    fig, ax1 = plt.subplots(figsize=(14,10))
    ax1.set_xlabel("Year", fontsize=22)
    ax1.set_ylabel(ylabel, fontsize=22)
    ax1.plot(yearmonths, avgs, color="red", label=dataLabel)
    ax1.plot(smoothYearmonths, smoothAvgs, color="blue", label=smoothLabel)
    ax1.tick_params(axis="both", labelsize=20)

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    #ax1.legend(lines1, labels1, loc="lower right", fontsize=20)
    ax1.legend(lines1, labels1, fontsize=20)
    plt.tight_layout()

    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, sfStdevs = readAverages(averagesPath)

    ohYearmonthSmoothed, ohAvgSmoothed = computeSmoothGraph(ohYearmonths, ohAvgs)
    sfYearmonthSmoothed, sfAvgSmoothed = computeSmoothGraph(sfYearmonths, sfAvgs)

    makeAndSaveGraph(ohYearmonths, ohYearmonthSmoothed, ohAvgs, ohAvgSmoothed, averagesPath, isOH=True)
    makeAndSaveGraph(sfYearmonths, sfYearmonthSmoothed, sfAvgs, sfAvgSmoothed, averagesPath, isOH=False)

