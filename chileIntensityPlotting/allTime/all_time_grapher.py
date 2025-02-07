from sys import argv

import matplotlib.pyplot as plt

YEAR_COLORS = {
    "2009": "black",
    "2010": "darkgray",
    "2011": "rosybrown",
    "2012": "brown",
    "2013": "red",
    "2014": "sandybrown",
    "2015": "gold",
    "2016": "darkkhaki",
    "2017": "yellow",
    "2018": "lawngreen",
    "2019": "forestgreen",
    "2020": "aquamarine",
    "2021": "teal",
    "2022": "deepskyblue",
    "2023": "purple",
    "2024": "hotpink",
}


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
    plt.figure(figsize=(20,13))
    plt.grid(visible=True, axis="both")
    title = "OH Temp Daily Averages from All Years"
    plt.title(title, fontsize=26)
    #plt.errorbar(times, temps, yerr=stdevs, fmt='o', capsize=5, ecolor="r", elinewidth=.5, label="Daily Average OH Temp")
    for i in range(len(years)):
        year = years[i]
        times = allTimes[i]
        temps = allTemps[i]
        stdevs = allStdevs[i]
        plt.scatter(times, temps, label=year, color=YEAR_COLORS[year])

    plt.set_xlabel("Day of Year", fontsize=20)
    plt.set_ylabel("OH Temp (K)", fontsize=20)

    plt.legend(fontsize=15)

    # NOTE: Assuming averagesPath is the path to ..../YEARdailyAverages.csv
    outPath = "allTime_OH_temp.png"
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


def getYearAverages(year, yearPath):
    times, temps, stdevs = readAverages(yearPath)
    return times, temps, stdevs


if __name__ == "__main__":
    years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    days = []
    temps = []
    stdevs = []

    for year in years:
        path = f"{year}/{year}dailyAverages.csv"
        newDays, newTemps, newStdevs = getYearAverages(year, path)
        days.append(newDays)
        temps.append(newTemps)
        stdevs.append(newStdevs)


    makeAndSaveGraph(years, days, temps, stdevs)

