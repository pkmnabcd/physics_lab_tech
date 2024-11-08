def get_file_metadata(filename_string):
    """
    This gets most of the metadata that the program will be using by looking at the filename
    :param filename_string: The filename string that the function will use to get the metadata
    :return: a list of the metadata in the form [day_of_year, month, day, year] all in string type
    """
    substring_start_index = filename_string.index("day")

    substring = filename_string[substring_start_index:]

    day_of_year = get_day_of_year_string(substring)

    date_index_start = substring.index('_') + 1
    date_string = substring[date_index_start:date_index_start + 4]
    month_int = int(date_string[0:2])
    day = date_string[2:]
    month = get_month_string(month_int)
    year = get_year(substring)

    return [day_of_year, month, day, year]


def get_month_string(month_int):
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return months[month_int - 1]


def get_day_of_year_string(substring):
    index = 3
    out_string = ""
    while substring[index].isdigit():
        out_string += substring[index]
        index += 1

    return out_string


def get_year(substring):
    index_start = substring.index("10by10") - 5
    year = substring[index_start:index_start + 4]
    return year
