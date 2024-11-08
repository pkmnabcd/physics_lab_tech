"""
Purpose of this program:

Go through all of my excel files (or ouputted .csv files)
Apply a process to each of the months in each year
    On each month, count the number of days, and how many 1s are in each 
category of processing.

For each year, add the data for each month into an array that holds all the 
percentage data for the months
    Use matplotlib or whatever package to plot data

"""
import os.path
import csvhandling
import pandas as pd
import arrayprocessing as processing


df = pd.DataFrame()
# Do the process to each year at once.
for i in range(13):
    year = str(2009 + i)

    year_avg_data = pd.DataFrame()
    year_out = pd.DataFrame()
    included_months = []
    for month in range(12):
        path = csvhandling.import_path_making(month, year)

        # Skips csv files that don't exist
        if not os.path.exists(path):
            continue

        # Count what months have a .csv file
        included_months.append(csvhandling.month_converting(month))
        # Import data from the month
        monthly_data = csvhandling.import_csv_to_df(path)

        # Get all the averages, add to the DataFrame for all the years' averages
        month_avg = processing.monthly_averages(monthly_data, month)
        year_avg_data = pd.concat([year_avg_data, month_avg])

        # Get each month's data to be put into the output file
        month_out = processing.output_processing(monthly_data, month_avg, month, year)
        year_out = pd.concat([year_out, month_out])

    # Add each year's data into the final DataFrame
    df = pd.concat([df, year_out])

    # Now to present the data
    # Make the indexes for the plot
    year_avg_data.index = included_months
    # Plotting function
    processing.avg_plot(year_avg_data, year)


# Export the final dataframe to csv
csvhandling.export_csv(df)
