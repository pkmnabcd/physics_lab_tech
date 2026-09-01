# Purpose of This Program
This program is a runner program for AMTM total power processing and generation.
It will generate the total power data and plots for an entire winter of data.

# Prerequisites
You need an environment like anaconda/spyder that has the following python libraries.
* Numpy
* Matplotlib
* Pandas

You also need IDL installed, as well as the path to the IDL folder.
It is typically installed at a path similar to `C:\Program Files\Harris\IDL89` for windows.
I think you need IDL version 8.5 or higher.

Make sure to have the following python programs in the same directory.
* `amtm_total_power_runner.py`
* `calculate_tot_powr.py`
* `total_power_graphing_monthly.py`
* `total_power_graphing_winter.py`

Make sure you have the following IDL `.pro` files at a known location.
They are often found in a directory similar to `C:\Users\Person\OneDrive\Desktop\MachineLearning\IDLCode`.
* `m_fft_amtm_loop.pro`
* `read_images_AMTM_total_power.pro`

# Setup
After making sure all of the prerequisites are met, open the python script `amtm_total_power_runner.py` in spyder or an editor.
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

### **winter_over_2_years**
This corresponds to the following line.
```python
winter_over_2_years = True
```
This variable should be `True` if the winter your drive's data covers takes place over two years.
For example, ALOMAR AMTM data often takes place from August to April.
However, if your winter takes place in a single year, like as in the south pole, make this variable `False`.

### **year1 and year2**
You'll edit the following line with the years that you are looking at.
In one drive, there is typically two different years since the drive is for a winter's worth of data.
Put the earlier year as `year1` and the later year as `year2`.
```python
winter_over_2_years = True
year1 = "2016"
year2 = "2017"
```
If your drive has all its data in one year (like in the south pole), only change `year1`.
The value of `year2` will be ignored.
```python
winter_over_2_years = False
year1 = "2016"
year2 = "Literally Doesn't matter"
```

## Some Options
The following are a few options that you can use, if desired.

### **p12_img_stub**
For each drive you use, check the filenames, and put whatever comes before the numbers and `.tif` in the `p12_img_stub`.
From my experience, ALOMAR often has 'P12_31_XXXX.tif', while McMurdo has 'P12_1_XXXX.tif'.
```python
p12_img_stub = "P12_31_"
#p12_img_stub = "P12_1_"
```

### **do_all_windows**
Normally when you run the program, you will set this to `True` in order to do all the fft, total power processing, and graphing for the whole winter.
However, if you adjusted a window, setting this to `False` will then make it so the windows in the `days1` and `days2` get FFT processing done.
Make sure `skip_processing=False` so that FFT happens.
They won't get graphed or total power processed because those imply overwriting some but not all total power files.
So, after running with `do_all_windows=False`, run the program again with `do_all_windows=True` and `skip_fft=True` and `skip_processing=False` so that total power processing and graphing happen with the updated windows.
```python
do_all_windows = True
```

### **skip_fft**
Set this to true when you want to skip the IDL fft processing. This is mostly here so that when you run with `do_all_windows=False`, you can then combine those results with the previous results relatively quickly.
```python
skip_fft = False
```

### **skip_processing**
This involves the following code.
```python
skip_processing = False
```
If you have already done the IDL and total power processing previously (so you already have the CSV files), you can skip that processing by setting this option to True.

### **days1 and days2**
These are the dictionaries that you will fill out if you're running with `do_all_windows = False`.
See the examples in the code for how you fill it out.
They `days1` corresponds to the windows in `year1` while `days2` corresponds to the windows in `year2`.
If you're running with `do_all_windows = True`, then these will be ignored.

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
* **NOTE:** These may say P14_1_ff instead of _31 for each set of images.

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

# Potential Errors
This section covers some potential errors you may run into and some possible troubleshooting steps.

## Path Not Existing
Several errors you may encounter may involve path not found errors or directories not existing.
* **WARNING!! The given ____dir: ___ does not exist!**
    * This happens when the directories you put in don't exist. These are the `IDL_DIR`, `idl_scripts_dir`, `save_dir`, and `read_dir`. Make sure these paths are correct. You can check to see what paths were actually used by using Spyder's variable explorer or by printing the variable when running the script with interactivity after it runs (`python -i`).
* **WARNING! File missing: ___/TempOH_TOTAL.csv**
    * This means that the `.csv` files from the IDL processing haven't been made. Make sure that the `skip_processing` option is false the first time you run this program on the data.
* **WARNING: The first P12 image file (needed for timestamp) is missing! ____/P12___.tif**
    * The program reads the first P12 image file for each window to get the initial timestamp. If that image is not present, you will get this error. It may just be not the expected name. See the `p12_img_stub` parameter and compare with what it is for your drive.
* **WARNING:______ doesn't have a TempOH0_TOTAL.csv file, so its total power won't be used.**
    * This means that when total power processing was done on that window, the window was too short, so no `TempOH0_TOTAL.csv`, `TempOH1_TOTAL.csv`, etc. Either try to expand the window, update the `days.txt` file, and run the processing, or delete the window.

## Improper Files
You may encounter errors relating to improperly formatted or files.
There can also be errors relating to files not being filled out properly.
In particular, the `days.txt` could be easily messed up.
For these, see the instructions for the [read directory setup](#read-directory) and the [save directory setup](#save-directory) to see where you went wrong with your file setup.
* **WARNING! The first line should be the month stub like Nov or Apr . Make sure days.txt is formatted correctly.**
    * You will get this if your `days.txt` file is missing the month stub on the first line of the file.
* **WARNING! At least one row in ___/days.txt has _ columns instead of 3. Make sure ___/days.txt is formatted correctly.**
    * You will get this if at least one row of the `days.txt` file (besides the line with the month stub) doesn't have 3 columns.
* **WARNING!!! Only one of the following days.txt files exists:**
    * This will occur when the `days.txt` file exists only in the `read_dir`'s month-year or in the `save_dir`'s year/month-year folder. Make sure that it is present in both.
* **WARNING!!! the days.txt data are not the same length at the following two paths!**
    * This will occur when the the `read_dir`'s and `save_dir`'s version of `days.txt` contain different numbers of columns. Make sure that they have the same data.
* **WARNING!!! the days.txt data do not share the same data at the following two paths!**
    * This will occur when the the `read_dir`'s and `save_dir`'s version of `days.txt` contain the same number of columns, but have different windows. Make sure that they have the same data.

# Running the Program
Once you have opened the runner in your chosen environment and adjusted the required variables, you should be able to simply hit the run button to run it.
The program will constantly log what it's up to, so you should be able to track its progress.
Messages (besides error messages) that are from the runner and not the IDL code will have dashes to signify their origin (`--- message ---`).
The program will output the following sets of files in your `save_dir`.
* Inside the base `save_dir` directory there will be a plot of the winter. In its filename it will say the `year1` and `year2` of the drive (or just `year1` if the winter takes place in just one year). It will look like, for example `Totpowr_winter_2013_to_2014.jpg`.
* Inside the year folders, there will be total power plots made for each month of windows. They have the month stub and the year in their filenames. They will look like, for example `MarTotpowr2016.jpg`.
* Inside the year then month-year folders, there will be folders made for each window in your `days.txt` file. They have the month stub, days of the month that the night involves, and the image indexes of the start and end of the window. They will look like the following.
    * `Nov30-01_0000-0400`
    * `Feb01-02_0301-1424`
* Inside these folders will be one to several CSV files that have the various powers calculated by the FFT processing. Note that the power spectrum processing uses the same folders, so there may be other CSV files associated with that process. The ones that are made by this program are `TempOH0_TOTAL.csv` and possibly more files with indexes 1, 2, 3, etc. The number of these CSV files depends on the length of the window.
* Also inside these folders is a file called `T_and_power.txt` that has the total power calculations for each `TempOHi_TOTAL.csv` file in the folder.


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
