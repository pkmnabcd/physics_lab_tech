import sys
import os.path

from parser import read_file, get_metadata
import grapher


def check_or_make_dir(directory):
    if directory == "":
        return
    if not os.path.exists(directory):
        os.mkdir(directory)


def get_data_type_index(data_type: str, headers_list: list):
    index = headers_list.index(data_type)
    return index


def add_date_to_metadata(date_col_header: str, metadata_dict: dict):
    date_end = len(date_col_header) - 3
    date = date_col_header[0:date_end]
    metadata_dict["date"] = date


def separateFilenameAndDirectory(file_path: str):
    last_slash_index = -1
    for i in range(len(file_path)):
        if file_path[i] == '/':
            last_slash_index = i

    file_dir = file_path[:last_slash_index + 1]
    filename = file_path[last_slash_index + 1:]
    return filename, file_dir


if __name__ == "__main__":
    file_path = sys.argv[1]
    filename, file_dir = separateFilenameAndDirectory(file_path)

    data, col_headers = read_file(file_path)
    if data == None and col_headers == None:
        print("Empty file detected. No graph was saved.", file=sys.stderr)
        exit(1)

    metadata = get_metadata(filename)
    add_date_to_metadata(col_headers[0], metadata)

    OH_headers_present = "OHTemp" in col_headers and "OHBandInt" in col_headers
    CCD_present = "CCDTemp" in col_headers
    filters_present = "P12" in col_headers and "P14" in col_headers and "BG" in col_headers and "ActDark" in col_headers
    if not (OH_headers_present and CCD_present and filters_present):
        print("ERROR: At least one column is missing or misspelled.")
        exit(1)

    P12_index = get_data_type_index("P12", col_headers)
    P14_index = get_data_type_index("P14", col_headers)
    BG_index = get_data_type_index("BG", col_headers)
    Dark_index = get_data_type_index("ActDark", col_headers)

    OH_temp_index = get_data_type_index("OHTemp", col_headers)
    OH_band_index = get_data_type_index("OHBandInt", col_headers)
    CCD_temp_index = get_data_type_index("CCDTemp", col_headers)

    # Change this and combined graph so it doesn't use the SingleGraph objects anymore
    # Changes should end here
    data_map = {
	col_headers[P12_index]: data[P12_index],
	col_headers[P14_index]: data[P14_index],
	col_headers[BG_index]: data[BG_index],
	col_headers[Dark_index]: data[Dark_index],
	col_headers[OH_temp_index]: data[OH_temp_index],
	col_headers[OH_band_index]: data[OH_band_index],
	col_headers[CCD_temp_index]: data[CCD_temp_index],
    }
    
    combined_graph = grapher.CombinedGraph(data_map, metadata, data[0])
    combined_graph.generate_graph()

    save_dir = file_dir
    check_or_make_dir(save_dir)
    combined_graph.save_graph(save_dir)
