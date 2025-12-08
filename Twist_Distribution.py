# This is the file used to calculate the twist distribution in the wing

#first import the necessary packages and functions from 
import numpy as np
import math
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import G
from torsional_stiffness_functions import torsional_constant
from load_calculations import T
from Aircraft_parameters import b

#importing y grid
from grid_setup import y_arr

def twist_function():

    #vectorize torsional stiffness J calculations
    J_vec = np.vectorize(torsional_constant)
    J_grid = J_vec(y_arr)
    #calculate T and dthetady
    
    T_grid = T()
    dthetady_grid = T_grid / (G * J_grid)

    #integrate to obtain twist
    twist_grid = cumulative_trapezoid(dthetady_grid, y_arr, initial = 0)
    #make function callable
    twist = interp1d(y_arr, twist_grid, fill_value = "extrapolate")

    return twist_grid
