# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import E
from MOI import MOI
from load_calculations import M, V
from Aircraft_parameters import b

def lateral_deflection_function():

    #define grid with y positions
    n = 3000
    y_max = b/2
    y_grid = np.linspace(0, y_max, n)

    #vectorize MOI calculations
    MOI_vec = np.vectorize(MOI)
    MOI_grid = MOI_vec(y_grid)

    #calculate M and h 
    M_grid = M(y_grid)
    h_grid = M_grid / (E * MOI_grid)
    print(M_grid[0], M_grid[-1])
    #double integration to obtain deflection profile
    dvdy_grid = -1 * cumulative_trapezoid(h_grid, y_grid, initial=0)
    v_grid = cumulative_trapezoid(dvdy_grid, y_grid, initial = 0)

    #make function callable
    # h = interp1d(y_grid, h_grid, fill_value = "extrapolate")
    # dvdy = interp1d(y_grid, dvdy_grid, fill_value = "extrapolate")
    lateral_deflection = interp1d(y_grid, v_grid, fill_value = "extrapolate")

    return(y_grid, v_grid)

def lateral_deflection_function_from_V(n=3000):
    """
    Compute lateral deflection v(y) using d^3 v / dy^3 = - V(y) / (E * I(y)).
    Integrates three times with trapezoidal rule.
    Boundary conditions enforced: v(0)=0, v'(0)=0, v''(0)=0.
    Returns (y_grid, v_grid).
    """
    # grid
    y_max = b / 2
    y_grid = np.linspace(0.0, y_max, n)

    # robust MOI evaluation (loop to handle non-vectorized MOI)
    MOI_vals = []
    for yy in y_grid:
        try:
            MOI_vals.append(float(MOI(float(yy))))
        except Exception:
            MOI_vals.append(np.nan)
    I_grid = np.asarray(MOI_vals, dtype=float)

    # distributed relation h3 = -V/(E I)
    V_grid = V(y_grid)
    with np.errstate(divide='ignore', invalid='ignore'):
        h3_grid = np.where(I_grid != 0.0, V_grid / (E * I_grid), np.nan)

    # integrate 3 times: v'' -> v' -> v
    v2_grid = cumulative_trapezoid(h3_grid, y_grid, initial=0.0)         # v''(y)
    v1_grid = cumulative_trapezoid(v2_grid, y_grid, initial=0.0)         # v'(y)
    v_grid  = cumulative_trapezoid(v1_grid, y_grid, initial=0.0)         # v(y)

    # optional: make callable if needed
    # v_func = interp1d(y_grid, v_grid, fill_value="extrapolate")

    return y_grid, v_grid