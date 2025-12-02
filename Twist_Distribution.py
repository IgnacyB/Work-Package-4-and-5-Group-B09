# This is the file used to calculate the twist distribution in the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import G
from torsional_stiffness_functions import torsional_constant_singlecell
from load_calculations import T
from Aircraft_parameters import b

n = 3000
y_max = b/2
y_grid = np.linspace(0, y_max, n)

#vectorize torsional stiffness J calculations
J_vec = np.vectorize(torsional_constant_singlecell)
J_grid = J_vec(y_grid)

#calculate T and dthetady
T_grid = T(y_grid)
dthetady_grid = T_grid / (G * J_grid)

#integrate to obtain twist
twist_grid = cumulative_trapezoid(dthetady_grid, y_grid, initial = 0)

#make function callable
twist = interp1d(y_grid, twist_grid, fill_value = "extrapolate")

print(twist(b/2))



# def dthetady(y):
#     return T(y) / (G * torsional_constant_singlecell(y))

# #y_pos = int(input("Spanwise location: "))

# def twist(y):
#     return sp.integrate.quad(dthetady,0,float(y))[0]

# print(twist(5))