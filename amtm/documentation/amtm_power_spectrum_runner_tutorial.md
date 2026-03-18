# Purpose of This Program
This program is a runner program for AMTM power spectrum processing and generation.

# Prerequisites
You need an environment like anaconda/spyder that has the following python libraries.
* Numpy
* Matplotlib
* Pandas

You also need IDL installed, as well as the path to the IDL folder.
It is typically installed at a path similar to `C:\Program Files\Harris\IDL89` for windows.
I think you need IDL version 8.5 or higher.

Make sure to have the following python programs in the same directory.
* `amtm_power_spectrum_runner.py`
* `power_spectrum_daily.py`

Make sure you have the following IDL `.pro` files at a known location.
They are often found in a directory similar to `C:\Users\Person\OneDrive\Desktop\MachineLearning\IDLCode`.
* `m_fft_asi.pro`
* `read_images_AMTM.pro`

# Setup
After making sure all of the prerequisites are met, open the python script `amtm_power_spectrum_runner.py` in spyder or an editor.
To use the program, you'll need to change several lines near the top of the script.
If you're unfamiliar with the `os.path.join` function, see [Appendix A](#appendix-a-ospathjoin) before editing.

## Main Settings
The following are the most important settings

### **idl_scripts_dir**
The first line you'll have to edit is the following.
```python
idl_scripts_dir = join("C:\\", "Users", "Domi", "OneDrive", "Desktop", "MachineLearning", "IDLCode")
```
This directory should contain the IDL `.pro` files described above.

### **save_dir**
The second line you'll have to edit is the following.
```python
save_dir = join("C:\\", "Gabes_stuff", "AMTM_ALOMAR")
```
This directory is the main save directory for all processing output.
It should contain year folders and winter total power plots.
In the year directories, there should be month-year directories like `October2016`, inside which there should be (at least) the `days.txt` and will contain folders corresponding to the windows.
I hope I'm not overexplaining things, but I want to make clear that this is not the main directory of the drive where the images are stored.
This is the directory where data derived from those images are stored.

### **read_dir**
The third line you'll have to edit is the following.
```python
read_dir = join("I:\\")
```
This is the main directory where the raw data images are stored at, usually the root of the drive, but sometimes there's another subdirectory of the root you have to navigate to.
This directory should contain your `months.txt` file and the month-year folders like `October2016`.

### **year**
You'll edit the following line with the year that you are looking at.
In one drive, there is typically two different years since the drive is for a winter's worth of data.
You can choose one year to process at a time.
```python
year = "2016"
```

### **days**
Finally, you'll edit the following code.
```python
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
```
This object `days` is a python dictionary with the month names as keys and a list of nights as the values.
If you have no nights in that month, you can leave the month's list empty.
If you want to do multiple nights in a month, make sure to put commas after each line (except the last one, but python is okay even if you leave the comma there).
Each of these nights should have at least one entry in the corresponding month's `days.txt` file.

## Some Options
The following are a few options that you can use, if desired. They are turned off (or `False`) by default.

### **do_all**
This involves the following code.
```python
do_all_windows = False
```
If you want to just make a power spectrum for each window, set this option to True.
It will make a power spectrum for each window in the drive's `days.txt` file for each month in the `year`, designated above.
So, to make the power spectrums for all the windows in the drive, you will have to do it twice, once for each year your drive covers.


### **skip_IDL**
This involves the following code.
```python
skip_IDL = False
```
If you have already done the IDL processing previously (so you already have the CSV files), you can skip that processing by setting this option to True.

## File Setup
The runner is expecting a variety of files in your drive where you're processing and where you're saving the data.

### **Read Directory**
The read directory should contain your raw and processed image data.
The `read_dir` variable should take you to the folder that contains the month-year folders like `October2016` or `April2020`.
These folder names should have no space between the month and year, and the month should be capitalized and spelled out.

Inside the month-year folder you should have raw data folders labelled mon-night like `Sep01-02`, `Apr09-10`, and `Aug31-01`.
These folders have the raw images and the `processed` folder that has processed images.
For nights that you want to make power spectrums for, there should be the following set of processed files in the processed folder.
* BandOH
* BandOH_caun
* TempOH
* TempOH_caun
* BG_31_ff
* P12_31_ff
* P14_31_ff

Also inside the year-month folder should be a `days.txt` file (if the month has any windows).
The `days.txt` file should look like the following example.

```
Sep
01-02 0039 0600
01-02 0670 1050
09-10 0000 0350
11-12 0004 0400
30-31 0204 1245
31-01 0001 0112
31-01 0403 1330
```
So, the format is that there should be the month stub at the top of the file and the image indexes of the windows below.
The window indexes should have a width of 4 with zeros padding the front (so '0030' instead of '30').
The date should just be the night with each day of the month taking two characters (so '01-02' instead of '1-2').

### **Save Directory**
The save directory should contain your processed csv and txt files, as well as the generated plots.
The `save_dir` variable should take you to the folder that contains the year folders like `2016` or `2020`.
Inside the year folder there should be month-year folders like `October2016` or `April2020`.
These folder names should have no space between the month and year, and the month should be capitalized and spelled out.

Inside the month-year folder you should have your `days.txt` file.
It should be identical to the corresponding file in the read directory.

Also in the month-year folder you should have a `timestamp.txt` file.
This file should contain the timestamp of the first image indexed in each window in the `days.txt` file for that month.

```
#0-year 1-month 2-day 3-hour 4-minute 5-second
#Ut time of the starting frame given and aligned for each day in days.txt
2016 11  1 16 30 22
2016 11  1 19 49 19
2016 11  5  1 19  1
2016 11  5 15 17 55
2016 11  6 15 19 32
2016 11  7 12 26 37
2016 11 17 15 15 30
2016 11  8  3 49 28
2016 11  8  5  4 28
2016 11  8 22 35 17
2016 11 20 20 30  2
```
As shown in the comments, the above numbers represent the following.
The year, month, day of month, hour, minute, second of the first image in the corresponding window.
You get that timestamp from the Norway image reader.
So that the file looks nice and organized, use the spacing shown above, where single-digit numbers are right-justified within the column.

The only thing that maps the timestamp to the window in `days.txt` is the ordering, so given the following example `days.txt` file,
```
Nov
01-02 0039 0600
01-02 0670 1050
05-06 0000 0350
...
...
```

the correspondance would be the following.
* `01-02 0039 0600` corresponds to `2016 11  1 16 30 22`
* `01-02 0670 1050` corresponds to `2016 11  2  1 49 19`
* `05-06 0000 0350` corresponds to `2016 11  6  1 19  1`
and so on.
These timestamps are used to get the timeseries data for the plots.


# Running the Program
Once you have opened the runner in your chosen environment and adjusted the required variables, you should be able to simply hit the run button to run it.
The program will constantly log what it's up to, so you should be able to track its progress.
Messages (besides error messages) that are from the runner and not the IDL code will have dashes to signify their origin (`--- message ---`).
The program will output the following sets of files in your `save_dir`.
* Inside the year then month-year folders, there will be power spectrum plots made for each window. They have the month stub, days of the month that the night involves, and the image indexes of the start and end of the window. They will look like the following.
    * `Nov30-01OH_0000-0400.jpg`
    * `Feb01-02OH_0301-1424.jpg`
* Also inside the year then month-year folders, there will be folders made for each window in your `days.txt` file. They have the month stub, days of the month that the night involves, and the image indexes of the start and end of the window. They will look like the following.
    * `Nov30-01_0000-0400`
    * `Feb01-02_0301-1424`
* Inside these folders will be several CSV files that have the various powers calculated by the FFT processing. Note that the total power processing uses the same folders, so there may be other files associated with that process. The ones that are made by this program are the following.
    * `OH_PER_.csv`
    * `OH_POW_.csv`
    * `OH_TOTAL_.csv`
    * `OH_WIN_.csv`


# Appendix A: os.path.join
## Motivation
The purpose of `join()` is to easily create a path, without having to consider your OS.
Windows typically follows the convention of using `\` to denote a directory, most other operating systems use `/`.
It also generally simplifies the combination of paths.
When given some number of paths or strings, it returns a path with directory markers put between the paths.

Consider the following example.
```python
from os.path import join

def combinePathsNoJoin(path1, path2, path3):
    return path1 + "\\" + path2 + "\\" + path3

def combinePathsWithJoin(path1, path2, path3):
    return join(path1, path2, path3)
```
Both of the defined functions do the same thing.

## Usage
In the code that I have you edit, I have you put your paths in as `join()`s.
This makes the code more cross-platform, and it ensures that the same conventions are followed throughout the program.

Take the following example.
```python
idl_scripts_dir = join("C:\\", "Users", "Domi", "OneDrive", "Desktop", "MachineLearning", "IDLCode")
```
It may seem like it would be easier to just do the following.
```python
idl_scripts_dir = "C:\\Users\\Domi\\OneDrive\\Desktop\\MachineLearning\\IDLCode"
```
However, someone may use `/` instead of `\\`, or even try `\`, which would produce errors.
These may mess with the system, so I think that it would be easier to just use `join()`.
