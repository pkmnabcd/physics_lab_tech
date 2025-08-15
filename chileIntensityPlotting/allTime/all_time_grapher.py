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
        temps.append(float(cols[2]))
        stdevs.append(float(cols[3]))

    file.close()
    return times, temps, stdevs


def makeAndSaveGraph(times, temps, stdevs):
    plt.figure(figsize=(14,10))
    plt.grid(visible=True, axis="both")

    plt.xlabel("Year", fontsize=22)
    plt.ylabel("OH Temp (K)", fontsize=22)
    plt.plot(times, temps, color="blue", label="Daily Average OH Temp")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "2009-2024 OH Temp Daily Averages"
    plt.title(title, fontsize=26)

    plt.legend(fontsize=20)
    fig.tight_layout()

    # NOTE: Assuming averagesPath is the path to ..../YEARdailyAverages.csv
    outPath = "all_time_oh_daily_average.png"
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
        for day in newDays:
            # NOTE: Assuming day is day of year number
            days.append(year + (day / 366))
        for temp in newTemps:
            temps.append(temp)
        for stdev in newStdevs:
            stdevs.append(stdev)


    makeAndSaveGraph(years, days, temps, stdevs)

