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


def makeAndSaveGraph(years, ohAvgs, solarAvgs, ohStdevs, averagesPath):
    fig, ax1 = plt.subplots(figsize=(14,10))
    #plt.errorbar(times, temps, yerr=stdevs, fmt='o', capsize=5, ecolor="r", elinewidth=.5, label="Daily Average OH Temp")

    ax1.set_xlabel("Year", fontsize=20)
    ax1.set_ylabel("Solar Flux (SFU)", fontsize=20)
    ax1.plot(years, solarAvgs, color="red", label="Yearly Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("OH Temp (K)", fontsize=20)
    ax2.errorbar(years, ohAvgs, yerr=ohStdevs, color="blue", fmt="o", ecolor="purple", label="Yearly Average OH Temp")
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "ChileMTM All-Time (2009-2024) Yearly OH Temp and Solar Flux"
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    plt.tight_layout()

    # NOTE: Assuming averagesPath is the path to ..../all_time_year_averages.csv
    outPath = averagesPath.replace(".csv", ".png")
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_oh_sf_year_averages.csv"
    years, ohAvgs, solarAvgs, ohStdevs, solarStdevs = readAverages(averagesPath)

    makeAndSaveGraph(years, ohAvgs, solarAvgs, ohStdevs, averagesPath)

