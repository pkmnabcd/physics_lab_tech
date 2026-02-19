
import sys
from os.path import join


IDL_DIR = join("C:/", "Program Files", "Harris", "IDL89")
sys.path.append(f"{IDL_DIR}/lib/bridges")

from idlpy import *

IDL.print("Hello world!")


FFT_FILENAME = "m_fft_asi.pro"
READ_IMAGE_FILENAME = "read_images_ALOMAR.pro"
SHELLRUNNER_FILENAME = "mlshellrunnertest.pro"


# NOTE: the following code yields the path
# C:\Users\Domi\OneDrive\Desktop\MachineLearning\IDLCode
idl_scripts_dir = join("C:/", "Users", "Domi", "OneDrive", "Desktop", "MachineLearning", "IDLCode")

IDL.run(f".compile {join(idl_scripts_dir, FFT_FILENAME)}")
