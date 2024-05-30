def read_file(filename):
    """
    This reads the data from the given file. If invalid data is given, float("NaN") is used.
    :param filename: the filename of the data file to be read
    :return: a list of the data at the file and the column headers of the file in a tuple (data, col_headers)
    """
    file = open(filename, 'r')
    lines = file.readlines()
    header_line = lines.pop(0)

    line_length = len(header_line)
    column_length = 15
    number_of_columns = line_length // column_length

    row_set = []

    for line in lines:
        line = line.strip("\n")
        line_data = []

        for i in range(number_of_columns):
            index_start = i * column_length
            index_end = index_start + column_length
            substring = line[index_start: index_end]
            if substring == "***************":
                line_data.append(float("NaN"))
            else:
                line_data.append(float(substring))
        row_set.append(line_data)

    col_set = convert_row_set_to_col_set(row_set)

    header_list = []
    for i in range(number_of_columns):
        index_start = i * column_length
        index_end = index_start + column_length
        substring = header_line[index_start: index_end]
        substring = substring.replace(" ", "")
        header_list.append(substring)

    return col_set, header_list


def get_metadata(filename: str):
    """
    Takes a zenus data filename and outputs a dictionary with the day of year and year inside.
    :param filename: filename like this: OH_Andover_ALO23day1.dat or OH_Andover_ALO08day300.dat
    :return: a dict with the key:values  "year" and "day_of_year", where "year" is 20YY.
    """
    metadata = {}
    date = filename.replace("OH_Andover_ALO", "").replace(".dat", "")
    year_stub, day_of_year = tuple(date.split("day"))

    metadata["year"] = "20" + year_stub
    metadata["day_of_year"] = day_of_year
    return metadata


def convert_row_set_to_col_set(dataset):
    row_total = len(dataset)
    col_total = len(dataset[0])
    col_set = []
    for i in range(col_total):
        col_set.append([])

    for i in range(row_total):
        for j in range(col_total):
            col_set[j].append(dataset[i][j])
    return col_set
