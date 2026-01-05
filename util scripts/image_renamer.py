from os import listdir
from os.path import isfile, join
from re import compile


def main():
    path = "."
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    print(all_files)
    print(type(all_files[0]))

    regex = compile("BG_31_[0-9]{4}.tif")
    for file in all_files:
        if regex.match(file):
            print(file)

main()
