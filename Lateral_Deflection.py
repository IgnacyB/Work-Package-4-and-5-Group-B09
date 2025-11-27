# This is the file used to actually calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumtrapz

#import all the information from the other files
from material_properties import E
from MOI import MOI_single_cell
from load_calculations import M


def h(y):
    return M(y) / (E * MOI_single_cell(y))

print(h(5))

def dvdy(y):
    return -1 * sp.integrate.quad(np.vectorize(h),0,y)[0]

print(dvdy(5))

#y_pos = float(input("spanwise location: "))
def lateral_deflection(y):
    return sp.integrate.quad(dvdy,0,y)[0]

print(lateral_deflection(0.1))

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

