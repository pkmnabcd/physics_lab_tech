import grapher
import numpy as np

sales = np.array([72, 180, 279, 378, 495, 585, 693, 792, 855, 873, 801, 648, 612, 477, 396])
indexes = np.arange(1, 16)

grapher.do_polynomial_fit(indexes, sales, 2)
