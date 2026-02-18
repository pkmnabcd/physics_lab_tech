
import sys
from os.path import join


IDL_DIR = join("C:/", "Program Files", "Harris", "IDL89")
sys.path.append(f"{IDL_DIR}/lib/bridges")

from idlpy import *

IDL.print("Hello world!")
