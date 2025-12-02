# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import E
from MOI import MOI_single_cell
from load_calculations import M
from Aircraft_parameters import b

def lateral_deflection_function(y):

    #define grid with y positions
    n = 3000
    y_max = b/2
    y_grid = np.linspace(0, y_max, n)

    #vectorize MOI calculations
    MOI_vec = np.vectorize(MOI_single_cell)
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

    return(lateral_deflection(y))

#test
print(lateral_deflection_function(b/2))










# def h(y):
#     return M(y) / (E * MOI_single_cell(y))

# print(h(5))

# def dvdy(y):
#     return -1 * sp.integrate.quad(np.vectorize(h),0,y)[0]

# print(dvdy(5))

# #y_pos = float(input("spanwise location: "))
# def lateral_deflection(y):
#     return sp.integrate.quad(dvdy,0,y)[0]

# print(lateral_deflection(0.1))








# import numpy as np
# from scipy.integrate import cumulative_trapezoid as cumtrapz

# from material_properties import E
# from Aircraft_parameters import b
# from MOI import MOI_single_cell
# from load_calculations import M

# def h(y):
#     return M(y) / (E * MOI_single_cell(y))

# L = b/2
# N = 10
# ys = np.linspace(0, L, N)

# # Vectorize h
# h_vec = np.vectorize(h)
# h_vals = h_vec(ys)

# # first integration
# dvdy_vals = -cumtrapz(h_vals, ys, initial=0)

# # second integration
# v_vals = cumtrapz(dvdy_vals, ys, initial=0)

# def dvdy(y):
#     return np.interp(y, ys, dvdy_vals)

# def lateral_deflection(y):
#     return np.interp(y, ys, v_vals)

# print(lateral_deflection(0.1))
