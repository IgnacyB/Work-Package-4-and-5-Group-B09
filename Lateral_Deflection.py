# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

#import constants from other files
from material_properties import E
from MOI import MOI
from load_calculations import M, V, precompute_internal_loads
from Aircraft_parameters import b

def lateral_deflection_function(n=3000):
    """Deflection via d2v/dy2 = -M/(E I) with v(0)=0 and v'(0)=0."""
    #define grid with y positions (shared)
    y_max = b/2
    y_grid = np.linspace(0, y_max, n)

    # ensure internal loads are precomputed on same resolution
    try:
        precompute_internal_loads(n=len(y_grid))
    except Exception:
        pass

    # robust MOI evaluation
    I_vals = [float(MOI(float(yy))) for yy in y_grid]
    I_grid = np.asarray(I_vals, dtype=float)

    #calculate M and h, guard division
    M_grid = V_grid = None
    M_grid = M(y_grid)
    with np.errstate(divide='ignore', invalid='ignore'):
        h_grid = np.where(I_grid != 0.0, -M_grid / (E * I_grid), np.nan)

    #double integration to obtain deflection profile
    dvdy_grid = cumulative_trapezoid(h_grid, y_grid, initial=0.0)   # v'(y)
    v_grid    = cumulative_trapezoid(dvdy_grid, y_grid, initial=0.0) # v(y)

    lateral_deflection = interp1d(y_grid, v_grid, fill_value="extrapolate")
    return y_grid, v_grid

def lateral_deflection_function_from_V(n=3000):
    """
    Deflection via d^3 v / dy^3 = - V(y) / (E * I(y)).
    Enforces v(0)=0, v'(0)=0, v''(0)=0.
    """
    y_max = b / 2
    y_grid = np.linspace(0.0, y_max, n)

    # ensure internal loads are precomputed on same resolution
    try:
        precompute_internal_loads(n=len(y_grid))
    except Exception:
        pass

    # robust MOI evaluation (loop to handle non-vectorized MOI)
    I_vals = [float(MOI(float(yy))) for yy in y_grid]
    I_grid = np.asarray(I_vals, dtype=float)

    # distributed relation h3 = -V/(E I)  [FIXED: minus sign]
    V_grid = V(y_grid)
    with np.errstate(divide='ignore', invalid='ignore'):
        h3_grid = np.where(I_grid != 0.0, -V_grid / (E * I_grid), np.nan)

    # integrate 3 times: v'' -> v' -> v
    v2_grid = cumulative_trapezoid(h3_grid, y_grid, initial=0.0)         # v''(y)
    v1_grid = cumulative_trapezoid(v2_grid, y_grid, initial=0.0)         # v'(y)
    v_grid  = cumulative_trapezoid(v1_grid, y_grid, initial=0.0)         # v(y)

    # optional callable
    # v_func = interp1d(y_grid, v_grid, fill_value="extrapolate")
    return y_grid, v_grid

def compare_deflection_methods(n=2000):
    """Quick check: compute both methods on the same grid and report max difference."""
    y = np.linspace(0, b/2, n)
    try:
        precompute_internal_loads(n=len(y))
    except Exception:
        pass

    y1, v_M = lateral_deflection_function(n=n)
    y2, v_V = lateral_deflection_function_from_V(n=n)
    if np.array_equal(y1, y2):
        diff = np.nanmax(np.abs(v_M - v_V))
        print(f"[deflection] max|v_M - v_V| = {diff:.3e} m")
    else:
        print("[deflection] grids differ; ensure both use same n")

if __name__ == "__main__":
    compare_deflection_methods()