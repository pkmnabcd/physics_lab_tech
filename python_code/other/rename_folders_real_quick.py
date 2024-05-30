"""
Dumb lil script that changes the names of McMurdo_minus_15#.. dirs to specifying lon direction.
This works for just the directory it's placed in
"""

from os import rename
from os import listdir

# directories = listdir()
# for current_dir in directories:
#     if "McMurdo_" in current_dir:
#         value = 0
#         string_length = len(current_dir)
#         for i in range(string_length):
#             current_character = current_dir[i]
#             if current_character == "#":
#                 value = int(current_dir[i + 1:])
#                 break
#         rename(current_dir, "McMurdo_lon_minus_15#" + str(value))

directories = listdir()
for current_dir in directories:
    not_mcmurdo = "McMurdo_" in current_dir
    no_lat = "lat" not in current_dir
    if not_mcmurdo and not no_lat:
        string_length = len(current_dir)
        lon_val = 0
        lat_val = 0

        lon_index = current_dir.find("lon")
        lat_index = current_dir.find("lat")

        lon_type = "plus" if current_dir[lon_index+4] == "p" else "minus"
        lat_type = "plus" if current_dir[lat_index-6] == "_" else "minus"

        for i in range(lon_index, string_length):
            if current_dir[i] == "#":
                num_string = ""
                j = i + 1
                while current_dir[j].isdigit():
                    num_string += current_dir[j]
                    j += 1
                lon_val = num_string
                break
        for i in range(lat_index, string_length):
            if current_dir[i] == "#":
                num_string = ""
                j = i + 1
                while j < len(current_dir):
                    num_string += current_dir[j]
                    j += 1
                lat_val = num_string
                break
        new_name = "McMurdo_" + lon_type + "_lon_15#" + lon_val + "_" + lat_type + "_lat_5#" + lat_val
        rename(current_dir, new_name)
    elif not_mcmurdo and no_lat:
        string_length = len(current_dir)
        lon_val = 0

        lon_index = current_dir.find("lon")

        lon_type = "plus" if current_dir[lon_index + 4] == "p" else "minus"

        for i in range(lon_index, string_length):
            if current_dir[i] == "#":
                num_string = ""
                j = i + 1
                while j < len(current_dir):
                    num_string += current_dir[j]
                    j += 1
                lon_val = num_string
                break
        new_name = "McMurdo_" + lon_type + "_lon_15#" + lon_val
        rename(current_dir, new_name)
