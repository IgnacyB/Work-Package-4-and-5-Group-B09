# This is the file used to calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d
from material_properties import E
from MOI import MOI
from load_calculations import M, V, precompute_internal_loads
from Aircraft_parameters import b

def lateral_deflection_function(n=600):
    """Deflection via d2v/dy2 = -M/(E I), using shared grid and cache."""
    y = np.linspace(0, b/2, n)
    try:
        precompute_internal_loads(y)
    except Exception:
        pass

    # cache MOI over y once
    I_vals = np.asarray([float(MOI(float(yy))) for yy in y], dtype=float)

    M_vals = M(y)
    with np.errstate(divide='ignore', invalid='ignore'):
        h = np.where(I_vals != 0.0, -M_vals / (E * I_vals), np.nan)

    dvdy = cumulative_trapezoid(h, y, initial=0.0)
    v = cumulative_trapezoid(dvdy, y, initial=0.0)
    return y, v

# lateral_deflection_at_tip = lateral_deflection_function()[1][-1]
