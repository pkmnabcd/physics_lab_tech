from sys import argv

import matplotlib.pyplot as plt

def readAverages(path):
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    yearmonths = []  # this is the year and then some multiple of 1/12 to be the month
    solarAvgs = []
    solarStdevs = []
    for line in lines:
        cols = line.split(",")

        yearmonth = int(cols[0])
        month = int(cols[1]) - 1
        yearmonth += (1/12) * month

        solarAvgs.append(float(cols[2]))
        solarStdevs.append(float(cols[3]))
        yearmonths.append(yearmonth)

    file.close()
    return yearmonths, solarAvgs, solarStdevs


def makeAndSaveGraph(yearmonths, solarAvgs, averagesPath):
    fig, ax1 = plt.subplots(figsize=(14,10))

    ax1.set_xlabel("Year", fontsize=20)
    ax1.set_ylabel("Solar Flux (SFU)", fontsize=20)
    ax1.plot(yearmonths, solarAvgs, color="red", label="Monthly Average Solar Flux")
    ax1.tick_params(axis="y", labelcolor="red")

    fig.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "Monthly Solar Flux from 1979 to 2009"
    plt.title(title, fontsize=26)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="lower right")
    plt.tight_layout()

    # NOTE: Assuming averagesPath is the path to ..../all_time_year_averages.csv
    outPath = averagesPath.replace(".csv", ".png")
    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "30_years_past_sf_month_averages.csv"
    yearmonths, solarAvgs, solarStdevs = readAverages(averagesPath)

    makeAndSaveGraph(sfYearmonths, solarAvgs, averagesPath)

