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


def makeAndSaveGraph(ohSmoothYearmonths, sfSmoothYearmonths, ohSmoothAvgs, sfSmoothAvgs):
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Year", fontsize=20)
    ax1.set_ylabel("Solar Flux (SFU)", fontsize=20)
    ax1.plot(sfSmoothYearmonths, sfSmoothAvgs, color="red", label="Monthly Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Temp (K)", fontsize=20)
    ax2.plot(ohSmoothYearmonths, ohSmoothAvgs, color="blue", label="Monthly Average OH Temp")
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM 2009-2024 Monthly OH Temp and Solar Flux Smoothed Graphs (window: 19)"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    plt.tight_layout()

    outPath = "all_time_oh_sf_month_average_both_smooth.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, sfStdevs = readAverages(averagesPath)

    ohYearmonthSmoothed, ohAvgSmoothed = computeSmoothGraph(ohYearmonths, ohAvgs)
    sfYearmonthSmoothed, sfAvgSmoothed = computeSmoothGraph(sfYearmonths, sfAvgs)

    makeAndSaveGraph(ohYearmonthSmoothed, sfYearmonthSmoothed, ohAvgSmoothed, sfAvgSmoothed)

