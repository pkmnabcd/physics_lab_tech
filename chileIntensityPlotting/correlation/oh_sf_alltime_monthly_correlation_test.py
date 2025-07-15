from sys import argv
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

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


def runPearsonCorrelation(d0, d1):
    print(" --- Running Pearson's r ---")
    if not len(d0) == len(d1):
        print(f"WARNING: d0 and d1 are not the same size.\nlen(d0)={len(d0)}\nlen(d1)={len(d1)}")
    correlationCoefficient, r_value = pearsonr(d0, d1)
    print(f"\tCorrelation Coefficient: {correlationCoefficient}\n\tr-value: {r_value}")


def runSpearmanCorrelation(d0, d1):
    print(" --- Running Spearman's rho ---")
    if not len(d0) == len(d1):
        print(f"WARNING: d0 and d1 are not the same size.\nlen(d0)={len(d0)}\nlen(d1)={len(d1)}")
    result = spearmanr(d0, d1)
    correlationCoefficient = result.statistic
    r_value = result.pvalue
    print(f"\tCorrelation Coefficient: {correlationCoefficient}\n\tr-value: {r_value}")


def runKendallCorrelation(d0, d1):
    print(" --- Running Kendall's Tau ---")
    if not len(d0) == len(d1):
        print(f"WARNING: d0 and d1 are not the same size.\nlen(d0)={len(d0)}\nlen(d1)={len(d1)}")
    result = kendalltau(d0, d1)
    correlationCoefficient = result.statistic
    r_value = result.pvalue
    print(f"\tCorrelation Coefficient: {correlationCoefficient}\n\tr-value: {r_value}")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, sfStdevs = readAverages(averagesPath)

    ohYearmonthSmoothed, ohAvgSmoothed = computeSmoothGraph(ohYearmonths, ohAvgs)
    sfYearmonthSmoothed, sfAvgSmoothed = computeSmoothGraph(sfYearmonths, sfAvgs)

    print(" ===== Testing Correlation on unsmoothed data =====")
    runPearsonCorrelation(ohAvgs, sfAvgs)
    runSpearmanCorrelation(ohAvgs, sfAvgs)
    runKendallCorrelation(ohAvgs, sfAvgs)

    print(" ===== Testing Correlation on smoothed data =====")
    runPearsonCorrelation(ohAvgSmoothed, sfAvgSmoothed)
    runSpearmanCorrelation(ohAvgSmoothed, sfAvgSmoothed)
    runKendallCorrelation(ohAvgSmoothed, sfAvgSmoothed)

