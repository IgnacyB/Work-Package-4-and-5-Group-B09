# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import E
from MOI import MOI_grid
from load_calculations import M
from Aircraft_parameters import b

#importing y grid
from grid_setup import y_arr
def lateral_deflection_function():

    #calculate M and h 
    M_grid = M()
    h_grid = M_grid / (E * MOI_grid)

    #double integration to obtain deflection profile
    dvdy_grid = -1 * cumulative_trapezoid(h_grid, y_arr, initial=0)
    v_grid = cumulative_trapezoid(dvdy_grid, y_arr, initial = 0)

    return v_grid

# lateral_deflection_at_tip = lateral_deflection_function()[1][-1]
