from Aircraft_parameters import b
import numpy as np

# Define the y grid for spanwise positions
n = 3000
y_max = b / 2
y_arr = np.linspace(0, y_max, n)