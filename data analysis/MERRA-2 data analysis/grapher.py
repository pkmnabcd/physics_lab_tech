"""
grapher.py
by Gabriel Decker
"""
import file_input as file
from metadata_gathering import get_file_metadata
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from os.path import exists
from os import mkdir
from textwrap import wrap
from multi_dataset_graphing import graph_multiple_locations_for_year
from multi_dataset_graphing import graph_all_locations_one_day


def __folder_check_and_maker(path):
    if exists(path):
        return
    else:
        mkdir(path)


class Merra:
    def __init__(self, year_path, subfolder):
        self.__year_folder = year_path
        self.__subfolder = subfolder

        self.__months = self.__make_month_list()
        self.__start_month = self.__months[0]
        self.__end_month = self.__months[-1]

        self.__temperature_filenames = self.__make_filename_list("T")  # 2-D array, arrays separated by month
        self.__temperature_filenames_1D = get_1d_list_from_2d(self.__temperature_filenames)

        self.__north_wind_filenames = self.__make_filename_list("V")
        self.__north_wind_filenames_1D = get_1d_list_from_2d(self.__north_wind_filenames)

        self.__east_wind_filenames = self.__make_filename_list("U")
        self.__east_wind_filenames_1D = get_1d_list_from_2d(self.__east_wind_filenames)

        self.__check_filename_continuity()
        self.__day_of_year_list = self.__get_day_of_year_list_for_year()
        self.__year = get_file_metadata(self.__temperature_filenames_1D[0])[3]

        self.__temperature_data = []  # 3-D array: month->day->data
        self.__temp_data_loaded = False
        self.__north_wind_data = []
        self.__north_wind_data_loaded = False
        self.__east_wind_data = []
        self.__east_wind_data_loaded = False

        self.__current_altitude_value = 0

        # Default other settings
        self.__want_smoothing = False
        self.__smoothing_window_size = 32
        self.__do_polynomial_best_fit = False
        self.__polynomial_best_fit_order = 0
        self.__do_residual_analysis_graph = False
        self.__residual_analysis_type = "poly"

        self.__make_monthly_graphs = False
        self.__make_graph_for_year = False

        self.__make_day_marker = False
        self.__day_marker_value = 0

        self.__do_all_altitudes = False
        self.__do_every_other_altitude = False
        self.__do_specified_altitudes = False
        self.__specified_altitudes = None

        self.__specified_day_of_year_range = None
        self.__do_specified_day_of_year_range = False

    def set_temp_data(self):
        self.__temperature_data = self.__get_data(self.__temperature_filenames)
        self.__temp_data_loaded = True

    def set_wind_data(self):
        self.__north_wind_data = self.__get_data(self.__north_wind_filenames)
        self.__north_wind_data_loaded = True
        self.__east_wind_data = self.__get_data(self.__east_wind_filenames)
        self.__east_wind_data_loaded = True

    def set_altitude_level(self, level):
        self.__current_altitude_value = level

    def set_smoothing_toggle(self, toggle):
        assert isinstance(toggle, bool)
        self.__want_smoothing = toggle

    def set_polynomial_fit_order(self, order):
        assert isinstance(order, int)
        self.__do_polynomial_best_fit = True
        self.__polynomial_best_fit_order = order

    def set_residual_analysis_toggle(self, toggle, residual_type):
        assert isinstance(toggle, bool)
        if self.__polynomial_best_fit_order == 0:
            self.__polynomial_best_fit_order = 2
        self.__do_residual_analysis_graph = True

        self.__do_polynomial_best_fit = False
        self.__make_graph_for_year = False
        self.__make_monthly_graphs = False

        if residual_type != "poly":
            self.__residual_analysis_type = residual_type
            self.__want_smoothing = False

    def set_monthly_graphs_toggle(self, toggle):
        assert isinstance(toggle, bool)
        self.__make_monthly_graphs = toggle

    def set_year_graph_toggle(self, toggle):
        assert isinstance(toggle, bool)
        self.__make_graph_for_year = toggle

    def set_day_marker(self, toggle, value):
        assert isinstance(toggle, bool)
        self.__make_day_marker = toggle
        self.__day_marker_value = value

    def set_do_all_altitudes_toggle(self, toggle):
        assert isinstance(toggle, bool)
        self.__do_all_altitudes = toggle

    def set_do_every_other_altitude_toggle(self, toggle):
        assert isinstance(toggle, bool)
        self.__do_every_other_altitude = toggle

    def set_specified_altitudes(self, altitudes):
        self.__do_specified_altitudes = True
        self.__specified_altitudes = altitudes
        self.__current_altitude_value = -1

    def set_specified_date_range(self, dates):
        assert isinstance(dates, list)
        self.__do_specified_day_of_year_range = True
        self.__specified_day_of_year_range = dates
        self.__make_monthly_graphs = False

    def make_graphs(self):
        """
        The properties of the graphs depend on the Merra Object's settings and what data is set.
        :return: Graphs are always saved to //output_graphs//subfolder// folders in the year folder or month folder
        """
        if self.__do_every_other_altitude:
            self.__make_graphs_every_other_altitude()
        elif self.__do_all_altitudes:
            self.__make_graphs_all_altitudes()
        elif self.__do_specified_altitudes:
            self.__make_graphs_specified_altitudes()
        else:
            self.__make_graphs_for_current_altitude()

    def __make_graphs_for_current_altitude(self):
        print("Making graphs for altitude level: " + str(self.__current_altitude_value))
        if self.__make_monthly_graphs:
            for month in self.__months:
                self.__make_month_graph(month)
        if self.__make_graph_for_year:
            self.__make_year_graph()
        if self.__do_residual_analysis_graph:
            self.__make_residual_analysis_graph()

    def __make_month_graph(self, month):
        month_index = -1
        for i in range(len(self.__months)):
            if self.__months[i] == month:
                month_index = i
                break

        temp_filenames = self.__temperature_filenames[month_index]
        first_day_metadata = get_file_metadata(temp_filenames[0])

        if self.__temp_data_loaded:
            self.__generate_month_graph(True, month_index, first_day_metadata)
        if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
            self.__generate_month_graph(False, month_index, first_day_metadata)

    def __make_year_graph(self):
        if self.__temp_data_loaded:
            self.__generate_year_graph(True)
        if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
            self.__generate_year_graph(False)

    def __make_residual_analysis_graph(self):
        if self.__temp_data_loaded:
            self.__generate_residual_analysis_graph(True)
        if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
            self.__generate_residual_analysis_graph(False)

    def __generate_year_graph(self, graphing_temp):
        begin_month = self.__start_month
        end_month = self.__end_month
        altitude = str(self.__current_altitude_value)
        year = self.__year
        day_of_year_list = self.return_day_of_year_list()

        if self.__want_smoothing:
            day_of_year_list = do_day_of_year_smoothing(day_of_year_list, self.__smoothing_window_size)
        day_of_year_list = np.array(day_of_year_list)

        small_figure = graphing_temp or (not graphing_temp and self.__want_smoothing)
        plt.figure(figsize=(15, 10)) if small_figure else plt.figure(figsize=(25, 15))

        if graphing_temp:
            temp_data = self.return_temp_list()
            if self.__want_smoothing:
                temp_data = do_smoothing(temp_data, self.__smoothing_window_size)
            temp_data = np.array(temp_data)

            plt.plot(day_of_year_list, temp_data, label='T', color='tab:blue')

            if self.__do_polynomial_best_fit:
                polynomials = np.polyfit(day_of_year_list, temp_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, polynomials, "Temp")

        else:
            north_wind_data = self.return_north_wind_list()
            if self.__want_smoothing:
                north_wind_data = do_smoothing(north_wind_data, self.__smoothing_window_size)
            north_wind_data = np.array(north_wind_data)

            east_wind_data = self.return_east_wind_list()
            if self.__want_smoothing:
                east_wind_data = do_smoothing(east_wind_data, self.__smoothing_window_size)
            east_wind_data = np.array(east_wind_data)

            plt.plot(day_of_year_list, north_wind_data, label='V', color='tab:blue')
            plt.plot(day_of_year_list, east_wind_data, label='U', color='tab:orange')

            if self.__do_polynomial_best_fit:
                north_polynomials = np.polyfit(day_of_year_list, north_wind_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, north_polynomials, "North")

                east_polynomials = np.polyfit(day_of_year_list, east_wind_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, east_polynomials, "East", color="tab:brown")

        plt.grid(visible=True, axis="both")
        title_type = "Temperature between " if graphing_temp else "Wind between "
        location = get_location_string(self.__subfolder)

        title = title_type + begin_month + " and " + end_month + " " + year + " at " + location
        if self.__do_specified_day_of_year_range:
            begin_day, end_day = str(self.__specified_day_of_year_range[0]), str(self.__specified_day_of_year_range[1])
            title = title_type + "day " + begin_day + " and day " + end_day + " " + year + " at " + location
        title += " at altitude level " + altitude
        title = "\n".join(wrap(title))
        plt.title(title, fontsize=25)
        if self.__make_day_marker:
            if self.__do_specified_day_of_year_range:
                begin_day, end_day = self.__specified_day_of_year_range[0], self.__specified_day_of_year_range[1]
                if begin_day <= self.__day_marker_value <= end_day:
                    plt.axvline(x=self.__day_marker_value, color='r',
                                label="Marker for day " + str(self.__day_marker_value))
        plt.legend()

        plt.xlabel("Day of Year", fontsize=20)
        plt.xticks(fontsize=15)
        y_label = "Temperature (K)" if graphing_temp else "Wind Speed (m / s)"
        plt.ylabel(y_label, fontsize=20)
        plt.yticks(fontsize=15)

        save_directory = self.__year_folder + "output_graphs//" + self.__subfolder + "//"
        folder_check_and_maker(save_directory)

        smoothing_file_label = "smoothed_" if self.__want_smoothing else ""
        if self.__do_polynomial_best_fit:
            smoothing_file_label += "degree_" + str(self.__polynomial_best_fit_order) + "_poly_fit_"

        filename_type = "_temp_at_altitude_" if graphing_temp else "_wind_at_altitude_"
        filename = smoothing_file_label + begin_month + "_to_" + end_month
        if self.__do_specified_day_of_year_range:
            begin_day, end_day = str(self.__specified_day_of_year_range[0]), str(self.__specified_day_of_year_range[1])
            filename = smoothing_file_label + begin_day + "_to_" + end_day
        filename += "_" + year + filename_type + altitude + ".png"
        save_path = save_directory + filename
        plt.savefig(save_path)

        plt.close()

    def __generate_month_graph(self, graphing_temp, month_index, first_day_metadata):

        # first_date_number = first_day_metadata[0]  # Commented out because it is never used as of now
        month = first_day_metadata[1]
        # day = first_day_metadata[2]  # Day is commented out because it's never used as of now
        year = first_day_metadata[3]
        altitude = str(self.__current_altitude_value)

        day_of_year_list = self.__get_day_of_year_list_for_month(month_index)
        if self.__want_smoothing:
            day_of_year_list = do_day_of_year_smoothing(day_of_year_list, self.__smoothing_window_size)
        day_of_year_list = np.array(day_of_year_list)

        plt.figure(figsize=(12, 8))

        if graphing_temp:
            temp_data = get_1d_list_from_2d(self.__temperature_data[month_index])
            if self.__want_smoothing:
                temp_data = do_smoothing(temp_data, self.__smoothing_window_size)
            temp_data = np.array(temp_data)
            plt.plot(day_of_year_list, temp_data, label='T')

            if self.__do_polynomial_best_fit:
                polynomials = np.polyfit(day_of_year_list, temp_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, polynomials, "Temp")
        else:
            north_wind_data = get_1d_list_from_2d(self.__north_wind_data[month_index])
            east_wind_data = get_1d_list_from_2d(self.__east_wind_data[month_index])
            if self.__want_smoothing:
                north_wind_data = do_smoothing(north_wind_data, self.__smoothing_window_size)
                east_wind_data = do_smoothing(east_wind_data, self.__smoothing_window_size)
            north_wind_data = np.array(north_wind_data)
            east_wind_data = np.array(east_wind_data)

            plt.plot(day_of_year_list, north_wind_data, label='V')
            plt.plot(day_of_year_list, east_wind_data, label='U')

            if self.__do_polynomial_best_fit:
                north_polynomials = np.polyfit(day_of_year_list, north_wind_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, north_polynomials, "North")

                east_polynomials = np.polyfit(day_of_year_list, east_wind_data, self.__polynomial_best_fit_order)
                add_best_fit_to_graph(plt, day_of_year_list, east_polynomials, "East", color="tab:brown")

        plt.grid(visible=True, axis='both')
        title_type = "Temp in " if graphing_temp else "Wind in "
        location = get_location_string(self.__subfolder)
        title = title_type + month + ' ' + year + " at " + location + " at altitude level " + altitude
        title = "\n".join(wrap(title))
        plt.title(title, fontsize=25)
        if self.__make_day_marker and self.__day_marker_value in day_of_year_list:
            plt.axvline(x=self.__day_marker_value, color='r', label="Marker for day " + str(self.__day_marker_value))
        plt.legend()

        plt.xlabel("Day of Year", fontsize=20)
        plt.xticks(fontsize=15)
        y_label = "Temperature (K)" if graphing_temp else "Wind Speed (m / s)"
        plt.ylabel(y_label, fontsize=20)
        plt.yticks(fontsize=15)

        save_directory = self.__year_folder + "//" + month + "//output_graphs//" + self.__subfolder + "//"
        folder_check_and_maker(save_directory)

        smoothing_file_label = "smoothed_" if self.__want_smoothing else ""
        if self.__do_polynomial_best_fit:
            smoothing_file_label += "degree_" + str(self.__polynomial_best_fit_order) + "_poly_fit_"

        filename_type = "_temp_at_altitude_" if graphing_temp else "_wind_at_altitude_"
        filename = smoothing_file_label + month + year + filename_type + altitude + ".png"
        save_path = save_directory + filename
        plt.savefig(save_path)

        plt.close()

    def __generate_residual_analysis_graph(self, graphing_temp):  # TODO: add alternate method of doing the analysis
        begin_month = self.__start_month
        end_month = self.__end_month
        altitude = str(self.__current_altitude_value)
        year = self.__year

        use_polynomials = self.__residual_analysis_type == "poly"

        day_of_year_list = self.return_day_of_year_list()
        if self.__want_smoothing:
            day_of_year_list = do_day_of_year_smoothing(day_of_year_list, self.__smoothing_window_size)
        day_of_year_list_np = np.array(day_of_year_list)

        plt.figure(figsize=(15, 10))

        if graphing_temp:
            temp_data = self.return_temp_list()
            if self.__want_smoothing:
                temp_data = do_smoothing(temp_data, self.__smoothing_window_size)
            temp_data_np = np.array(temp_data)

            if use_polynomials:
                polynomials = np.polyfit(day_of_year_list_np, temp_data_np, self.__polynomial_best_fit_order)
                subtracted_data = subtract_best_fit_from_data(temp_data, polynomials, day_of_year_list)
                subtracted_data = np.array(subtracted_data)
                poly_order = str(len(polynomials) - 1)
            else:
                unsmoothed_day_of_year_list = day_of_year_list
                day_of_year_list = do_day_of_year_smoothing(day_of_year_list, self.__smoothing_window_size)
                smoothed_temp = do_smoothing(temp_data, self.__smoothing_window_size)
                original_temp = temp_data

                reduce_data_using_date_differences(unsmoothed_day_of_year_list, day_of_year_list, original_temp)
                subtracted_data = np.array(original_temp) - np.array(smoothed_temp)

            plt.plot(day_of_year_list, subtracted_data, label='Temp', color='tab:blue')

        else:
            north_wind_data = self.return_north_wind_list()
            east_wind_data = self.return_east_wind_list()
            if self.__want_smoothing:
                north_wind_data = do_smoothing(north_wind_data, self.__smoothing_window_size)
                east_wind_data = do_smoothing(east_wind_data, self.__smoothing_window_size)
            north_wind_data_np = np.array(north_wind_data)
            east_wind_data_np = np.array(east_wind_data)

            if use_polynomials:
                north_polynomials = np.polyfit(day_of_year_list_np, north_wind_data_np, self.__polynomial_best_fit_order)
                north_subtracted_data = subtract_best_fit_from_data(north_wind_data, north_polynomials, day_of_year_list)
                north_subtracted_data = np.array(north_subtracted_data)

                east_polynomials = np.polyfit(day_of_year_list_np, east_wind_data_np, self.__polynomial_best_fit_order)
                east_subtracted_data = subtract_best_fit_from_data(east_wind_data, east_polynomials, day_of_year_list)
                east_subtracted_data = np.array(east_subtracted_data)
                poly_order = str(len(north_polynomials) - 1)
            else:
                unsmoothed_day_of_year_list = day_of_year_list
                day_of_year_list = do_day_of_year_smoothing(day_of_year_list, self.__smoothing_window_size)

                smoothed_north = do_smoothing(north_wind_data, self.__smoothing_window_size)
                smoothed_east = do_smoothing(east_wind_data, self.__smoothing_window_size)
                original_north = north_wind_data
                original_east = east_wind_data

                reduce_data_using_date_differences(unsmoothed_day_of_year_list, day_of_year_list, original_north)
                reduce_data_using_date_differences(unsmoothed_day_of_year_list, day_of_year_list, original_east)
                north_subtracted_data = np.array(original_north) - np.array(smoothed_north)
                east_subtracted_data = np.array(original_east) - np.array(smoothed_east)

            plt.plot(day_of_year_list_np, north_subtracted_data, label='North Wind', color='tab:blue')
            plt.plot(day_of_year_list_np, east_subtracted_data, label='East Wind', color='tab:orange')

        plt.grid(visible=True, axis="both")
        title_type = "Temperature between " if graphing_temp else "Wind between "
        location = get_location_string(self.__subfolder)
        if use_polynomials:
            title = "\n".join(wrap("Order " + poly_order + " Residual Analysis of " + title_type + begin_month + " and "
                                   + end_month + " " + year + " at " + location + " at altitude level " + altitude))
            if self.__do_specified_day_of_year_range:
                begin_day = str(self.__specified_day_of_year_range[0])
                end_day = str(self.__specified_day_of_year_range[1])
                title = "\n".join(wrap("Order " + poly_order + " Residual Analysis of " + title_type + "day " +
                                       begin_day + " and day " + end_day + " " + year + " at " + location +
                                       " at altitude level " + altitude))
        else:
            title = "\n".join(wrap("Residual Analysis from 4-day smoothed graph of " + title_type + begin_month +
                                   " and " + end_month + " " + year + " at " + location + " at altitude level " +
                                   altitude))
            if self.__do_specified_day_of_year_range:
                begin_day = str(self.__specified_day_of_year_range[0])
                end_day = str(self.__specified_day_of_year_range[1])
                title = "\n".join(wrap("Residual Analysis from 4-day smoothed graph of " + title_type + "day " +
                                       begin_day + " and day " + end_day + " " + year + " at " + location +
                                       " at altitude level " + altitude))

        plt.title(title, fontsize=25)

        if self.__make_day_marker:
            if self.__do_specified_day_of_year_range:
                begin_day, end_day = self.__specified_day_of_year_range[0], self.__specified_day_of_year_range[1]
                if begin_day <= self.__day_marker_value <= end_day:
                    plt.axvline(x=self.__day_marker_value, color='r',
                                label="Marker for day " + str(self.__day_marker_value))

        plt.xlabel("Day of Year", fontsize=20)
        plt.xticks(fontsize=15)
        plt.axhline(y=0, color='black')
        y_label = "Temperature (K)" if graphing_temp else "Wind Speed (m / s)"
        plt.ylabel(y_label, fontsize=20)
        plt.yticks(fontsize=15)

        save_directory = self.__year_folder + "output_graphs//" + self.__subfolder + "//"
        folder_check_and_maker(save_directory)

        smoothing_string = "of_smoothed_" if self.__want_smoothing else ""
        filename_type = "_temp_at_altitude_" if graphing_temp else "_wind_at_altitude_"
        analysis_type = "residual_analysis_polynomial_" if use_polynomials else "residual_analysis_smoothed_"

        filename = analysis_type + smoothing_string + "from_" + begin_month + "_to_" + end_month
        if self.__do_specified_day_of_year_range:
            begin_day = str(self.__specified_day_of_year_range[0])
            end_day = str(self.__specified_day_of_year_range[1])
            filename = analysis_type + smoothing_string + "from_day_" + begin_day + "to_day_" + end_day
        filename += "_" + year + filename_type + altitude + ".png"
        save_path = save_directory + filename
        plt.savefig(save_path)

        plt.close()

    def __make_graphs_all_altitudes(self):
        for i in range(1, 73):
            self.__current_altitude_value = i
            if self.__temp_data_loaded:
                self.set_temp_data()
            if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
                self.set_wind_data()
            self.__make_graphs_for_current_altitude()

    def __make_graphs_every_other_altitude(self):
        for i in range(1, 73, 2):
            self.__current_altitude_value = i
            if self.__temp_data_loaded:
                self.set_temp_data()
            if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
                self.set_wind_data()
            self.__make_graphs_for_current_altitude()

    def __make_graphs_specified_altitudes(self):
        for altitude in self.__specified_altitudes:
            self.__current_altitude_value = altitude
            if self.__temp_data_loaded:
                self.set_temp_data()
            if self.__north_wind_data_loaded and self.__east_wind_data_loaded:
                self.set_wind_data()
            self.__make_graphs_for_current_altitude()

    def __get_day_of_year_list_for_year(self):
        temp_filenames = self.__temperature_filenames_1D

        first_day_of_year_number = int(get_file_metadata(temp_filenames[0])[0])
        day_count = len(temp_filenames)
        number_data_points_per_day = 8
        day_list = []
        for i in range(day_count):
            date_number = first_day_of_year_number + i
            for j in range(number_data_points_per_day):
                day_list.append(date_number + j * 1 / number_data_points_per_day)
        return day_list

    def __get_day_of_year_list_for_month(self, month_index):
        this_month_filenames = self.__temperature_filenames[month_index]
        first_day_doy = get_file_metadata(this_month_filenames[0])[0]
        day_of_year_list = []
        for i in range(len(this_month_filenames)):
            date_number = int(first_day_doy) + i
            for j in range(8):
                day_of_year_list.append(date_number + j * .125)
        return day_of_year_list

    def __make_month_list(self):
        month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "December"]

        relevant_months = []
        for month in month_list:
            month_path = self.__year_folder + month + "//"
            if exists(month_path):
                relevant_months.append(month)

        return relevant_months

    def __make_filename_list(self, type_char):
        """
        Makes 2-D array where each internal array has each month's filenames inside
        :param type_char: "T" for temp, "V" for north wind, "U" for east wind
        :return: 2-D array of all the year's filenames, separated by month
        """
        filenames_by_month = []
        for month in self.__months:
            month_path = self.__year_folder + month + "//IDL_data_exports//" + self.__subfolder + "//"
            filenames_by_month.append(file.get_relevant_filenames(month_path, type_char))

        return filenames_by_month

    def __check_filename_continuity(self):
        for month in self.__north_wind_filenames:
            confirm_month_unbroken_data(month)
        for month in self.__east_wind_filenames:
            confirm_month_unbroken_data(month)
        for month in self.__temperature_filenames:
            confirm_month_unbroken_data(month)

        # Make sure months are continuous with each other
        self.__check_continuity_between_months()
        # Check that all three data sets use data over the same time period
        self.__check_continuity_between_datasets()

    def __check_continuity_between_datasets(self):
        temp_first_day_metadata = get_file_metadata(self.__temperature_filenames[0][0])
        north_first_day_metadata = get_file_metadata(self.__north_wind_filenames[0][0])
        east_first_day_metadata = get_file_metadata(self.__east_wind_filenames[0][0])

        # Make sure that the different winds have the same data over the same period
        doesnt_start_same_day = north_first_day_metadata[0] != east_first_day_metadata[0] != temp_first_day_metadata[0]
        not_same_length = len(self.__north_wind_filenames_1D) != len(
            self.__east_wind_filenames_1D) != len(self.__temperature_filenames_1D)

        if doesnt_start_same_day or not_same_length:
            print("The two wind types' and the temperature's files must cover the same days.")
            sleep(5)
            quit()

    def __check_continuity_between_months(self):
        # Make sure months are continuous with each other
        for i in range(len(self.__temperature_filenames) - 1):
            # Figure out what the last day of the month should be for it to be continuous
            month = get_file_metadata(self.__temperature_filenames[i][0])[1]
            if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or \
                    month == "October" or month == "December":
                days_in_month = "31"
            elif month == "April" or month == "June" or month == "September" or month == "November":
                days_in_month = "30"
            else:
                if int(get_file_metadata(self.__temperature_filenames[i][0])[3]) % 4 == 0:
                    days_in_month = "29"
                else:
                    days_in_month = "28"

            begin_month_last_day = get_file_metadata(self.__temperature_filenames[i][-1])[2]
            end_month_first_day = get_file_metadata(self.__temperature_filenames[i + 1][0])[2]
            is_continuous = begin_month_last_day == days_in_month and end_month_first_day == "01"
            if not is_continuous:
                print("The data must be continuous between months")
                sleep(5)
                quit()

    def __get_data(self, filename_list):
        """
        Returns a 3-D list of the data at the filenames
        :param filename_list: the filename list to be used
        :return: 3-D list month->day->each data value at each 3-hour interval on that day
        """
        return_list = []
        for month_of_filenames in filename_list:
            data_by_day = []
            for i in range(len(month_of_filenames)):
                day_of_data = file.read_dat_file(month_of_filenames[i], self.__current_altitude_value)
                data_by_day.append(day_of_data)
            return_list.append(data_by_day)
        return return_list

    def return_day_of_year_list(self):
        """
        Returns the day of year list (with values between the integer days, representing the values within the days, so
        for example, [120, 120.2, 120.4, ..., 121, ...]. If there is a specified doy range, only data within that range
        is returned)
        :return: 1-D array of the day of year data
        """
        day_of_year_list = self.__get_day_of_year_list_for_year()
        output_list = day_of_year_list
        if self.__do_specified_day_of_year_range:
            day_range = self.__specified_day_of_year_range
            output_list = []
            for i in range(len(day_of_year_list)):
                current = day_of_year_list[i]
                if day_range[0] <= current < day_range[1] + 1:  # +1 because we need to include all of that day's data
                    output_list.append(current)
        return output_list

    def return_temp_list(self):
        """
        Returns the temperature data. If a date range is specified, this is reflected in the data returned.
        :return: 1-D array of the temperature data
        """
        if self.__temp_data_loaded:
            return self.__return_data_list('T')
        else:
            print("Sorry, this data isn't loaded.")

    def return_north_wind_list(self):
        """
        Returns the north wind data. If a date range is specified, this is reflected in the data returned.
        :return: 1-D array of the north wind data
        """
        if self.__north_wind_data_loaded:
            return self.__return_data_list('V')
        else:
            print("Sorry, this data isn't loaded.")

    def return_east_wind_list(self):
        """
        Returns the east wind data. If a date range is specified, this is reflected in the data returned.
        :return: 1-D array of the east wind data
        """
        if self.__east_wind_data_loaded:
            return self.__return_data_list('U')
        else:
            print("Sorry, this data isn't loaded.")

    def __return_data_list(self, data_type):
        if self.__specified_day_of_year_range:
            if data_type == 'T':
                data = get_1d_list_from_3d(self.__temperature_data)
            elif data_type == 'V':
                data = get_1d_list_from_3d(self.__north_wind_data)
            else:
                data = get_1d_list_from_3d(self.__east_wind_data)
            reduce_data_using_date_differences(self.__get_day_of_year_list_for_year(),
                                               self.return_day_of_year_list(),
                                               data)
            return data
        else:
            if data_type == 'T':
                return get_1d_list_from_3d(self.__temperature_data)
            elif data_type == 'V':
                return get_1d_list_from_3d(self.__north_wind_data)
            else:
                return get_1d_list_from_3d(self.__east_wind_data)

    def return_begin_and_end_months(self):
        return self.__start_month, self.__end_month

    def return_year(self):
        return self.__year

    def return_subfolder(self):
        return self.__subfolder


def reduce_data_using_date_differences(original_day_of_year_list, edited_day_of_year_list, data_list):
    """
    Modifies the data_list based off of comparing the original doy list with the edited doy list. Original doy list and
    data_list should be the same length.
    :param original_day_of_year_list: unedited day of year list, should be same len as data_list
    :param edited_day_of_year_list: changed day of year list that you want reflected in the data_list
    :param data_list: temp, wind, etc data to be cut down to match the changed day of year list. This list will be
    modified
    :return: Nothing returned. data_list modified
    """
    same_length = len(original_day_of_year_list) == len(data_list)
    if not same_length:
        print("Invalid, need same length")
        return
    else:
        indexes_to_delete = []
        for i in range(len(original_day_of_year_list)):
            value = original_day_of_year_list[i]
            if value not in edited_day_of_year_list:
                indexes_to_delete.append(i)

        current_list_index = len(indexes_to_delete) - 1
        while current_list_index >= 0:
            data_list.pop(indexes_to_delete[current_list_index])
            current_list_index -= 1


def get_location_string(subfolder_string):
    outstring = subfolder_string
    if "minus" in subfolder_string:
        value = 0
        string_length = len(subfolder_string)
        for i in range(string_length):
            current_character = subfolder_string[i]
            if current_character == "#":
                value = int(subfolder_string[i + 1:])
                break
        minus_amount = str(value * 15)
        outstring = "McMurdo minus " + minus_amount + " degrees longitude"
    return outstring


def do_smoothing(array, window_size):
    i = 0
    moving_averages = []

    while i < len(array) - window_size:
        window_average = round(np.sum(array[i:i + window_size]) / window_size, 2)
        moving_averages.append(window_average)
        i += 1

    return moving_averages


def do_day_of_year_smoothing(array, window_size):
    out_list = []
    for value in array:  # Copy the array to not modify the original
        out_list.append(value)
    assert(window_size % 16 == 0)  # Want whole days taken from each side only
    front_pop_count = window_size // 2
    back_pop_count = window_size // 2
    for i in range(front_pop_count):
        out_list.pop(0)
    for i in range(back_pop_count):
        out_list.pop()
    return out_list


def subtract_best_fit_from_data(data, polynomials, day_of_year_list):
    subtracted_data = []
    for i in range(len(day_of_year_list)):
        day_value = day_of_year_list[i]
        total_to_subtract = 0
        # Highest coefficient first
        power = len(polynomials) - 1
        for polynomial in polynomials:
            total_to_subtract += polynomial * pow(day_value, power)
            power -= 1
        sub_data = data[i] - total_to_subtract
        subtracted_data.append(sub_data)
    return subtracted_data


def add_best_fit_to_graph(plot, x_data, polynomials, data_type, color="tab:green"):
    """
    Adds a best-fit line to the given plot
    :param plot: plt object to add the line to
    :param x_data: x-axis data to expand
    :param polynomials: polynomials to apply to the data to get the values
    :param data_type: Temp, North, or East
    :param color: default: "tab:green", other options include "tab:brown", "tab:gray", etc
    :return: None, just changes the plt object
    """
    x_fit = np.linspace(min(x_data), max(x_data), 1000)
    y_fit = np.polyval(polynomials, x_fit)

    poly_order = len(polynomials) - 1

    plot.plot(x_fit, y_fit, label='Order ' + str(poly_order) + ' best fit - ' + data_type, color=color)


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

    is_unbroken = int(first_data[2]) + list_length - 1 == int(last_data[2]) and int(
        first_data[2]) + middle_index == int(middle_data[2])
    is_same_month = first_data[1] == last_data[1] == middle_data[1]

    if not is_unbroken or not is_same_month:
        print("Need unbroken line of data in the same month! Month:" + first_data[1])
        sleep(5)
        quit()


def get_1d_list_from_2d(inlist):
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


def get_1d_list_from_3d(inlist):
    """
    Takes 3-D list and returns a 1-D list in order of the values
    :param inlist: 3-D list
    :return: 1-D list version of inlist
    """
    out_list = []
    for inner_list in inlist:
        out_list.append(get_1d_list_from_2d(inner_list))
    return get_1d_list_from_2d(out_list)


def grapher(year_filepath, subfolder, graph_temp=True, graph_winds=True,
            graph_months=False, graph_year=False, altitude_level=1,
            do_all_altitudes=False, do_every_other_altitude=False, specified_altitudes=None, day_emphasis_bar=None,
            smoothing=False, polynomial_best_fit=None, residual_analysis_graph=False, residual_analysis_type="poly",
            specified_date_range=None,
            graphing_multiple_locations=None, graph_all_locations_one_day_day=None):
    """
    Graphs MERRA-2 data given after IDE processing
    :param year_filepath: filepath of the year of data (with month sub-folders) to graph
    :param subfolder: the folder in which you find the .dat input files, the folder below //IDL_data_exports//
    :param graph_temp: True to get temp graphs, False to not get temp graphs
    :param graph_winds: True to get wind graphs, False to not get wind graphs
    :param graph_year: True to get graph of the whole year (that's in the file system)
    :param graph_months: True to get graph of the individual months in the year
    :param altitude_level: altitude level (int 1-72) you want
    :param do_all_altitudes: True to get graphs of all altitudes
    :param do_every_other_altitude: True to get graphs of every other altitude
    :param specified_altitudes: Pass a list of integers from 1-72 to have those altitude levels graphed
    :param day_emphasis_bar: input int to get a bar on the day you put in
    :param smoothing: True to get a graph that has moving average smoothing done to it
    :param polynomial_best_fit: Put int int (2,3,etc) for a best-fit line of the data of that order
    :param residual_analysis_graph: True to get a graph of the residual analysis. (The graph subtracted by the best-fit
    base) If using a polynomials as the base, specify order in polynomial_best_fit variable. 2nd order default. Won't
    output graphs with the poly line on the normal graph. If smoothing=True, the polynomials will be calculated by and
    subtracted from the smoothed data. If false, the same will be done using the original data. If using the smoothed
    data as the base to be subtracted from, smoothing will be turned off for the data, and the smoothed data will be
    subtracted from it to get the residual.
    :param residual_analysis_type: sets the base residual analysis. "poly" for polynomial-best-fit line, "smoothed" to
    use the smoothed line.
    :param specified_date_range: None for nothing, [start_int, end_int] to plot that range of data. Ex: [3, 15]
    :param graphing_multiple_locations: None only use subfolder data, input list of subfolder names to graph all of
    that data on the same plot. Ex: ["McMurdo", "Davis", "McMurdo_minus_15#20"]
    :param graph_all_locations_one_day_day: If int inputted, graph of all locations' data at hour 0 of that day
    :return: graphs saved to //output_graphs in the month_filepath / year_filepath
    """
    if isinstance(graphing_multiple_locations, list):
        graph_multiple_locations_for_year(graphing_multiple_locations, year_filepath, graph_temp, graph_winds, altitude_level,
                                          day_emphasis_bar, smoothing, specified_date_range)
        return
    if isinstance(graph_all_locations_one_day_day, int):
        graph_all_locations_one_day(year_filepath, graph_temp, graph_winds, altitude_level,
                                    graph_all_locations_one_day_day)
        return

    merra_object = Merra(year_filepath, subfolder)
    merra_object.set_altitude_level(altitude_level)

    if graph_temp:
        merra_object.set_temp_data()
    if graph_winds:
        merra_object.set_wind_data()

    if graph_months:
        merra_object.set_monthly_graphs_toggle(True)
    if graph_year:
        merra_object.set_year_graph_toggle(True)

    if isinstance(day_emphasis_bar, int):
        merra_object.set_day_marker(True, day_emphasis_bar)

    if smoothing:
        merra_object.set_smoothing_toggle(smoothing)
    if isinstance(polynomial_best_fit, int):
        merra_object.set_polynomial_fit_order(polynomial_best_fit)

    if residual_analysis_graph:
        merra_object.set_residual_analysis_toggle(residual_analysis_graph, residual_analysis_type)

    if do_all_altitudes:
        merra_object.set_do_all_altitudes_toggle(True)
    elif do_every_other_altitude:
        merra_object.set_do_every_other_altitude_toggle(True)
    elif isinstance(specified_altitudes, list):
        merra_object.set_specified_altitudes(specified_altitudes)

    if isinstance(specified_date_range, list):
        merra_object.set_specified_date_range(specified_date_range)

    merra_object.make_graphs()
