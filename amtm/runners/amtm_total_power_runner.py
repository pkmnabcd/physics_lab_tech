import sys
from os.path import join, exists

from calculate_tot_powr import calcWindowTotalPowerOverTime
from total_power_graphing_monthly import makeMonthlyPlot
from total_power_graphing_winter import makeWinterPlot
# NOTE: power_spectrum_daily.py should be in the same directory as this python program


# NOTE: you may have to adjust IDL_DIR for your system
IDL_DIR = join("C:\\", "Program Files", "Harris", "IDL89")
sys.path.append(f"{IDL_DIR}/lib/bridges")

from idlpy import IDL, IDLError




# NOTE: Begin editing here!!!!!!!
# NOTE: Begin editing here!!!!!!!
# NOTE: Begin editing here!!!!!!!
# NOTE: Begin editing here!!!!!!!
# NOTE: Begin editing here!!!!!!!


# NOTE: the following code yields the path
# C:\Users\Domi\OneDrive\Desktop\MachineLearning\IDLCode
idl_scripts_dir = join("C:\\", "Users", "Domi", "OneDrive", "Desktop", "AMTM", "IDLCode")

# NOTE: this should the directory where ALOMAR output data goes.
# It should contain your year folders, plots of the winter, etc.
# This is where the output CSV files go.
save_dir = join("C:\\", "Gabes_stuff", "AMTM_ALOMAR")

# NOTE: this should be the main directory of the drive you're using.
# It should contain the month-year folders (like October2016/) and months.txt file.
read_dir = join("I:\\")

# NOTE: this is the years in your winter
year1 = "2016"
year2 = "2017"

# NOTE: If you want to skip the IDL code or total power caculation because
# it has already done, and you just want new plots, set the following as true
skip_processing = False



# NOTE: YOU SHOULD NOT EDIT ANYTHING AFTER THIS
# NOTE: YOU SHOULD NOT EDIT ANYTHING AFTER THIS
# NOTE: YOU SHOULD NOT EDIT ANYTHING AFTER THIS
# NOTE: YOU SHOULD NOT EDIT ANYTHING AFTER THIS
# --
# --
# --
# --
# --
# --
# --
# --
# --


FFT_FILENAME = "m_fft_amtm_loop.pro"
READ_IMAGE_FILENAME = "read_images_AMTM_total_power.pro"


MONTH_STUBS = {
    "January": "Jan",
    "February": "Feb",
    "March": "Mar",
    "April": "Apr",
    "May": "May",
    "June": "Jun",
    "July": "Jul",
    "August": "Aug",
    "September": "Sep",
    "October": "Oct",
    "November": "Nov",
    "December": "Dec"
}
MONTHS = list(MONTH_STUBS.keys())


def getAllWindows(year, read_path):
    days = {}
    for month in MONTHS:
        days_txt_days = readDaysTxtAllDays(year, month, read_path)
        days[month] = days_txt_days
    return days


def readDaysTxtAllDays(year, month, main_path):
    read_path = join(main_path, f"{month}{year}", "days.txt")
    if not exists(read_path): # Skip files that don't exist
        return []
    split_lines = []
    with open(read_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            line = line.strip("\n\r")
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split()
            if i == 0: # The first line should be the month stub
                if len(parts) != 1:
                    print("WARNING! The first line should be the month stub like Nov or Apr. Make sure days.txt is formatted correctly.")
                continue
            if len(parts) != 3:
                print(f"WARNING! parts has a length of {len(parts)} instead of 3. Make sure days.txt is formatted correctly.")
            split_lines.append(parts)

    days_list = []
    for line in split_lines:
        if line[0] not in days_list:
            days_list.append(line[0])
    return days_list


# NOTE: I know it's a bit inefficient that I'm reading the days.txt files
# twice, but it won't add too much time and it was easier to write it this
# way since I started with the power spectrum runner first.
def readDaysTxtOneDay(year, month, day, main_path):
    read_path = join(main_path, year, f"{month}{year}", "days.txt")
    split_lines = []
    with open(read_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            line = line.strip("\n\r")
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split()
            if i == 0: # The first line should be the month stub
                if len(parts) != 1:
                    print("WARNING! The first line should be the month stub like Nov or Apr. Make sure days.txt is formatted correctly.")
                continue
            if len(parts) != 3:
                print(f"WARNING! parts has a length of {len(parts)} instead of 3. Make sure days.txt is formatted correctly.")
            split_lines.append(parts)

    begin_ends = []
    for line in split_lines:
        if line[0] == day:
            begin_ends.append((int(line[1]), int(line[2])))
    return begin_ends


def doIDLAndTotPowrProcessingOneYear(year, days):
    print(f"--- Getting total power for all windows in year {year} on the drive ---")
    print(f"--- Generating total power for {year} ---")
    for month in MONTHS:
        print(f"--- Looking for days in month: {month} ---")
        days_list = days[month]
        for day in days_list:
            month_stub = MONTH_STUBS[month]
            print(f"--- Making total power for {month_stub}{day} ---")

            begin_ends = readDaysTxtOneDay(year, month, day, save_dir)
            for begin_end in begin_ends:  # Iterating over each window for the day
                begin = begin_end[0]
                end = begin_end[1]
                print(f"--- {month_stub}{day} frame: [{begin:04d},{end:04d}] ---")

                # Prepares the strings needed by read_images
                source_path = join(read_dir, f"{month}{year}", "")
                day_string = f"{month_stub}{day}"
                end_path = join(save_dir, year, f"{month}{year}", f"{month_stub}{day}_{begin:04d}-{end:04d}")

                MAX_ATTEMPTS = 5
                attempt = 0
                while attempt < MAX_ATTEMPTS:
                    try:
                        IDL.read_images(dateString=day_string, sourcePath=source_path, begins=begin, ends=end, endDir=end_path)
                        attempt = MAX_ATTEMPTS # Break out of the loop
                    except IDLError as e:
                        attempt += 1
                        print(f"Encountered the following IDL Error: {e}\nRestarting IDL and will attempt {MAX_ATTEMPTS-attempt} more times. If it's a memory problem and it persists, restart your computer and try again.")
                        IDL.run(".FULL_RESET_SESSION")
                        IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
                        IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")
                calcWindowTotalPowerOverTime(year, month, month_stub, day, f"{begin:04d}", f"{end:04d}", save_dir)
                print(f"--- FFT and total power processing finished for {year} {month_stub}{day} frame: [{begin:04d},{end:04d}] ---")


def getMonthsInYear(days):
    valid_months = []
    valid_mons = []
    for month in MONTHS:
        if len(days[month]) > 0:
            valid_months.append(month)
    for month in valid_months:
        valid_mons.append(MONTH_STUBS[month])
    return valid_months, valid_mons


def getDaysTxtData(days_path):
    split_lines = []
    with open(days_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            line = line.strip("\n\r")
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split()
            if i == 0: # The first line should be the month stub
                if len(parts) != 1:
                    print("WARNING! The first line should be the month stub like Nov or Apr. Make sure days.txt is formatted correctly.")
                continue
            if len(parts) != 3:
                print(f"WARNING! parts has a length of {len(parts)} instead of 3. Make sure days.txt is formatted correctly.")
            split_lines.append(parts)

    data = []
    for line in split_lines:
        data.append((line[0], line[1], line[2]))
    return data


def daysTxtAreSame(year):
    areSame = True
    for month in MONTHS:
        days_read_path = join(read_dir, f"{month}{year}", "days.txt")
        days_save_path = join(save_dir, year, f"{month}{year}", "days.txt")
        days_read_exists = exists(days_read_path)
        days_save_exists = exists(days_save_path)
        if not days_read_exists and not days_save_exists:
            continue
        # There should be a days.txt file in the save if there's one on the drive
        elif (days_read_exists and not days_save_exists):
            print(f"WARNING!!! Only one of the following days.txt files exists:\n\t{days_read_path}\n\t{days_save_path}")
            areSame = False
            continue
        elif (not days_read_exists and days_save_exists):
            continue # save may have months not present in read drive

        days_read = getDaysTxtData(days_read_path)
        days_save = getDaysTxtData(days_save_path)
        if len(days_read) != len(days_save):
            print(f"WARNING!!! the days.txt data are not the same length at the following two paths!\n\t{days_read_path}\n\t{days_save_path}")
            areSame = False
            continue
        for i in range(len(days_read)):
            for j in range(3): # 3 is length of inner tuples
                if days_read[i][j] != days_save[i][j]:
                    print(f"WARNING!!! the days.txt data do not share the same data at the following two paths!\n\t{days_read_path}\n\t{days_save_path}")
                    areSame = False
    return areSame

if __name__ == "__main__":
    IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
    IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")

    print(f"--- Finding all nights for the {year1}-{year2} winter ---")
    days1 = getAllWindows(year1, read_dir)
    months1, mons1 = getMonthsInYear(days1)
    days2 = getAllWindows(year2, read_dir)
    months2, mons2 = getMonthsInYear(days2)

    # TODO: make function that checks to make sure that the days.txt file from the drive and save folders match
    print("--- Checking to make sure the days.txt in the read dir and save dir are the same ---")
    if not daysTxtAreSame(year1) or not daysTxtAreSame(year2):
        print("--- Exiting because some days.txt files are not the same ---")
        sys.exit()
    print("--- Check passed ---")

    if skip_processing:
        print("--- Skipping FFT and total power processing. ---")
    else:
        doIDLAndTotPowrProcessingOneYear(year1, days1)
        doIDLAndTotPowrProcessingOneYear(year2, days2)
    print("--- Generating Plots ---")

    # Making monthly plots for year 1
    for i in range(len(months1)):
        month = months1[i]
        mon = mons1[i]
        print(f"--- Making montly plot for {month} {year1} ---")
        makeMonthlyPlot(year1, month, mon, save_dir)

    # Making monthly plots for year 2
    for i in range(len(months2)):
        month = months2[i]
        mon = mons2[i]
        print(f"--- Making montly plot for {month} {year2} ---")
        makeMonthlyPlot(year2, month, mon, save_dir)

    print(f"--- Making winter plot for the {year1}-{year2} winter ---")
    makeWinterPlot(year1, year2, months1, months2, mons1, mons2, save_dir)
