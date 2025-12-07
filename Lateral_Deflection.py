# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import E
from MOI import MOI
from load_calculations import M
from Aircraft_parameters import b

def lateral_deflection_function():

    #define grid with y positions
    n = 3000
    y_max = b/2
    y_grid = np.linspace(0, y_max, n)
    print(y_max)

    #vectorize MOI calculations
    MOI_vec = np.vectorize(MOI)
    MOI_grid = MOI_vec(y_grid)

    #calculate M and h 
    M_grid = M(y_grid)
    h_grid = M_grid / (E * MOI_grid)

    #double integration to obtain deflection profile
    dvdy_grid = -1 * cumulative_trapezoid(h_grid, y_grid, initial=0)
    v_grid = cumulative_trapezoid(dvdy_grid, y_grid, initial = 0)

    #make function callable
    # h = interp1d(y_grid, h_grid, fill_value = "extrapolate")
    # dvdy = interp1d(y_grid, dvdy_grid, fill_value = "extrapolate")
    lateral_deflection = interp1d(y_grid, v_grid, fill_value = "extrapolate")

    return(y_grid, v_grid)

# lateral_deflection_at_tip = lateral_deflection_function()[1][-1]

lateral_deflection_function()