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
    return


if __name__ == "__main__":
    if len(argv) == 1:
        print("USAGE: python[3] grapher.py path_to/[year]dailyAverages.csv")
        exit()
    averagesPath = argv[1]
    times, temps, stdevs = readAverages(averagesPath)
    year = getYear(averagesPath)
    print(year)
    print(times)
    print(temps)
    print(stdevs)
    makeAndSaveGraph(year, times, temps, stdevs)
