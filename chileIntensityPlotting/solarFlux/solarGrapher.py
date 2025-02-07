from sys import argv

import matplotlib.pyplot as plt

def readAverages(path):
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    years = []
    ohAvgs = []
    solarAvgs = []
    ohStdevs = []
    solarStdevs = []
    for line in lines:
        cols = line.split(",")
        years.append(int(cols[0]))
        ohAvgs.append(float(cols[1]))
        solarAvgs.append(float(cols[2]))
        ohStdevs.append(float(cols[3]))
        solarStdevs.append(float(cols[4]))

    file.close()
    return years, ohAvgs, solarAvgs, ohStdevs, solarStdevs


def makeAndSaveGraph(years, ohAvgs, solarAvgs, averagesPath):
    fig, ax1 = plt.subplots(figsize=(10,6))
    #plt.errorbar(times, temps, yerr=stdevs, fmt='o', capsize=5, ecolor="r", elinewidth=.5, label="Daily Average OH Temp")

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Solar Flux (SFU)")
    ax1.plot(years, solarAvgs, color="r", label="Yearly Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="r")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Temp (K)")
    ax2.errorbar(years, ohAvgs, color="b", fmt="o", ecolor="p", label="Yearly Average OH Temp")
    ax1.tick_params(axis="y", labelcolor="b")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "OH Temp Daily Averages from Year " + year
    plt.title(title, fontsize=26)

    # NOTE: Assuming averagesPath is the path to ..../all_time_year_averages.csv
    outPath = averagesPath.replace(".csv", ".png")
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_year_averages.csv"
    years, ohAvgs, solarAvgs, ohStdevs, solarStdevs = readAverages(averagesPath)

    makeAndSaveGraph(years, ohAvgs, solarAvgs, averagesPath)

