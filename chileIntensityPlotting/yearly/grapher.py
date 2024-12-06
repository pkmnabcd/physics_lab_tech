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

def getYear(file_path: str):
    last_slash_index = -1
    for i in range(len(file_path)):
        if file_path[i] == '/':
            last_slash_index = i

    filename = file_path[last_slash_index + 1:]
    year = filename[0:4]
    return year


def makeAndSaveGraph(year, times, temps, stdevs):
    plt.figure(figsize=(15,8))
    plt.errorbar(times, temps, yerr=stdevs, fmt='o', capsize=5, ecolor="r", elinewidth=.5, label="Daily Average OH Temp")
    plt.grid(visible=True, axis="both")

    title = "OH Temp Daily Averages from Year " + year
    plt.title(title, fontsize=26)

    plt.show()


if __name__ == "__main__":
    if len(argv) == 1:
        print("USAGE: python[3] grapher.py path_to/[year]dailyAverages.csv")
        exit()
    averagesPath = argv[1]
    times, temps, stdevs = readAverages(averagesPath)
    year = getYear(averagesPath)
    makeAndSaveGraph(year, times, temps, stdevs)
