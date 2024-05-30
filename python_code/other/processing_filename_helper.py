"""
Purpose of this program:
The user (after selecting a mode) will input the starting and ending numbers for the files to be processed. 
Once the user submits this info, the program will (depending on the mode) print the filenames required to process the night of images.

This is best used for ChileMTM because processing takes relatively little time, and you have to do little processes repeatedly. This will help save time with that.

"""


# This function takes the beginning and ending numbers
def get_beginning_and_end():
    print()
    FORMATTING = "04d"
    begin = int(input('Enter the beginning number: '))
    ending = int(input('Enter the ending number: '))
    begin = format(begin, FORMATTING)
    ending = format(ending, FORMATTING)
    return begin, ending


# This function picks the filter that is used
def filter_chooser():
    print('Filters:\n\t1) 866\n\t2) 868\n\t3) BG\n\t4) P12A\n\t5) P14A\n\t6) Quit')
    filter_chosen = input('Which filter? ')
    if not filter_chosen.isdigit():
        filter_name = 'None'
        return filter_name
    if int(filter_chosen) == 1:
        filter_name = '866'
    elif int(filter_chosen) == 2:
        filter_name = '868'
    elif int(filter_chosen) == 3:
        filter_name = 'BG'
    elif int(filter_chosen) == 4:
        filter_name = 'P12A'
    elif int(filter_chosen) == 5:
        filter_name = 'P14A'
    elif int(filter_chosen) == 6:
        filter_name = 'Quit'
    else:
        filter_name = 'None'
    return filter_name


def mode1():
    while True:
        FILTER_LIST = ["P14A", "P12A", "BG", "868", "866"]
        done = False
        start = end = 0
        while not done:

            try:
                start, end = get_beginning_and_end()
                done = True
            except ValueError:
                print("You must type integers between 0 and 9999")

        print()
        for filter_name in FILTER_LIST:
            print("--- " + filter_name + " ---")
            print_data(filter_name, start, end)


def mode2():
    while True:
        # Get the filter and start and end numbers, then print the correct file names
        filter_name = filter_chooser()
        if filter_name == 'Quit':
            done = True
            break
        if filter_name == 'None':
            continue

        start = end = 0
        done = False
        while not done:
            try:
                start, end = get_beginning_and_end()
                done = True
            except ValueError:
                print("You must type integers between 0 and 9999")

        print_data(filter_name, start, end)


def print_data(filter_name, start, end):
    mean_start_name = filter_name + '_sr' + start + '.tif'
    mean_end_name = filter_name + '_sr' + end + '.tif'
    mean_name = 'FF_' + filter_name + '_' + str(start) + '-' + str(end) + '.tif'
    calibration_start_name = filter_name + '_srff' + start + '.tif'
    calibration_end_name = filter_name + '_srff' + end + '.tif'

    COLUMN_LENGTH = len(mean_name)
    FORMATTING = ">" + str(COLUMN_LENGTH) + "s"

    out_message = "\nCreating a mean image:\n"
    out_message += "\tStart filename: " + format(mean_start_name, ">" + str(COLUMN_LENGTH) + "s") + "\n"
    out_message += "\tEnd filename: " + format(mean_end_name, ">" + str(COLUMN_LENGTH + 2) + "s") + "\n"
    out_message += "\tMean filename: " + format(mean_name, ">" + str(COLUMN_LENGTH + 1) + "s") + "\n\n"
    out_message += "Calibration:\n"
    out_message += "\tStart filename: " + format(calibration_start_name, ">" + str(COLUMN_LENGTH) + "s") + "\n"
    out_message += "\tEnd filename: " + format(calibration_end_name, ">" + str(COLUMN_LENGTH + 2) + "s") + "\n\n\n"
    print(out_message)


def mode_selection():
    print("Modes:\n\t1) All filters\n\t2) One filter")
    mode = input("Which mode? ")
    if int(mode) == 1:
        mode1()
    elif int(mode) == 2:
        mode2()


def main():
    done = False
    while not done:
        try:
            mode_selection()
            done = True
        except ValueError:
            print("You must enter the ints 1 or 2")


main()
