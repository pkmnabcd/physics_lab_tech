import sys
from os import listdir
from re import compile

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Usage: python[3] nan_checker.py [processed_folder]")
        exit(0)
    processed_folder_path = args[1]

    paths = listdir(processed_folder_path)
    pattern = compile("OH_Andover_ALO[0-9][0-9]day[0-9]{1,3}.dat")
    for path in paths:
        if not pattern.match(path):
            continue
        else:
            file = open(processed_folder_path + "/" + path)
            lines = file.readlines()

            for line in lines:
                if "NaN" in line:
                    print(path + " has NaN in it!")
                    break

