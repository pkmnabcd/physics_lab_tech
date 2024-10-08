# Homebrew Origin Manual

## Program Purpose

The purpose of this program is to take raw Chile MTM temperature/intensity data, clean it, and graph the original and cleaned version in the same program. The goal is to be able to drag and drop this script into whatever directory where you have the intenisty .dat files and process each one.

The design philosophy of this program maintains that you shouldn't need to edit any code each time you use it, so instead of using an IDE to edit and run the code, you will run the code on the command line, and pass in the file path of the file you want to run the process on.

## What you need for this program

### Python and Java files
To run this program, you need the python and java source code in the right directory. The right directory is specified in the main script: chileTempCleanerAndGrapher.bat , which says that the python files should be in the same directory as main.py which has the path `SET PYTHON_SCRIPT=C:\Gabe's_stuff\Gabe_programs\Data Analysis\homebrew origin\python_src\main.py`. The java files should be located in the directory `SET JAVA_PATH=C:\Gabe's_stuff\Gabe_programs\Data Analysis\homebrew origin\java_src`. If you're on a different system than the one this program was written for, you can specify your own path by changing these values in `chileTempCleanerAndGrapher.bat`.

You need the following python files in the same folder (specified by `PYTHON_SCRIPT`) to run the program:
* main.py
* parser.py
* grapher.py

You need the following java files in the same folder (specified by `JAVA_PATH`) to run the program:
* AbstractCleaner.class
* CloudCleaner$Graph.class
* CloudCleaner.class
* Main.class
* Parser.class
* PreBGCleaner.class
* PreOHCleaner.class
* StandardDeviationCleaner.class
* StandardDeviationCleanerBGOnly.class
* STDEV.class
* Write.class

If you have the corresponding .java files, but not the .class files, you will need to compile them by navigating to the folder where all the .java files are, and run `javac Main.java`. If the command isn't recognized, you'll have to get the jdk as described below.

### Java Installed
Make sure you have Java installed by opening a windows terminal (this can be done by hitting the windows key and typing `command` and clicking what pops up) and entering `javac`. If a long message is printed, describing how to use the command, then you have java already and can skip this step. If a *command not found* message is printed, you need to install it. 
#### Installing Java
You can install Java by looking up Java JDK Windows and downloading the installer. You can also find it at [this link](https://www.oracle.com/java/technologies/downloads/).

### Matplotlib
You may have to install the python package matplotlib to run the script from the command line. Do this by running the following command: `python -m pip install matplotlib`.

Also try `python3 -m pip install matplotlib` if the above command doesn't work.

### The Correct Files
The inputted data files are those outputted by Dr. Yucheng Zhao's IDL code called `ALO_OH_Andover.pro` which is usually kept in the Chile MTM drive in the same directory as the year folders.

This script is expecting inputted file names in this format (what Yucheng's script outputs): `OH_Andover_ALOYYdayD.dat`. Where `YY` means the last two numbers of the year (for example 2022 is represented as 22) and D is the day of the year number. It can be one, two, or three characters long.
#### Filename Examples
* `OH_Andover_ALO23day122.dat`
* `OH_Andover_ALO20day122.dat`
* `OH_Andover_ALO23day1.dat`
* `OH_Andover_ALO24day365.dat`
* `OH_Andover_ALO09day65.dat`
#### File Contents
My program is expecting the file's contents to look like this:
```
    May09-10-23         OHTemp      OHBandInt        CCDTemp            P12            P14             BG        ActDark
        -1.2800       263.9560    223807.2500       -46.7000     65535.0000     65534.1055     65532.7344           -NaN
        -1.0200     39241.3867***************       -43.0400     49866.3125     54312.7578     61185.1250      5248.2764
```

The dataset is made up of columns with length 15 with everything right-justified within the column. The first column conisists of labels that need to be identical to these labels except for the date label, which must follow the format: `MMMDD-DD-YY`. The inner data can have positive or negative numbers, a NaN (Not a Number) value (from what I've seen, they're most often `-NaN`, but `NaN` is also supported), or the entire row of that column can be `***************`.

### Windows Terminal
To run the script, you will use the windows terminal. You can get to it by hitting the windows key and entering `terminal`, but you will have to find the right directory by using for example `cd I:\ChileMTM\2023`. You can also just use the file explorer and open the folder to where the files are and right-click and select `Open in Terminal`. This option is present in windows 11, but I'm unsure about older versions. Once you're in the terminal, you can run the script.

## Running the script
Once you have the above items, you are ready to run the script. For simplicity, I recommend putting the chileTempCleanerAndGrapher.bat file (the actual script) in the year folder, open the terminal into that same folder, then you can navigate to the right file from there as you run the script.

When you have the terminal open in the same directory as `chileTempCleanerAndGrapher.bat`, use this command format to run the script:

`.\chileTempCleanerAndGrapher.bat [filename]`

The `.\` before the script name tells the terminal to run the script. The brackets represent the filename that will be passed to the python and Java files. Two things are *super important* to note about these.
* Always use forward-slash `/` when navigating through a folder
* If there is a space in the path, *always use quotation marks around the filename*

Here's an example if I'm in the 2023 ChileMTM folder:

`./chileTempCleanerAndGrapher.bat Oct2023/processed/OH_Andover_ALO23day276.dat`

One you run the script for the first time, instead of manually typing in the entire command again for the next file, you can instead press the up arrow to get the most recently used command, then change a number or two, then press enter to run the script again.

## Common Errors
### File Errors
* `Error: Could not find or load main class Main`
    * Java can't find the file `Main.class` in the directory assigned to `JAVA_PATH`.
    * Make sure that there isn't a `\` (backslash) at the end of the `JAVA_PATH`.
    * Double check that the path to the java .class files is correct, formatted correctly, and is hardcoded.
        * Ex: `SET JAVA_PATH=C:\Gabe's_stuff\Gabe_programs\Data Analysis\homebrew origin\java_src`
* `python: can't open file .....`
    * Python can't find the file that the script is trying to run.
    * Make sure that the file path to main.py is correct, formatted correctly, and hardcoded.
        * Ex: `SET PYTHON_SCRIPT=C:\Gabe's_stuff\Gabe_programs\Data Analysis\homebrew origin\python_src\main.py`
* `java.io.FileNotFoundException` and `FileNotFoundError`
    * The python and java files were found, but the inputted .dat file wasn't found.
    * Make sure that the file path that you inputted in the command line is correct and that it's formatted correctly.
        * Directories should be separated by forward slashes: `/`. 
        * Surround the file path with quotation marks `""`. Technically this is only needed when there is a space in the file path, but it's best to keep them just in case.
        * Double check that the file path is correct
### Other Errors
* `ModuleNotFoundError`
    * Make sure that you have all of the python and java files as specified above.
    * Make sure that you have matplotlib installed, following the above instructions
