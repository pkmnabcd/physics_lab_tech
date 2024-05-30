import os
from metadata_gathering import get_file_metadata


def read_dat_file(filename, altitude_number):
    """
    This reads the data from the given file at the given altitude
    :param filename: the filename of the data file to be read
    :param altitude_number: the altitude level you want read (int between 1 and 72)
    :return: a list of the data at the file and altitude level
    """
    file = open(filename, 'r')

    for i in range(altitude_number):
        line = file.readline()
    line_length = len(line)
    column_length = 15
    number_of_columns = line_length // column_length
    number_list = []

    for i in range(number_of_columns):
        index_start = i * column_length
        index_end = index_start + column_length
        substring = line[index_start: index_end]
        number_list.append(float(substring))
    return number_list


# def selection_sort(number_list, filename_list):
#     for i in range(len(number_list) - 2):
#         start_index = i
#         current_min_index = start_index
#         test_index = start_index + 1
#         swap_needed = False
#
#         while test_index < len(number_list) - 1:
#             if number_list[test_index] < number_list[current_min_index]:
#                 swap_needed = True
#                 current_min_index = test_index
#             test_index += 1
#         if swap_needed:
#             number_temp = number_list[current_min_index]
#             filename_temp = filename_list[current_min_index]
#             number_list[current_min_index] = number_list[start_index]
#             filename_list[current_min_index] = filename_list[start_index]
#             number_list[start_index] = number_temp
#             filename_list[start_index] = filename_temp
def selection_sort(obj_list):
    for start_index in range(len(obj_list) - 1):
        current_min_index = start_index
        current_min = obj_list[current_min_index]

        for test_index in range(start_index + 1, len(obj_list)):
            if obj_list[test_index] < current_min:
                current_min = obj_list[test_index]
                current_min_index = test_index
        if current_min_index != start_index:
            obj_list[current_min_index] = obj_list[start_index]
            obj_list[start_index] = current_min


def get_relevant_filenames(path, data_category):
    """
    Gets the file names of all the files in the inputted directory and returns a list of those with the given data type
    Also makes sure that the list is sorted in case the files aren't automatically inputted correctly
    :param path: the folder in which the data files are in, should be IDL_data_exports
    :param data_category: the character on the filename that denotes which data type it is: V North, U East, T temp
    :return: a list with all the file names of that data category
    """
    files_with_this_data_category = []
    for file in os.listdir(path):
        if file.startswith(data_category):
            files_with_this_data_category.append(path + file)

    files_with_this_data_category.sort()

    # # Properly sort the days
    # metadata_list = []
    # for filename in files_with_this_data_category:
    #     metadata_list.append(get_file_metadata(filename))
    # # Make list of day of year numbers
    # day_of_year_list = []
    # for item in metadata_list:
    #     day_of_year_list.append(item[0])
    #
    # # Sort that list of numbers, and everything I move in this list, also move in the output list
    # selection_sort(day_of_year_list, files_with_this_data_category)
    #
    # return files_with_this_data_category
    filename_obj_list = []
    for filename in files_with_this_data_category:
        filename_obj_list.append(Filename(filename))

    selection_sort(filename_obj_list)

    filename_list = []
    for filename_obj in filename_obj_list:
        filename_list.append(filename_obj.get_filename())

    return filename_list


class Filename:

    def __init__(self, filename):
        self.__filename = filename
        self.__metadata_list = get_file_metadata(filename)
        self.__day_of_year = int(self.__metadata_list[0])

    def __lt__(self, other):
        return self.get_day_of_year() < other.get_day_of_year()

    def get_day_of_year(self):
        return self.__day_of_year

    def get_filename(self):
        return self.__filename
