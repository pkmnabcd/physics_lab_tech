from os import listdir
from os.path import exists
from os.path import isdir


year = "2020"

path_stub = f"E://ChileMTM//{year}//"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for month in months:
    outer_path = path_stub + month + year + "//"
    if not exists(outer_path):
        continue
    dirs = listdir(outer_path)
    for directory in dirs:
        inner_path = outer_path + directory + "//"
        if not isdir(inner_path):
            continue
        files = listdir(inner_path)
        for file in files:
            file_path = inner_path + file
            if isdir(file_path):
                print(f"Extras in {inner_path}")
                break

input("Waiting....")
