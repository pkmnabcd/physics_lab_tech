"""
time_wind_grapher.py
by Gabriel Decker
"""
import file_input as file
from metadata_gathering import get_file_metadata
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from os.path import exists
from os import mkdir


def folder_check_and_maker(path):
    if exists(path):
        return
    else:
        mkdir(path)


def confirm_month_unbroken_data(list_of_filenames):
    """
    This will terminate the program if it detects that the data isn't properly ordered
    The data files must be a continuous line of days in the same month
    :param list_of_filenames: a list of all the filenames in the dataset to be tested
    :return: None
    """
    list_length = len(list_of_filenames)
    middle_index = list_length // 2

    first_filename = list_of_filenames[0]
    last_filename = list_of_filenames[list_length - 1]
    middle_filename = list_of_filenames[middle_index]

    first_data = get_file_metadata(first_filename)
    last_data = get_file_metadata(last_filename)
    middle_data = get_file_metadata(middle_filename)

    is_unbroken = int(first_data[2]) + list_length - 1 == int(last_data[2]) and int(first_data[2]) + middle_index == int(middle_data[2])
    is_same_month = first_data[1] == last_data[1] == middle_data[1]

    if not is_unbroken or not is_same_month:
        print("Need unbroken line of data in the same month! Month:" + first_data[1])
        sleep(5)
        quit()


def get_1d_list(inlist):
    """
    Takes a 2-D list and returns a 1-D list in order of the values
    :param inlist: a 2-D list
    :return: a 1-D list version of the inlist
    """
    out_list = []
    for row in inlist:
        for number in row:
            out_list.append(number)
    return out_list


def make_wind_graph(north_wind_data_by_day, east_wind_data_by_day, filename_data, save_directory):
    """
    This function makes the graph of the day of year and wind speed with V and U
    :param north_wind_data_by_day: 2-D array of each day's V data in a separate array
    :param east_wind_data_by_day: 2-D array of each day's U data in a separate array
    :param filename_data: the metadata for the first day
    :param save_directory: the folder path the files will be saved to
    :return: None
    """
    first_date_number = filename_data[0]
    month = filename_data[1]
    # day = filename_data[2]  # Day is commented out because it's never used as of now
    year = filename_data[3]
    altitude = filename_data[4]

    # Attempt to combine all the values into a 1-D list
    north_wind_data = get_1d_list(north_wind_data_by_day)
    north_wind_data = np.array(north_wind_data)

    east_wind_data = get_1d_list(east_wind_data_by_day)
    east_wind_data = np.array(east_wind_data)

    date_number_list = []
    for i in range(len(north_wind_data_by_day)):
        date_number = int(first_date_number) + i
        for j in range(8):
            date_number_list.append(date_number + j * .125)
    date_number_list = np.array(date_number_list)

    plt.figure(figsize=(12, 8))
    plt.plot(date_number_list, north_wind_data, label='V')
    plt.plot(date_number_list, east_wind_data, label='U')

    plt.grid(visible=True, axis='both')
    plt.title("Wind in " + month + ' ' + year + " at altitude level " + altitude, fontsize=25)
    plt.legend()

    plt.xlabel("Day of Year", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Wind Speed (m / s)", fontsize=20)
    plt.yticks(fontsize=15)

    filename = month + year + "_wind_at_altitude_" + altitude + ".png"
    save_path = save_directory + filename
    plt.savefig(save_path)

    # plt.show()
    plt.close()


def make_temp_graph(temp_data_by_day, filename_data, save_directory):
    """
    This function makes the graph of the day of year and temperature T
    :param temp_data_by_day: north_wind_data_by_day: 2-D array of each day's T data in a separate array
    :param filename_data: the metadata for the first day
    :param save_directory: the folder path the files will be saved to
    :return: None
    """
    first_date_number = filename_data[0]
    month = filename_data[1]
    # day = filename_data[2]  # Day is commented out because it's never used as of now
    year = filename_data[3]
    altitude = filename_data[4]

    # Combine the 2-D list values into a 1-D list
    temp_data = get_1d_list(temp_data_by_day)
    temp_data = np.array(temp_data)

    date_number_list = []
    for i in range(len(temp_data_by_day)):
        date_number = int(first_date_number) + i
        for j in range(8):
            date_number_list.append(date_number + j * .125)
    date_number_list = np.array(date_number_list)

    plt.figure(figsize=(12, 8))
    plt.plot(date_number_list, temp_data, label='T')

    plt.grid(visible=True, axis='both')
    plt.title("Temp in " + month + ' ' + year + " at altitude level " + altitude, fontsize=25)
    plt.legend()

    plt.xlabel("Day of Year", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Temperature (K)", fontsize=20)
    plt.yticks(fontsize=15)

    filename = month + year + "_temp_at_altitude_" + altitude + ".png"
    save_path = save_directory + filename
    plt.savefig(save_path)

    # plt.show()
    plt.close()


def make_temp_year_graph(temp_data, day_of_year_list, metadata, save_location):
    begin_month = metadata[0]
    end_month = metadata[1]
    altitude = metadata[2]
    year = metadata[3]

    plt.figure(figsize=(15, 10))
    plt.plot(np.array(day_of_year_list), np.array(temp_data), label='T')

    plt.grid(visible=True, axis="both")
    title = "Temp between " + begin_month + " and " + end_month + " " + year + " at altitude level " + altitude
    plt.title(title, fontsize=25)
    plt.legend()

    plt.xlabel("Day of Year", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Temperature (K)", fontsize=20)
    plt.yticks(fontsize=15)

    filename = begin_month + "_to_" + end_month + "_" + year + "_temp_at_altitude_" + altitude + ".png"
    save_path = save_location + filename
    plt.savefig(save_path)

    plt.close()


def make_wind_year_graph(north_wind_data, east_wind_data, day_of_year_list, metadata, save_location):
    begin_month = metadata[0]
    end_month = metadata[1]
    altitude = metadata[2]
    year = metadata[3]

    plt.figure(figsize=(25, 15))
    plt.plot(np.array(day_of_year_list), np.array(north_wind_data), label='V')
    plt.plot(np.array(day_of_year_list), np.array(east_wind_data), label='U')

    plt.grid(visible=True, axis="both")
    title = "Wind between " + begin_month + " and " + end_month + " " + year + " at altitude level " + altitude
    plt.title(title, fontsize=25)
    plt.legend()

    plt.xlabel("Day of Year", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Wind Speed (m / s)", fontsize=20)
    plt.yticks(fontsize=15)

    filename = begin_month + "_to_" + end_month + "_" + year + "_wind_at_altitude_" + altitude + ".png"
    save_path = save_location + filename
    plt.savefig(save_path)

    plt.close()


def time_wind_grapher(altitude_number, path):
    """
    This gets the wind data from the .dat files at the given path. It will use the given altitude level
    :param altitude_number: int between 1 and 72 that will determine which line of the files is read
    :param path: the directory in which the .dat files are located
    :return: None
    """
    north_wind_filenames = file.get_relevant_filenames(path, 'V')
    east_wind_filenames = file.get_relevant_filenames(path, 'U')

    north_first_day_filename_data = get_file_metadata(north_wind_filenames[0])
    east_first_day_filename_data = get_file_metadata(east_wind_filenames[0])

    # Test to make sure these are all in the same month
    confirm_month_unbroken_data(north_wind_filenames)
    confirm_month_unbroken_data(east_wind_filenames)

    # Test to make sure they start on the same day and are the same length
    doesnt_start_same_day = north_first_day_filename_data[0] != east_first_day_filename_data[0]
    not_same_length = len(north_wind_filenames) != len(east_wind_filenames)
    if doesnt_start_same_day or not_same_length:
        print("The two wind types' files must match")
        sleep(5)
        quit()

    # Make arrays with the actual data in the files
    north_wind_data = []
    for filename in north_wind_filenames:
        north_wind_data.append(file.read_dat_file(filename, altitude_number))

    east_wind_data = []
    for filename in east_wind_filenames:
        east_wind_data.append(file.read_dat_file(filename, altitude_number))

    # Pass data into graphing function
    north_first_day_filename_data.append(str(altitude_number))
    print(north_first_day_filename_data)

    save_directory = path[:-18] + "output_graphs//"
    folder_check_and_maker(save_directory)
    make_wind_graph(north_wind_data, east_wind_data, north_first_day_filename_data, save_directory)
    print("File saved to: " + save_directory)


def time_temp_grapher(altitude_number, path):
    """
    This gets the temp data from the .dat files at the given path and outputs a graph. It will use the given altitude
    level
    :param altitude_number: int between 1 and 72 that will determine which line of the files is read
    :param path: the directory in which the .dat files are located
    :return: None
    """
    temp_filenames = file.get_relevant_filenames(path, 'T')

    temp_first_day_metadata = get_file_metadata(temp_filenames[0])

    # Test to make sure these are all in the same month
    confirm_month_unbroken_data(temp_filenames)

    # Make arrays with the actual data in the files
    temp_data = []
    for filename in temp_filenames:
        temp_data.append(file.read_dat_file(filename, altitude_number))

    # Pass data into graphing function
    temp_first_day_metadata.append(str(altitude_number))
    print(temp_first_day_metadata)

    save_directory = path[:-18] + "output_graphs//"
    folder_check_and_maker(save_directory)
    make_temp_graph(temp_data, temp_first_day_metadata, save_directory)
    print("File saved to: " + save_directory)


def year_temp_grapher(altitude_number, path):
    """
    Makes a plot of the temperature throughout the year, for however many months we have data for
    Warning: the data must be continuous
    The given path should contain month folders (capitalized, full name)
    :param altitude_number: the altitude level to be used: int between 1 and 72
    :param path: the filepath which should have the month folders inside ex: E://Folder//
    :return: None
    """
    # Get all the filenames that we'll be using by traversing through the month folders and getting the filenames of
    # the relevant files
    # Metadata to preserve for graph:
    # First and last month, altitude, year
    metadata = []

    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

    relevant_months = []
    for month in month_list:
        month_path = path + month + "//"
        if exists(month_path):
            relevant_months.append(month)

    metadata.append(relevant_months[0])
    metadata.append(relevant_months[-1])
    metadata.append(str(altitude_number))

    filenames_by_month = []
    for month in relevant_months:
        month_path = path + month + "//IDL_data_exports//"
        filenames_by_month.append(file.get_relevant_filenames(month_path, 'T'))

    metadata.append(get_file_metadata(filenames_by_month[0][0])[3])
    print(metadata)

    # Make sure month is continuous with itself
    for month_of_filenames in filenames_by_month:
        confirm_month_unbroken_data(month_of_filenames)

    # Make sure months are continuous with each other
    for i in range(len(filenames_by_month) - 1):
        # Figure out what the last day of the month should be for it to be continuous
        month = get_file_metadata(filenames_by_month[i][0])[1]
        if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December":
            days_in_month = "31"
        elif month == "April" or month == "June" or month == "September" or month == "November":
            days_in_month = "30"
        else:
            if int(get_file_metadata(filenames_by_month[i][0])[3]) % 4 == 0:
                days_in_month = "29"
            else:
                days_in_month = "28"

        begin_month_last_day = get_file_metadata(filenames_by_month[i][-1])[2]
        end_month_first_day = get_file_metadata(filenames_by_month[i + 1][0])[2]
        is_continuous = begin_month_last_day == days_in_month and end_month_first_day == "01"
        if not is_continuous:
            print("The data must be continuous between months")
            sleep(5)
            quit()

    filenames = get_1d_list(filenames_by_month)
    first_day_of_year_number = int(get_file_metadata(filenames[0])[0])
    day_count = len(filenames)
    number_data_points_per_day = 8
    day_list = []
    for i in range(day_count):
        date_number = first_day_of_year_number + i
        for j in range(number_data_points_per_day):
            day_list.append(date_number + j * 1/number_data_points_per_day)

    temp_data_by_day = []
    for i in range(len(filenames)):
        temp_data_by_day.append(file.read_dat_file(filenames[i], altitude_number))
    temp_data = get_1d_list(temp_data_by_day)

    graph_save_location = path + "output_graphs//"
    folder_check_and_maker(graph_save_location)

    make_temp_year_graph(temp_data, day_list, metadata, graph_save_location)
    print("File saved to: " + graph_save_location)


def year_wind_grapher(altitude_number, path):
    """
        Makes a plot of the wind speed throughout the year, for however many months we have data for
        Warning: the data must be continuous
        The given path should contain month folders (capitalized, full name)
        :param altitude_number: the altitude level to be used: int between 1 and 72
        :param path: the filepath which should have the month folders inside ex: E://Folder//
        :return: None
        """
    # Get all the filenames that we'll be using by traversing through the month folders and getting the filenames of
    # the relevant files
    # Metadata to preserve for graph:
    # First and last month, altitude, year
    metadata = []

    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

    relevant_months = []
    for month in month_list:
        month_path = path + month + "//"
        if exists(month_path):
            relevant_months.append(month)

    metadata.append(relevant_months[0])
    metadata.append(relevant_months[-1])
    metadata.append(str(altitude_number))

    north_wind_filenames_by_month = []
    for month in relevant_months:
        month_path = path + month + "//IDL_data_exports//"
        north_wind_filenames_by_month.append(file.get_relevant_filenames(month_path, 'V'))

    east_wind_filenames_by_month = []
    for month in relevant_months:
        month_path = path + month + "//IDL_data_exports//"
        east_wind_filenames_by_month.append(file.get_relevant_filenames(month_path, 'U'))

    metadata.append(get_file_metadata(north_wind_filenames_by_month[0][0])[3])
    print(metadata)

    # Make sure month is continuous with itself
    for month_of_filenames in north_wind_filenames_by_month:
        confirm_month_unbroken_data(month_of_filenames)
    for month_of_filenames in east_wind_filenames_by_month:
        confirm_month_unbroken_data(month_of_filenames)

    # Make sure months are continuous with each other
    for i in range(len(north_wind_filenames_by_month) - 1):
        # Figure out what the last day of the month should be for it to be continuous
        month = get_file_metadata(north_wind_filenames_by_month[i][0])[1]
        if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December":
            days_in_month = "31"
        elif month == "April" or month == "June" or month == "September" or month == "November":
            days_in_month = "30"
        else:
            if int(get_file_metadata(north_wind_filenames_by_month[i][0])[3]) % 4 == 0:
                days_in_month = "29"
            else:
                days_in_month = "28"

        begin_month_last_day = get_file_metadata(north_wind_filenames_by_month[i][-1])[2]
        end_month_first_day = get_file_metadata(north_wind_filenames_by_month[i + 1][0])[2]
        is_continuous = begin_month_last_day == days_in_month and end_month_first_day == "01"
        if not is_continuous:
            print("The data must be continuous between months")
            sleep(5)
            quit()
    for i in range(len(east_wind_filenames_by_month) - 1):
        # Figure out what the last day of the month should be for it to be continuous
        month = get_file_metadata(east_wind_filenames_by_month[i][0])[1]
        if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December":
            days_in_month = "31"
        elif month == "April" or month == "June" or month == "September" or month == "November":
            days_in_month = "30"
        else:
            if int(get_file_metadata(east_wind_filenames_by_month[i][0])[3]) % 4 == 0:
                days_in_month = "29"
            else:
                days_in_month = "28"

        begin_month_last_day = get_file_metadata(east_wind_filenames_by_month[i][-1])[2]
        end_month_first_day = get_file_metadata(east_wind_filenames_by_month[i + 1][0])[2]
        is_continuous = begin_month_last_day == days_in_month and end_month_first_day == "01"
        if not is_continuous:
            print("The data must be continuous between months")
            sleep(5)
            quit()

    north_wind_filenames = get_1d_list(north_wind_filenames_by_month)
    north_first_day_metadata = get_file_metadata(north_wind_filenames[0])
    east_wind_filenames = get_1d_list(east_wind_filenames_by_month)
    east_first_day_metadata = get_file_metadata(east_wind_filenames[0])

    # Make sure that the different winds have the same data over the same period
    doesnt_start_same_day = north_first_day_metadata[0] != east_first_day_metadata[0]
    not_same_length = len(north_wind_filenames) != len(east_wind_filenames)
    if doesnt_start_same_day or not_same_length:
        print("The two wind types' files must match")
        sleep(5)
        quit()

    first_day_of_year_number = int(get_file_metadata(north_wind_filenames[0])[0])
    day_count = len(north_wind_filenames)
    number_data_points_per_day = 8
    day_list = []
    for i in range(day_count):
        date_number = first_day_of_year_number + i
        for j in range(number_data_points_per_day):
            day_list.append(date_number + j * 1 / number_data_points_per_day)

    north_wind_data_by_day = []
    for i in range(len(north_wind_filenames)):
        north_wind_data_by_day.append(file.read_dat_file(north_wind_filenames[i], altitude_number))
    north_wind_data = get_1d_list(north_wind_data_by_day)

    east_wind_data_by_day = []
    for i in range(len(east_wind_filenames)):
        east_wind_data_by_day.append(file.read_dat_file(east_wind_filenames[i], altitude_number))
    east_wind_data = get_1d_list(east_wind_data_by_day)

    graph_save_location = path + "output_graphs//"
    folder_check_and_maker(graph_save_location)

    make_wind_year_graph(north_wind_data, east_wind_data, day_list, metadata, graph_save_location)
    print("File saved to: " + graph_save_location)


def main():
    # This filepath should contain the .dat files
    # The last folder should be named "IDL_data_exports"
    MONTH_PATH = "D://Downloading_merra_stuff//2020//March//IDL_data_exports//"
    
    YEAR_PATH = "D://Downloading_merra_stuff//2020//"

    #     MODE 1: Single month, single altitude, plotting wind speed
    ALTITUDE_NUMBER = 1
    time_wind_grapher(ALTITUDE_NUMBER, MONTH_PATH)

    # #     MODE 2: Single month, run through all altitudes, plotting wind speed
    # for i in range(72):  # There are 72 altitudes
    #     altitude_number = i + 1
    #     time_wind_grapher(altitude_number, MONTH_PATH)
    #
    #     MODE 3: Single month, single altitude, plotting temperature
    ALTITUDE_NUMBER = 1
    time_temp_grapher(ALTITUDE_NUMBER, MONTH_PATH)

    #     MODE 4: Up to a year, single altitude, plotting temperature
    ALTITUDE_NUMBER = 1
    year_temp_grapher(ALTITUDE_NUMBER, YEAR_PATH)

    #     MODE 5: Up to a year, single altitude, plotting wind
    ALTITUDE_NUMBER = 1
    year_wind_grapher(ALTITUDE_NUMBER, YEAR_PATH)
    
    # #     MODE 6: Up to a year, every other altitude, plotting temperature
    # for i in range(0, 72, 2):
    #     altitude_number = i + 1
    #     year_temp_grapher(altitude_number, YEAR_PATH)
    
    # #     MODE 7: Up to a year, every other altitude, plotting wind speed
    # for i in range(0, 72, 2):
    #     altitude_number = i + 1
    #     year_wind_grapher(altitude_number, YEAR_PATH)


main()
