
import sys
from os.path import join


# NOTE: you may have to adjust IDL_DIR for your system
IDL_DIR = join("C:/", "Program Files", "Harris", "IDL89")
sys.path.append(f"{IDL_DIR}/lib/bridges")

from idlpy import *


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


# NOTE: the following code yields the path
# C:\Users\Domi\OneDrive\Desktop\MachineLearning\IDLCode
idl_scripts_dir = join("C:/", "Users", "Domi", "OneDrive", "Desktop", "MachineLearning", "IDLCode")

# NOTE: this should the directory where ALOMAR output data goes. It should contain your year folders, plots of the winter, etc
save_dir = join("C:/", "Gabes_stuff", "AMTM_ALOMAR")

# NOTE: this should be the main directory of the drive you're using. It should contain the month-year folders (like October2016/) and months.txt file.
read_dir = join("I:/")

year = "2016"
days = {
    "January": (
    ),
    "February": (
    ),
    "March": (
    ),
    "April": (
    ),
    "May": (
    ),
    "June": (
    ),
    "July": (
    ),
    "August": (
    ),
    "September": (
        "16-17"
    ),
    "October": (
    ),
    "November": (
        "07-08",
        "08-09"
    ),
    "December": (
    )
}

# NOTE: we can get a list of the months from list(days.keys())

IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
IDL.run(f".compile {join(idl_scripts_dir, READ_IMAGE_FILENAME)}")
IDL.run(f".compile {join(idl_scripts_dir, SHELLRUNNER_FILENAME)}")
IDL.run("MLSHELLRUNNERTEST")

# TODO: Change this code to read the days.txt window files and parse them. Specify the read and save folders. Pass them to shellrunner

