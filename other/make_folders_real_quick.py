from os import mkdir
from os.path import exists


def make_dir_if_doesnt_exist(directory):
    if not exists(directory):
        mkdir(directory)


make_dir_if_doesnt_exist("McMurdo_lon_minus_15#20_minus_lat_5#1")
make_dir_if_doesnt_exist("McMurdo_lon_minus_15#20_minus_lat_5#2")
for i in range(33):
    multiplier = i + 1
    directory = "McMurdo_lon_minus_15#20_plus_lat_5#" + str(multiplier)
    make_dir_if_doesnt_exist(directory)
