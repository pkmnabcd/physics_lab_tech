import sys
from os.path import join, exists

from power_spectrum_daily import makeWindowPowerSpectrum
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

# NOTE: this is the year you're making power spectrums for.
year = "2016"

# NOTE: If you want to make a power spectrum for each window in all
# the days.txt files in that year's part of the drive, set the following as true
# If you do so, you don't need to modify the days dict below. It will be wiped
do_all_windows = False

# NOTE: If you want to skip the IDL code because it has already
# done, and you just want new plots, set the following as true
skip_IDL = False

# NOTE: Put the nights you want inside the lists like
# "January": (
#    "01-02",
#    "05-06"
# ),
days = {
    "January": [
    ],
    "February": [
    ],
    "March": [
    ],
    "April": [
    ],
    "May": [
    ],
    "June": [
    ],
    "July": [
    ],
    "August": [
    ],
    "September": [
        "16-17"
    ],
    "October": [
    ],
    "November": [
        "07-08",
        "08-09"
    ],
    "December": [
    ]
}


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


FFT_FILENAME = "m_fft_amtm.pro"
READ_IMAGE_FILENAME = "read_images_AMTM.pro"


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


def checkGivenPaths():
    if not exists(IDL_DIR):
        print(f"WARNING!! The given IDL_DIR: {IDL_DIR} does not exist!")
        exit()
    if not exists(idl_scripts_dir):
        print(f"WARNING!! The given idl_scripts_dir: {idl_scripts_dir} does not exist!")
        exit()
    if not exists(save_dir):
        print(f"WARNING!! The given save_dir: {save_dir} does not exist!")
        exit()
    if not exists(read_dir):
        print(f"WARNING!! The given read_dir: {read_dir} does not exist!")
        exit()


def getAllWindows(year, read_path):
    # Clear the days dict since we'll be filling it with new ones
    for key in days:
        days[key] = []

    for month in MONTHS:
        days_txt_days = readDaysTxtAllDays(year, month, read_path)
        for day in days_txt_days:
            days[month] = days_txt_days


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
# way.
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

if __name__ == "__main__":
    checkGivenPaths()

    IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
    IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")

    if do_all_windows:
        print(f"--- Getting power spectrums for all windows in year {year} on the drive ---")
        # NOTE: wipe and add all nights in days.txt files into days dict.
        getAllWindows(year, read_dir)

    print(f"--- Generating power spectrums for {year} ---")
    for month in MONTHS:
        print(f"--- Looking for days in month: {month} ---")
        days_list = days[month]
        for day in days_list:
            month_stub = MONTH_STUBS[month]
            print(f"--- Making power spectrum for {month_stub}{day} ---")

            begin_ends = readDaysTxtOneDay(year, month, day, save_dir)
            for begin_end in begin_ends:  # Iterating over each window for the day
                begin = begin_end[0]
                end = begin_end[1]
                print(f"--- {month_stub}{day} frame: [{begin:04d},{end:04d}]")

                # Prepares the strings needed by read_images
                source_path = join(read_dir, f"{month}{year}", "")
                day_string = join(f"{month_stub}{day}", "")
                end_path = join(save_dir, year, f"{month}{year}", f"{month_stub}{day}_{begin:04d}-{end:04d}", "")
                begin_str = str(begin)
                end_str = str(end)

                # Create csv files using the IDL code in read_images
                if not skip_IDL:
                    MAX_ATTEMPTS = 5
                    attempt = 0
                    while attempt < MAX_ATTEMPTS:
                        try:
                            IDL.read_images(dateString=day_string, sourcePath=source_path, begins=begin_str, ends=end_str, endDir=end_path)
                            attempt = MAX_ATTEMPTS # Break out of the loop
                        except IDLError as e:
                            attempt += 1
                            print(f"Encountered the following IDL Error: {e}\nRestarting IDL and will attempt {MAX_ATTEMPTS-attempt} more times. If it's a memory problem and it persists, restart your computer and try again.")
                            IDL.run(".FULL_RESET_SESSION")
                            IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
                            IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")
                    print("FFT processing finished. Starting to generate the power spectrum plot")
                else:
                    print("Skipping FFT processing. Starting to generate the power spectrum plot")
                makeWindowPowerSpectrum(year, month, month_stub, day, f"{begin:04d}", f"{end:04d}", save_dir)

