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


def splitMonths(yearmonths, avgs, stdevs):
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
            apr[2].append(stdevs[i])
        elif isclose(remainder, mayRemainder):
            may[0].append(year)
            may[1].append(avgs[i])
            may[2].append(stdevs[i])
        elif isclose(remainder, junRemainder):
            jun[0].append(year)
            jun[1].append(avgs[i])
            jun[2].append(stdevs[i])
        elif isclose(remainder, julRemainder):
            jul[0].append(year)
            jul[1].append(avgs[i])
            jul[2].append(stdevs[i])
        elif isclose(remainder, augRemainder):
            aug[0].append(year)
            aug[1].append(avgs[i])
            aug[2].append(stdevs[i])
        elif isclose(remainder, sepRemainder):
            sep[0].append(year)
            sep[1].append(avgs[i])
            sep[2].append(stdevs[i])

    monthDict["apr"] = apr
    monthDict["may"] = may
    monthDict["jun"] = jun
    monthDict["jul"] = jul
    monthDict["aug"] = aug
    monthDict["sep"] = sep
    return monthDict


# TODO: Add OH stdev to graph
def makeAndSaveGraph(ohYears, ohAvgs, ohStdevs, sfYears, sfAvgs, sfStdevs, month):
    fig, ax1 = plt.subplots(figsize=(8,7))

    ax1.set_xlabel("Year", fontsize=20)
    ax1.set_ylabel("Solar Flux (SFU)", fontsize=20)
    ax1.plot(sfYears, sfAvgs, color="red", label="Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Temp (K)", fontsize=20)
    ax2.plot(ohYears, ohAvgs, color="blue", label="Average OH Temp")
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM 2009-2024 Average OH Temp and Solar Flux in " + month
    title = "\n".join(wrap(title, 40))
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    plt.tight_layout()

    outPath = "all_time_oh_sf_average_" + month + ".png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_month_averages.csv"
    ohYearmonths, sfYearmonths, ohAvgs, sfAvgs, ohStdevs, sfStdevs = readAverages(averagesPath)
    ohMonthDict = splitMonths(ohYearmonths, ohAvgs, ohStdevs)
    sfMonthDict = splitMonths(sfYearmonths, sfAvgs, sfStdevs)

    makeAndSaveGraph(ohMonthDict["apr"][0], ohMonthDict["apr"][1], ohMonthDict["apr"][2], sfMonthDict["apr"][0], sfMonthDict["apr"][1], sfMonthDict["apr"][2], "April")
    makeAndSaveGraph(ohMonthDict["may"][0], ohMonthDict["may"][1], ohMonthDict["may"][2], sfMonthDict["may"][0], sfMonthDict["may"][1], sfMonthDict["may"][2], "May")
    makeAndSaveGraph(ohMonthDict["jun"][0], ohMonthDict["jun"][1], ohMonthDict["jun"][2], sfMonthDict["jun"][0], sfMonthDict["jun"][1], sfMonthDict["jun"][2], "June")
    makeAndSaveGraph(ohMonthDict["jul"][0], ohMonthDict["jul"][1], ohMonthDict["jul"][2], sfMonthDict["jul"][0], sfMonthDict["jul"][1], sfMonthDict["jul"][2], "July")
    makeAndSaveGraph(ohMonthDict["aug"][0], ohMonthDict["aug"][1], ohMonthDict["aug"][2], sfMonthDict["aug"][0], sfMonthDict["aug"][1], sfMonthDict["aug"][2], "August")
    makeAndSaveGraph(ohMonthDict["sep"][0], ohMonthDict["sep"][1], ohMonthDict["sep"][2], sfMonthDict["sep"][0], sfMonthDict["sep"][1], sfMonthDict["sep"][2], "September")

