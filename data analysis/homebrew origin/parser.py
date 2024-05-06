def read_file(filename):
    """
    This reads the data from the given file
    :param filename: the filename of the data file to be read
    :return: a list of the data at the file and the column headers of the file in a tuple (data, col_headers)
    """
    # TODO: add code to parse NaN and ***** data
    file = open(filename, 'r')
    lines = file.readlines()
    header_line = lines.pop(0)

    line_length = len(header_line)
    column_length = 15
    number_of_columns = line_length // column_length

    output_list = []

    for line in lines:
        line = line.strip("\n")
        line_data = []

        for i in range(number_of_columns):
            index_start = i * column_length
            index_end = index_start + column_length
            substring = line[index_start: index_end]
            if substring == "***************":
                line_data.append(float("NaN"))
            line_data.append(float(substring))
        output_list.append(line_data)

    header_list = []
    for i in range(number_of_columns):
        index_start = i * column_length
        index_end = index_start + column_length
        substring = header_line[index_start: index_end]
        substring = substring.replace(" ", "")
        header_list.append(substring)

    return output_list, header_list


def get_metadata(filename: str):
    """
    Filenames are like this: OH_Andover_ALO23day291.dat
    or OH_Andover_ALOYYdayDDD.dat
    :param filename:
    :return:
    """
    metadata = {}
    date = filename.replace("OH_Andover_ALO", "").replace(".dat", "")
    year_stub, day_of_year = tuple(date.split("day"))

    metadata["year"] = "20" + year_stub
    metadata["day_of_year"] = day_of_year
    return metadata
