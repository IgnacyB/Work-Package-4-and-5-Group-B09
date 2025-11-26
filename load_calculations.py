#Importing necessary libraries
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#Importing necessary constants
from constants import g, rho_air
from Wing_geometry import b, c_r, c_t
from mass import mass_wing, mass_fuel, n_fuel
from scipy.integrate import cumulative_trapezoid
#importing functions from other files if needed
from main import c, dL, dD, dM, alpha

#Assumptions
#The wing and fuel weight force act in the centroid of the wingbox
x_bar_c = 1/2 #location of centroid of wing box assumed to be at half the chord (Should be update with more accurate data!!!)
x_lift = 1/4 #location of aerodynamic lift assumed to be at quarter chord
CL = 0.5 #Assumed CL for load calculations (Should be updated with actual flight conditions)

#=========WEIGHT CALCULATIONS=========#

#WEIGHT DISTRIBUTION (HALF OF SPAN)
def weight_distribution(mass_wing, b, c_r, c_t):

    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero

    A = 3 / 2 * mass_wing*g / 2 / (y_0**3-(y_0 - b/2)**3)
    def w_dist(y):
        return A * (y_0 - y)**2
    
    return w_dist

#=========FUEL CALCULATIONS=========#

#FUEL DISTRIBUTION (HALF OF SPAN)
#Fuel is assumed to be distributed the same way as the wing weight (in the wingbox)
def fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t):

    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero

    A = 3 / 2 * n_fuel * mass_fuel*g / 2 / (y_0**3-(y_0 - b/2)**3)
    def f_dist(y):
        return A * (y_0 - y)**2
    
    return f_dist

#=========LIFT CALCULATIONS=========#

#DISTANCE FROM LIFT TO CENTROID OF WINGBOX AS FUNCTION OF SPANWISE LOCATION
def distance_lift_centroid(x_bar_c, x_lift, y):
    return (x_bar_c - x_lift) * c(y)

def dN(y):
    return dL(y, CL) * np.cos(alpha(CL)) + dD(y, CL) * np.sin(alpha(CL))

#=========FORCE AND MOMENT IN CROSS SECTION=========#

#SHIFTING N FROM LIFT TO WINGBOX CENTROID
#Force is the same since it acts vertically, only the moment changes
def dM_N(y):
    return dN(y) * distance_lift_centroid(x_bar_c, x_lift, y)

#=========COMPUTING INTERNAL SHEAR FORCE AND BENDING MOMENT=========#
w_dist = weight_distribution(mass_wing, b, c_r, c_t)
f_dist = fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t)

def dV(y):
    return -dN(y) + w_dist(y) + f_dist(y)
def dT(y):
    return -dM_N(y) - dM(y, CL)

# helper: try to call func on array, fall back to vectorize if needed
def _call_array(func, y):
    y_arr = np.asarray(y)
    # fast path: try direct call
    try:
        res = func(y_arr)
        res = np.asarray(res)
        if res.shape == y_arr.shape:
            return res
    except Exception:
        pass
    # fallback: vectorize scalar func
    vec = np.vectorize(lambda yy: func(float(yy)))
    return vec(y_arr)

# Internal shear/torque/moment: accept scalar or array y
def V(y):
    # scalar behavior (keep previous quad-based result)
    if np.ndim(y) == 0:
        Vval, error = sp.integrate.quad(dV, b/2, float(y))
        return Vval
    # array/vectorized behavior (fast cumulative integration)
    y_arr = np.asarray(y)
    dV_arr = _call_array(dV, y_arr)
    # integrate from tip (b/2) inward so V(b/2)=0
    V_flip = cumulative_trapezoid(np.flip(dV_arr), np.flip(y_arr), initial=0)
    V_arr = np.flip(V_flip)
    return V_arr

def T(y):
    if np.ndim(y) == 0:
        Tval, error = sp.integrate.quad(dT, b/2, float(y))
        return Tval
    y_arr = np.asarray(y)
    dT_arr = _call_array(dT, y_arr)
    T_flip = cumulative_trapezoid(np.flip(dT_arr), np.flip(y_arr), initial=0)
    T_arr = np.flip(T_flip)
    return T_arr

def M(y):
    # scalar: integrate V via quad (keeps previous API)
    if np.ndim(y) == 0:
        Mval, error = sp.integrate.quad(lambda s: V(s), b/2, float(y))
        return -1 * Mval
    # array: build V array then integrate
    y_arr = np.asarray(y)
    V_arr = V(y_arr)  # uses vectorized V above
    M_flip = cumulative_trapezoid(np.flip(V_arr), np.flip(y_arr), initial=0)
    M_arr = -1 * np.flip(M_flip)
    return M_arr


