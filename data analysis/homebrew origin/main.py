import sys
from parser import read_file, get_metadata


def add_date_to_metadata(date_col_header: str, metadata_dict: dict):
    date_end = len(date_col_header) - 3
    date = date_col_header[0:date_end]
    metadata_dict["date"] = date


class Graph:
    def __init__(self, data_array, ):

if __name__ == "__main__":
    filename = sys.argv[1]
    data, col_headers = read_file(filename)
    metadata = get_metadata(filename)
    add_date_to_metadata(col_headers[0], metadata)

    OH_headers_present = "OHTemp" in col_headers and "OHBandInt" in col_headers
    CCD_present = "CCDTemp" in col_headers
    filters_present = "P12" in col_headers and "P14" in col_headers and "BG" in col_headers and "ActDark" in col_headers
    if not (OH_headers_present and CCD_present and filters_present):
        print("ERROR: At least one column is missing or misspelled.")
        exit(1)


