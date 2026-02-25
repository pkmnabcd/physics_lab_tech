
import sys
from os.path import join


# NOTE: you may have to adjust IDL_DIR for your system
IDL_DIR = join("C:/", "Program Files", "Harris", "IDL89")
sys.path.append(f"{IDL_DIR}/lib/bridges")

from idlpy import *



# NOTE: the following code yields the path
# C:\Users\Domi\OneDrive\Desktop\MachineLearning\IDLCode
idl_scripts_dir = join("C:/", "Users", "Domi", "OneDrive", "Desktop", "MachineLearning", "IDLCode")

# NOTE: this should the directory where ALOMAR output data goes. It should contain your year folders, plots of the winter, etc
save_dir = join("C:/", "Gabes_stuff", "AMTM_ALOMAR")

# NOTE: this should be the main directory of the drive you're using. It should contain the month-year folders (like October2016/) and months.txt file.
read_dir = join("I:/")

# NOTE: this is the year you're making power spectrums for.
year = "2016"

# NOTE: Put the nights you want inside the tuples like
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


FFT_FILENAME = "m_fft_asi.pro"
READ_IMAGE_FILENAME = "read_images_ALOMAR.pro"
SHELLRUNNER_FILENAME = "mlshellrunnertest.pro"


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



def readDaysTxt(year, month, day, main_path):
    read_path = join(main_path, year, f"{month}{year}", "days.txt")
    split_lines = []
    with open(read_path) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0: # The first line should be the month stub
                continue
            line = lines[i]
            line = line.strip("\n\r")
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split()
            if len(parts) != 3:
                print(f"WARNING! parts has a length of {len(parts)} instead of 3.")
            split_lines.append(parts)

    begin_ends = []
    for line in split_lines:
        if line[0] == day:
            begin_ends.append((int(line[1]), int(line[2])))
    return begin_ends


months = list(days.keys())

IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")
#IDL.run(f".compile {join(idl_scripts_dir, SHELLRUNNER_FILENAME)}")
#IDL.run("MLSHELLRUNNERTEST")

print(f"--- Generating power spectrums for {year} ---")
for month in months:
    print(f"--- Looking for days in month: {month} ---")
    days_list = days[month]
    for day in days_list:
        month_stub = MONTH_STUBS[month]
        print(f"--- Making power spectrum for {month_stub}{day} ---")

        begin_ends = readDaysTxt(year, month, day, save_dir)
        for begin_end in begin_ends:
            begin = begin_end[0]
            end = begin_end[1]

            # Prepares the strings needed by read_images
            source_path = join(read_dir, f"{month}{year}")
            day_string = join(f"{month_stub}{day}", "")
            end_path = join(save_dir, year, f"{month}{year}", f"{month_stub}{day}_{begin:04d}-{end:04d}")
            begin_str = str(begin)
            end_str = str(end)

            # Create csv files using the IDL code in read_images
            IDL.run(f"read_images({day_string}, {source_path}, {begin_str}, {end_str}, {end_path})")

# NOTE: The read_images function is expecting the following parameters
# dateString: something like "Nov07-08/"
# sourcePath: the path to the MonthYear folder in the drive eg "I:/November2016/"
# begins: a string of the start index number. Just the shortest form of a number like "0" not "0000".
# ends: same as begins but the end index.
# endDir: path to the save folder of the outputted csv files. eg "C:/Gabes_stuff/AMTM_ALOMAR/2016/November2016/Nov07-08_0000-0779"

