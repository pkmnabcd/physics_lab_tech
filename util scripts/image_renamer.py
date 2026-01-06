from os import listdir, mkdir
from os.path import isfile, join, exists
from re import compile
from shutil import copy2


first_incorrect_index = 253


def getMatchingFiles(pattern, all_files):
    matching_files = []
    regex = compile(pattern)
    for file in all_files:
        if regex.match(file):
            matching_files.append(file)
    return matching_files



def main():
    path = "./data"  # TODO: change this to "." once I'm done testing
    all_files = [f for f in listdir(path) if isfile(join(path, f))]

    tmp_folder_path = join(path, "tmp_backup")
    tmp_folder_already_exists = exists(tmp_folder_path)
    if not tmp_folder_already_exists:
        mkdir(tmp_folder_path)

    raw_file_patterns = ["BG_31_[0-9]{4}.tif", "P12_31_[0-9]{4}.tif", "P14_31_[0-9]{4}.tif"]
    raw_bg_files = getMatchingFiles(raw_file_patterns[0], all_files)
    raw_p12_files = getMatchingFiles(raw_file_patterns[1], all_files)
    raw_p14_files = getMatchingFiles(raw_file_patterns[2], all_files)

    if not tmp_folder_already_exists:  # NOTE: don't want to overwrite existing copies
        print("Making copies of the raw data")
        for file in raw_bg_files:
            copy2(join(path, file), tmp_folder_path)
        for file in raw_p12_files:
            copy2(join(path, file), tmp_folder_path)
        for file in raw_p14_files:
            copy2(join(path, file), tmp_folder_path)


main()
