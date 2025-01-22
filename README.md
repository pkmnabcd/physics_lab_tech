# What is this repo?
This is a repository of code that I've made for my physics lab. I do a bunch of data analysis and processing, so many of these are just simple scripts that make my life easier. However, there are a few programs that are particularly large, and probably should have been their own repos, but I like keeping everything in one place for now.

## Some Specific Subprojects
### Chile Intensity Plotting
This contains several functions to help me in my task to plot ChileMTM's OH layer temperature. Some of these are functions to help me clean the dataset, as previous people have messed with the database, requiring me to fix it.

The main graphing code is gathering and averaging daily temperature data, and graphing it over the year, or for all time (from Aug2009 to Apr2024)

### MERRA-2 data analysis
This is all one python program with main driver code with a bunch of options. This was meant to be used with downloaded and IDL-processed MERRA-2 NASA atmospheric model data. This can perform various graphical analysis on the data.

### Homebrew Origin

This silly-named project is a project to replace my lab's use of some software called Origin. This makes a program that takes ChileMTM OH image intensity and calculated temperature data and detects useless twilight and cloud data and removes it by making edited files that will later be graphed.
