from sys import argv

import matplotlib.pyplot as plt

def readAverages(path):
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    times = []
    temps = []
    stdevs = []
    for line in lines:
        cols = line.split(",")
        times.append(int(cols[0]))
        temps.append(float(cols[1]))
        stdevs.append(float(cols[2]))

    file.close()
    return times, temps, stdevs


def makeAndSaveGraph(years, allTimes, allTemps, allStdevs):
    plt.figure(figsize=(15,8))
    plt.grid(visible=True, axis="both")
    title = "OH Temp Daily Averages from All Years"
    plt.title(title, fontsize=26)
    #plt.errorbar(times, temps, yerr=stdevs, fmt='o', capsize=5, ecolor="r", elinewidth=.5, label="Daily Average OH Temp")
    for i in range(len(years)):
        year = years[i]
        times = allTimes[i]
        temps = allTemps[i]
        stdevs = allStdevs[i]
        plt.scatter(times, temps, label=year)

    # NOTE: Assuming averagesPath is the path to ..../YEARdailyAverages.csv
    plt.legend(fontsize=15)
    outPath = "allTime_OH_temp.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


def getYearAverages(year, yearPath):
    times, temps, stdevs = readAverages(yearPath)
    return times, temps, stdevs


if __name__ == "__main__":
    #years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    years = ["2020", "2021"]
    days = []
    temps = []
    stdevs = []

    for year in years:
        path = f"{year}/{year}dailyAverages.csv"
        newDays, newTemps, newStdevs = getYearAverages(year, path)
        days.append(newDays)
        temps.append(newTemps)
        stdevs.append(newStdevs)

    print(days)
    print(temps)
    print(stdevs)

    makeAndSaveGraph(years, days, temps, stdevs)

