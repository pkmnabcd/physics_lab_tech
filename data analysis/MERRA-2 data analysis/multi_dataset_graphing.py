import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap


def graph_multiple_locations_for_year(list_of_locations, year_filepath, graph_temp, graph_winds, altitude_level,
                                      day_emphasis_bar, want_smoothing, specified_day_of_year_range):
    from grapher import Merra
    merra_objects = []
    for location in list_of_locations:
        current_merra = Merra(year_filepath, location)
        current_merra.set_altitude_level(altitude_level)
        print("Loading data for " + location)

        if graph_temp:
            current_merra.set_temp_data()
        if graph_winds:
            current_merra.set_wind_data()

        if isinstance(specified_day_of_year_range, list):
            current_merra.set_specified_date_range(specified_day_of_year_range)

        merra_objects.append(current_merra)

    if graph_temp:
        make_multiple_location_graph_for_year(merra_objects, year_filepath, altitude_level, day_emphasis_bar, want_smoothing,
                                              list_of_locations, specified_day_of_year_range, True)
    if graph_winds:
        make_multiple_location_graph_for_year(merra_objects, year_filepath, altitude_level, day_emphasis_bar, want_smoothing,
                                              list_of_locations, specified_day_of_year_range, False)


def make_multiple_location_graph_for_year(merra_objects, year_filepath, altitude_level, day_emphasis_bar, want_smoothing,
                                          list_of_locations, specified_day_of_year_range, graphing_temp):
    from grapher import do_smoothing
    from grapher import get_location_string
    from grapher import folder_check_and_maker

    begin_month, end_month = merra_objects[0].return_begin_and_end_months()
    altitude = str(altitude_level)
    year = merra_objects[0].return_year()
    day_of_year_list = merra_objects[0].return_day_of_year_list()

    do_specified_day_of_year_range = isinstance(specified_day_of_year_range, list)
    make_day_marker = isinstance(day_emphasis_bar, int)

    if want_smoothing:
        day_of_year_list = do_smoothing(day_of_year_list)
    day_of_year_list = np.array(day_of_year_list)

    # small_figure = graphing_temp or (not graphing_temp and want_smoothing)
    # plt.figure(figsize=(15, 10)) if small_figure else plt.figure(figsize=(25, 15))
    plt.figure(figsize=(20, 15))

    if graphing_temp:
        for current_data in merra_objects:
            temp_data = current_data.return_temp_list()
            if want_smoothing:
                temp_data = do_smoothing(temp_data)
            temp_data = np.array(temp_data)

            location = get_location_string(current_data.return_subfolder())
            plt.plot(day_of_year_list, temp_data, label='Temp at ' + location)

    else:
        for current_data in merra_objects:
            north_wind_data = current_data.return_north_wind_list()
            if want_smoothing:
                north_wind_data = do_smoothing(north_wind_data)
            north_wind_data = np.array(north_wind_data)

            east_wind_data = current_data.return_east_wind_list()
            if want_smoothing:
                east_wind_data = do_smoothing(east_wind_data)
            east_wind_data = np.array(east_wind_data)

            location = get_location_string(current_data.return_subfolder())
            plt.plot(day_of_year_list, north_wind_data, label='North Wind at ' + location)
            plt.plot(day_of_year_list, east_wind_data, label='East Wind at ' + location)

    plt.grid(visible=True, axis="both")
    title_type = "Temperature between " if graphing_temp else "Wind between "

    title = title_type + begin_month + " and " + end_month + " " + year
    if do_specified_day_of_year_range:
        begin_day, end_day = str(specified_day_of_year_range[0]), str(specified_day_of_year_range[1])
        title = title_type + "day " + begin_day + " and day " + end_day + " " + year
    title += " at altitude level " + altitude
    title = "\n".join(wrap(title))
    plt.title(title, fontsize=25)
    if make_day_marker:
        if do_specified_day_of_year_range:
            begin_day, end_day = specified_day_of_year_range[0], specified_day_of_year_range[1]
            if begin_day <= day_emphasis_bar <= end_day:
                plt.axvline(x=day_emphasis_bar, color='r',
                            label="Marker for day " + str(day_emphasis_bar))
    plt.legend()

    plt.xlabel("Day of Year", fontsize=20)
    plt.xticks(ticks=np.arange(int(day_of_year_list[0]), day_of_year_list[-1], 10), fontsize=15)
    y_label = "Temperature (K)" if graphing_temp else "Wind Speed (m / s)"
    plt.ylabel(y_label, fontsize=20)
    plt.yticks(fontsize=15)

    save_directory = year_filepath + "output_graphs//multi_location//"
    folder_check_and_maker(save_directory)

    location_string = ""
    for location in list_of_locations:
        location_string += location + ","

    smoothing_file_label = "smoothed_" if want_smoothing else ""

    filename_type = "_temp_at_altitude_" if graphing_temp else "_wind_at_altitude_"
    filename = smoothing_file_label + begin_month + "_to_" + end_month
    if do_specified_day_of_year_range:
        begin_day, end_day = str(specified_day_of_year_range[0]), str(specified_day_of_year_range[1])
        filename = smoothing_file_label + begin_day + "_to_" + end_day
    filename += "_" + year + filename_type + altitude + " at " + location_string + ".png"
    save_path = save_directory + filename
    plt.savefig(save_path)

    plt.close()


def graph_all_locations_one_day(year_filepath, graph_temp, graph_winds, altitude_level, day):
    from grapher import Merra
    merra_objects = []

    locations = ["McMurdo", "McMurdo_minus_15#1", "McMurdo_minus_15#2", "McMurdo_minus_15#3", "McMurdo_minus_15#4",
                 "McMurdo_minus_15#5", "McMurdo_minus_15#6", "McMurdo_minus_15#7", "McMurdo_minus_15#8",
                 "McMurdo_minus_15#9", "McMurdo_minus_15#10", "McMurdo_minus_15#11", "McMurdo_minus_15#12",
                 "McMurdo_minus_15#13", "McMurdo_minus_15#14", "McMurdo_minus_15#15", "McMurdo_minus_15#16",
                 "McMurdo_minus_15#17", "McMurdo_minus_15#18", "McMurdo_minus_15#19", "McMurdo_minus_15#20",
                 "McMurdo_minus_15#21", "McMurdo_minus_15#22", "McMurdo_minus_15#23"]
    for location in locations:
        current_merra = Merra(year_filepath, location)
        current_merra.set_altitude_level(altitude_level)
        print("Loading data for " + location)

        if graph_temp:
            current_merra.set_temp_data()
        if graph_winds:
            current_merra.set_wind_data()

        merra_objects.append(current_merra)

    if graph_temp:
        make_all_locations_graph_one_day(merra_objects, year_filepath, altitude_level, day, True)
    if graph_winds:
        make_all_locations_graph_one_day(merra_objects, year_filepath, altitude_level, day, False)


def make_all_locations_graph_one_day(merra_objects, year_filepath, altitude_level, day, graphing_temp):
    from grapher import folder_check_and_maker

    begin_month, end_month = merra_objects[0].return_begin_and_end_months()
    altitude = str(altitude_level)
    year = merra_objects[0].return_year()
    day_of_year_list = merra_objects[0].return_day_of_year_list()

    minus_amounts = []
    for merra in merra_objects:
        minus_amounts.append(get_location_minus_amount(merra.return_subfolder()))

    data_index = day_of_year_list.index(day)

    # small_figure = graphing_temp or (not graphing_temp and want_smoothing)
    # plt.figure(figsize=(15, 10)) if small_figure else plt.figure(figsize=(25, 15))
    plt.figure(figsize=(20, 15))

    if graphing_temp:
        temp_data = []
        for merra in merra_objects:
            data = merra.return_temp_list()
            temp_data.append(data[data_index])
        temp_data = np.array(temp_data)

        plt.scatter(minus_amounts, temp_data, label='Temp')

    else:
        north_wind_data = []
        east_wind_data = []
        for merra in merra_objects:
            north_data = merra.return_north_wind_list()
            east_data = merra.return_east_wind_list()

            north_wind_data.append(north_data[data_index])
            east_wind_data.append(east_data[data_index])

        plt.scatter(minus_amounts, north_wind_data, label='North Wind')
        plt.scatter(minus_amounts, east_wind_data, label='East Wind')

    plt.grid(visible=True, axis="both")
    title_type = "Temperature on day " if graphing_temp else "Wind on day "

    title = title_type + str(day) + " in the year " + year + " at altitude level " + altitude
    title = "\n".join(wrap(title))
    plt.title(title, fontsize=25)

    plt.xlabel("McMurdo minus x degrees longitude", fontsize=20)
    plt.xticks(fontsize=15)
    y_label = "Temperature (K)" if graphing_temp else "Wind Speed (m / s)"
    plt.ylabel(y_label, fontsize=20)
    plt.yticks(fontsize=15)

    save_directory = year_filepath + "output_graphs//multi_location//"
    folder_check_and_maker(save_directory)

    filename_type = "_temp_at_altitude_" if graphing_temp else "_wind_at_altitude_"
    filename = "day_" + str(day) + "_" + year + filename_type + altitude + ".png"
    save_path = save_directory + filename
    plt.savefig(save_path)

    plt.close()


def get_location_minus_amount(subfolder_string):
    minus_amount = 0
    if "minus" in subfolder_string:
        value = 0
        string_length = len(subfolder_string)
        for i in range(string_length):
            current_character = subfolder_string[i]
            if current_character == "#":
                value = int(subfolder_string[i + 1:])
                break
        minus_amount = value * 15
    return minus_amount

