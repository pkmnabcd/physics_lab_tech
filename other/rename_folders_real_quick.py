"""
Dumb lil script that changes the names of McMurdo_minus_15#.. dirs to specifying lon direction.
This works for just the directory it's placed in
"""

from os import rename
from os import listdir

directories = listdir()
for current_dir in directories:
    if "McMurdo_" in current_dir:
        value = 0
        string_length = len(current_dir)
        for i in range(string_length):
            current_character = current_dir[i]
            if current_character == "#":
                value = int(current_dir[i + 1:])
                break
        rename(current_dir, "McMurdo_lon_minus_15#" + str(value))
