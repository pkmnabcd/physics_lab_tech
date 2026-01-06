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


def filterImagesBeforeIndex(cutoff_index, images, number_start):
    filteredImages = []
    for image in images:
        index_str = image[number_start:number_start+4]
        index = int(index_str)
        if index >= cutoff_index:
            filteredImages.append(image)

    return filteredImages


def main():
    path = "./data"  # TODO: change this to "." once I'm done testing
    processed_path = join(path, "Processed")
    all_raw_files = [f for f in listdir(path) if isfile(join(path, f))]
    all_processed_files = [f for f in listdir(processed_path) if isfile(join(processed_path, f))]

    tmp_folder_path = join(path, "tmp_backup")
    tmp_folder_path_processed = join(tmp_folder_path, "Processed")
    if exists(tmp_folder_path):
        return  # NOTE: don't want to overwrite existing copies or redo the renaming

    mkdir(tmp_folder_path)
    mkdir(tmp_folder_path_processed)

    raw_file_patterns = ["BG_31_[0-9]{4}.tif", "P12_31_[0-9]{4}.tif", "P14_31_[0-9]{4}.tif"]
    raw_bg_files = getMatchingFiles(raw_file_patterns[0], all_raw_files)
    raw_p12_files = getMatchingFiles(raw_file_patterns[1], all_raw_files)
    raw_p14_files = getMatchingFiles(raw_file_patterns[2], all_raw_files)

    print("Making copies of the raw data")
    for file in all_raw_files:
        copy2(join(path, file), tmp_folder_path)
    print("Making copies of the processed data")
    for file in all_processed_files:
        copy2(join(processed_path, file), tmp_folder_path_processed)

    print("Filtering out images that are below the cutoff index")
    incorrect_bg = filterImagesBeforeIndex(first_incorrect_index, raw_bg_files, 6)
    incorrect_p12 = filterImagesBeforeIndex(first_incorrect_index, raw_p12_files, 7)
    incorrect_p14 = filterImagesBeforeIndex(first_incorrect_index, raw_p14_files, 7)


main()
