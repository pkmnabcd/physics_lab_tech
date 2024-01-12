"""
This program will check the unprocessed directory to determine what processed folders could exist, then to see if there
exists a processed folders for each potential month. Then the user can input which processed folders they do or do not
want made. Then it makes all of those directories except for those that the user doesn't want.

Note: the "processed" directory must already be made for this to work. This program makes the individual night's folders
 within the processed directory.
"""

import os.path
from time import sleep


def main():
    # Set the outside directory
    YEAR = '2023'  # Year will be a constant to save time
    initial_path = 'I://ChileMTM//' + YEAR
    print("Year = " + str(YEAR))
    month = input('Enter the month (3 letters): ').capitalize()
    initial_path += "//" + month + YEAR + "//"

    present_unprocessed, present_processed, missing_processed = find_folders(initial_path, month)
    folders_to_make = get_do_add_list(missing_processed)
    make_folders(folders_to_make, path_stub=initial_path + 'processed//' + month)
    print("Folders were created")
    sleep(3)


def find_folders(initial_path, month):
    # This loop finds all the path ending names that already exist
    unprocessed_folders = []
    for i in range(31):
        # This if-else-if series determines which ending to put on the path name
        # Path name in the form 10-11
        if i < 8:
            path_ending = "0" + str(i + 1) + "-0" + str(i + 2)
        elif i == 8:
            path_ending = "09-10"
        elif i == 30:
            path_ending = "31-01"
        else:
            path_ending = str(i + 1) + "-" + str(i + 2)
        # Adding a case just below for when it's the end of the month on the 28th 29th or 30th

        # Checks if that day's unprocessed folder is present
        path = initial_path + month + path_ending
        if os.path.exists(path):
            unprocessed_folders.append(path_ending)
        elif not os.path.exists(path) and (i == 27 or i == 28 or i == 29):  # Tests to see if it's the end of the month
            path = initial_path + month + str(i + 1) + "-01"
            if os.path.exists(path):
                path_ending = str(i + 1) + "-01"
                unprocessed_folders.append(path_ending)

    # Checks all the found unprocessed paths for if a processed folder exists
    initial_path += 'processed//' + month
    processed_folders = []
    missing_processed = []
    for i in unprocessed_folders:
        path = initial_path + i  # Appends each found unprocessed path ending
        if os.path.exists(path):
            processed_folders.append(i)
        else:
            missing_processed.append(i)
    return unprocessed_folders, processed_folders, missing_processed


def get_do_add_list(missing_processed):
    done = False
    selected = []
    while not done:
        ending = user_input(missing_processed, selected)
        if ending == -1:
            done = True
        else:
            selected.append(ending)
    output_list = []
    for path_ending in missing_processed:
        if selected.count(path_ending) == 0:
            output_list.append(path_ending)

    return output_list


def user_input(in_list, selected):
    count = 0
    print('\nThese folders will be created. Select those you don\'t want made')
    for i in in_list:
        print('\t' + str(count) + ') ' + i, end='')
        if selected.count(i) > 0:
            print(' (Selected)')
        else:
            print()
        count += 1

    index = input("Enter one that you want to not make, otherwise, hit enter: ")
    if index == "":
        return -1
    else:
        return in_list[int(index)]


def make_folders(folder_endings, path_stub):
    for ending in folder_endings:
        os.mkdir(path_stub + ending)


main()
