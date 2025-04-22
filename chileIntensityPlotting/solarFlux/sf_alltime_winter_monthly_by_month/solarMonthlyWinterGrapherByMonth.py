from sys import argv
from math import floor, isclose
from textwrap import wrap

import matplotlib.pyplot as plt

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


def splitMonths(yearmonths, avgs):
    monthDict = dict()
    # TODO: Add code to split the data by month.
    # So each month (apr to sep) will have its average value from every year (with a couple exceptions for OH)
    # NOTE: first list is the list of years, second is the corresponding monthly average
    apr = [[],[]]
    aprRemainder = 3/12
    may = [[],[]]
    mayRemainder = 4/12
    jun = [[],[]]
    junRemainder = 5/12
    jul = [[],[]]
    julRemainder = 6/12
    aug = [[],[]]
    augRemainder = 7/12
    sep = [[],[]]
    sepRemainder = 8/12

    for i in range(len(yearmonths)):
        year = floor(yearmonths[i])
        remainder = yearmonths[i] - year

        if isclose(remainder, aprRemainder):
            apr[0].append(year)
            apr[1].append(avgs[i])
        elif isclose(remainder, mayRemainder):
            may[0].append(year)
            may[1].append(avgs[i])
        elif isclose(remainder, junRemainder):
            jun[0].append(year)
            jun[1].append(avgs[i])
        elif isclose(remainder, julRemainder):
            jul[0].append(year)
            jul[1].append(avgs[i])
        elif isclose(remainder, augRemainder):
            aug[0].append(year)
            aug[1].append(avgs[i])
        elif isclose(remainder, sepRemainder):
            sep[0].append(year)
            sep[1].append(avgs[i])

    monthDict["apr"] = apr
    monthDict["may"] = may
    monthDict["jun"] = jun
    monthDict["jul"] = jul
    monthDict["aug"] = aug
    monthDict["sep"] = sep
    return monthDict


def getMonthFromKey(key):
    if key == "apr":
        return "April"
    if key == "may":
        return "May"
    if key == "jun":
        return "June"
    if key == "jul":
        return "July"
    if key == "aug":
        return "August"
    if key == "sep":
        return "September"


def makeAndSaveGraph(ohDict, sfDict):
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Month", fontsize=20)
    ax1.set_ylabel("Solar Flux (SFU)", fontsize=20)

    dictKeys = ["apr", "may", "jun", "jul", "aug", "sep"]

    sfXData = []
    sfYData = []
    ohXData = []
    ohYData = []
    for key in dictKeys:
        sfAvgsForMonth = sfDict[key][1]
        ohAvgsForMonth = ohDict[key][1]

        for _ in range(len(sfAvgsForMonth)):
            sfXData.append(getMonthFromKey(key))
        for val in sfAvgsForMonth:  # For each year's value in the month
            sfYData.append(val)
        for _ in range(len(ohAvgsForMonth)):
            ohXData.append(getMonthFromKey(key))
        for val in ohAvgsForMonth:
            ohYData.append(val)

    ax1.scatter(sfXData, sfYData, color="red", label="Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Temp (K)", fontsize=20)
    ax2.scatter(ohXData, ohYData, color="blue", alpha=0.60, label="Average OH Temp")
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM 2009-2024 Monthly Average OH Temp and Solar Flux By Month"
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    plt.tight_layout()

    outPath = "all_time_oh_sf_average_by_month.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, solarStdevs = readAverages(averagesPath)
    ohMonthDict = splitMonths(ohYearmonths, ohAvgs)
    sfMonthDict = splitMonths(sfYearmonths, sfAvgs)

    makeAndSaveGraph(ohMonthDict, sfMonthDict)

