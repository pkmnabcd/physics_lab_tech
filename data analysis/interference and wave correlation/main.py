"""
This program processes csv files made from ChileMTM_YEAR_weather_and_processing files and outputs a graph for each one.
This graph will have an x-axis that shows the months in that year, and has two y-axis. One y-axis is the amount of
interference throughout the month, and the other is the number of days with identifiable waves.
"""

import csvhandling
import array_processing as processing


def main():
    YEARS = ["2021", "2022", "2023"]
    for year in YEARS:
        path = csvhandling.import_path_making(year)
        df = csvhandling.import_csv_to_df(path)
        print(df)

        monthly_interference = processing.monthly_interference_count(df)
        monthly_days_with_waves = processing.monthly_days_with_waves_count(df)

        processing.make_graph(monthly_interference, monthly_days_with_waves, year)


main()
