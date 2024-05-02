def read_file(filename):
    """
    This reads the data from the given file
    :param filename: the filename of the data file to be read
    :return: a list of the data at the file and the column headers of the file in a tuple (data, col_headers)
    """
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
