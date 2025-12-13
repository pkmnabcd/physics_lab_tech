import matplotlib.pyplot as plt

def getYeardoy(year, month, dayOfMonth):
    """
    Returns the corresponding yeardoy which is the [year].(doy / # days in year)
    """

    isLeapYear = year % 4 == 0
    daysInYear = 365
    if isLeapYear:
        daysInYear = 366

    dayOfYearAdd = 0

    if month == 1:
        dayOfYearAdd = 0
    elif month == 2:
        dayOfYearAdd = 31
    elif month == 3:
        if isLeapYear:
            dayOfYearAdd = 60
        else:
            dayOfYearAdd = 59
    elif month == 4:
        if isLeapYear:
            dayOfYearAdd = 91
        else:
            dayOfYearAdd = 90
    elif month == 5:
        if isLeapYear:
            dayOfYearAdd = 121
        else:
            dayOfYearAdd = 120
    elif month == 6:
        if isLeapYear:
            dayOfYearAdd = 152
        else:
            dayOfYearAdd = 151
    elif month == 7:
        if isLeapYear:
            dayOfYearAdd = 182
        else:
            dayOfYearAdd = 181
    elif month == 8:
        if isLeapYear:
            dayOfYearAdd = 213
        else:
            dayOfYearAdd = 212
    elif month == 9:
        if isLeapYear:
            dayOfYearAdd = 244
        else:
            dayOfYearAdd = 243
    elif month == 10:
        if isLeapYear:
            dayOfYearAdd = 274
        else:
            dayOfYearAdd = 273
    elif month == 11:
        if isLeapYear:
            dayOfYearAdd = 305
        else:
            dayOfYearAdd = 304
    elif month == 12:
        if isLeapYear:
            dayOfYearAdd = 335
        else:
            dayOfYearAdd = 334
    else:
        print("WARNING!! The month may not be correct")

    dayOfYear = dayOfYearAdd + dayOfMonth
    return year + dayOfYear / daysInYear


def readAverages(path):
    file = open(path)
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
    file.close()

    sfYeardoys = []  # this is the year and then some multiple of 1/365 1/366 to be the day of year
    sfAvgs = []
    for line in lines:
        cols = line.split(",")

        year = int(cols[0])
        month = int(cols[1])
        day = int(cols[2])
        sfAvg = float(cols[3])

        sfYeardoys.append(getYeardoy(year, month, day))
        sfAvgs.append(sfAvg)

    return sfYeardoys, sfAvgs


def makeAndSaveGraph(times, temps, outPath):
    plt.figure(figsize=(14,10))
    plt.grid(visible=True, axis="both")

    plt.xlabel("Year", fontsize=22)
    plt.ylabel("Solar Flux (SFU)", fontsize=22)
    plt.plot(times, temps, color="blue", label="Daily Average Solar Flux")
    plt.tick_params(axis="both", labelsize=20)

    plt.tight_layout()
    plt.grid(visible=True, axis="both")

    title = "2009-2024 Solar Flux Daily Averages"
    plt.title(title, fontsize=26)

    plt.legend(fontsize=20)
    plt.tight_layout()

    plt.savefig(outPath)
    print(f"File saved to {outPath} .")


if __name__ == "__main__":
    averagesPath = "all_time_sf_daily_averages.csv"
    outPath = "all_time_sf_daily_average.png"
    sfYeardoys, sfAvgs = readAverages(averagesPath)

    makeAndSaveGraph(sfYeardoys, sfAvgs, outPath)

