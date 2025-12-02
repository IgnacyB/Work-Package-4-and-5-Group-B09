#Importing necessary libraries
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#Importing necessary constants
from constants import g, rho_air
from Aircraft_parameters import mass_aircraft, mass_fuel, mass_wing, n_fuel ,b, c_r, c_t, c, S_w
from scipy.integrate import cumulative_trapezoid
#importing functions from other files if needed
from XFLRextraction import dL, dD, dM, alpha

#Importing user inputs from main.py
from Load_cases import mass_aircraft, v_cruise, rho_cruise, mass_fuel

#Assumptions
#The wing and fuel weight force act in the centroid of the wingbox
x_bar_c = 1/2 #location of centroid of wing box assumed to be at half the chord (Should be update with more accurate data!!!)
x_lift = 1/4 #location of aerodynamic lift assumed to be at quarter chord
CL = 2 * mass_aircraft * g / (rho_cruise * v_cruise**2 * S_w) # Calculating the required CL for level flight
#=========WEIGHT CALCULATIONS=========#

#WEIGHT DISTRIBUTION (HALF OF SPAN)
def weight_distribution(mass_wing, b, c_r, c_t):

    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero

    A = 3 / 2 * mass_wing*g / (y_0**3-(y_0 - b/2)**3) #It is divided by 2 since we are only considering half the span and thus half of the weight
    def w_dist(y):
        return A * (y_0 - y)**2
    
    return w_dist

#=========FUEL CALCULATIONS=========#

#FUEL DISTRIBUTION (HALF OF SPAN)
#Fuel is assumed to be distributed the same way as the wing weight (in the wingbox)
def fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t):

    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero

    A = 3 / 2 * n_fuel * mass_fuel*g / (y_0**3-(y_0 - b/2)**3) #It is divided by 2 since we are only considering half the span and thus half of the weight
    def f_dist(y):
        return A * (y_0 - y)**2
    
    return f_dist

#=========LIFT CALCULATIONS=========#

#DISTANCE FROM LIFT TO CENTROID OF WINGBOX AS FUNCTION OF SPANWISE LOCATION
def distance_lift_centroid(x_bar_c, x_lift, y):
    return (x_bar_c - x_lift) * c(y)

def dN(y):
    return dL(y, CL) * np.cos(np.radians(alpha(CL))) + dD(y, CL) * np.sin(np.radians(alpha(CL)))

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
    V_arr = -1 * np.flip(V_flip)
    return V_arr

def T(y):
    if np.ndim(y) == 0:
        Tval, error = sp.integrate.quad(dT, b/2, float(y))
        return Tval
    y_arr = np.asarray(y)
    dT_arr = _call_array(dT, y_arr)
    T_flip = cumulative_trapezoid(np.flip(dT_arr), np.flip(y_arr), initial=0)
    T_arr = -1 * np.flip(T_flip)
    return T_arr

def M(y):
    # scalar: integrate V via quad (keeps previous API)
    if np.ndim(y) == 0:
        Mval, error = sp.integrate.quad(lambda s: V(s), b/2, float(y))
        return Mval
    # array: build V array then integrate
    y_arr = np.asarray(y)
    V_arr = V(y_arr)  # uses vectorized V above
    M_flip = cumulative_trapezoid(np.flip(V_arr), np.flip(y_arr), initial=0)
    M_arr = np.flip(M_flip)
    return M_arr

def plot_internal_loads(y=None, n=200):
    if y is None:
        y = np.linspace(0, b/2, n)
    V_arr = V(y) if callable(V) else np.asarray(V)
    T_arr = T(y) if callable(T) else np.asarray(T)
    M_arr = M(y) if callable(M) else np.asarray(M)

    fig, axs = plt.subplots(3, 1, figsize=(8, 10), constrained_layout=True)

    axs[0].plot(y, V_arr, lw=2, color="tab:blue")
    axs[0].axhline(0, color="k", lw=0.6)
    axs[0].set_ylabel("V(y) [N]")
    axs[0].set_title("Internal Shear Force along wing span")
    axs[0].grid(True)

    axs[1].plot(y, T_arr, lw=2, color="tab:green")
    axs[1].axhline(0, color="k", lw=0.6)
    axs[1].set_ylabel("T(y) [N·m]")
    axs[1].set_title("Internal Torque along wing span")
    axs[1].grid(True)

    axs[2].plot(y, M_arr, lw=2, color="tab:red")
    axs[2].axhline(0, color="k", lw=0.6)
    axs[2].set_xlabel("Spanwise coordinate y (m)")
    axs[2].set_ylabel("M(y) [N·m]")
    axs[2].set_title("Internal Bending Moment along wing span")
    axs[2].grid(True)

    plt.show()

def plot_distributed_loads(y=None, n=300):
    if y is None:
        y = np.linspace(0, b/2, n)
    # use existing helper to evaluate funcs on arrays
    dV_arr = _call_array(dV, y)
    dT_arr = _call_array(dT, y)

    plt.figure(figsize=(8,5))
    plt.plot(y, dV_arr, lw=2, label="dV/dy (q(y))", color="tab:orange")
    plt.plot(y, dT_arr, lw=2, linestyle="--", label="dT/dy", color="tab:purple")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Distributed loads")
    plt.title("Distributed loads along half-span: dV/dy and dT/dy")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_dN(y=None, n=300):
    """Plot the net distributed normal force dN(y) along the half-span."""
    if y is None:
        y = np.linspace(0, b/2, n)
    dN_arr = _call_array(dN, y)

    plt.figure(figsize=(8,4))
    plt.plot(y, dN_arr, lw=2, color="tab:orange")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("dN(y) [N/m]")
    plt.title("Net distributed normal force dN(y) along half-span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_dL(y=None, n=300):
    """Plot sectional lift distribution dL(y, CL) along the half-span."""
    if y is None:
        y = np.linspace(0, b/2, n)

    # dL in XFLRextraction expects (y, CL)
    dL_arr = _call_array(lambda yy: dL(yy, CL), y)

    plt.figure(figsize=(8,4))
    plt.plot(y, dL_arr, lw=2, color="tab:blue")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("dL(y) [N/m]")
    plt.title("Sectional lift distribution dL(y) along half-span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_wing_and_fuel_distributions(y=None, n=300):
    """Plot wing weight distribution w(y) and fuel distribution f(y) along half-span."""
    if y is None:
        y = np.linspace(0, b/2, n)

    w_func = weight_distribution(mass_wing, b, c_r, c_t)
    f_func = fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t)

    w_arr = _call_array(w_func, y)
    f_arr = _call_array(f_func, y)

    plt.figure(figsize=(8,5))
    plt.plot(y, w_arr, lw=2, label="Wing weight distribution w(y) [N/m]", color="tab:blue")
    plt.plot(y, f_arr, lw=2, linestyle="--", label="Fuel distribution f(y) [N/m]", color="tab:green")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Distributed load [N/m]")
    plt.title("Wing weight and fuel distributions along half-span")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def _integrate_from_tip(func, y):
    """Integrate `func` from tip (b/2) to y. Accepts scalar or array y."""
    # scalar behavior
    if np.ndim(y) == 0:
        val, err = sp.integrate.quad(func, b/2, float(y))
        return val
    # array/vectorized behavior: integrate from tip inward so integral(b/2)=0
    y_arr = np.asarray(y)
    f_arr = _call_array(func, y_arr)
    # integrate on flipped arrays then flip back (consistent with V/T implementation)
    integral_flip = cumulative_trapezoid(np.flip(f_arr), np.flip(y_arr), initial=0)
    integral_arr = -1 * np.flip(integral_flip)
    return integral_arr

def plot_integrated_distributions(y=None, n=300):
    """Compute and plot cumulative integrals (from tip b/2 to y) of dN, wing weight and fuel distributions."""
    if y is None:
        y = np.linspace(0, b/2, n)

    # get distribution functions
    w_func = weight_distribution(mass_wing, b, c_r, c_t)
    f_func = fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t)

    # compute cumulative integrals from tip to each y
    dN_int = _integrate_from_tip(dN, y)
    w_int  = _integrate_from_tip(w_func, y)
    f_int  = _integrate_from_tip(f_func, y)

    plt.figure(figsize=(8,5))
    plt.plot(y, dN_int, lw=2, label="Integrated dN (from tip) [N]", color="tab:orange")
    plt.plot(y, w_int, lw=2, label="Integrated wing weight (from tip) [N]", color="tab:blue")
    plt.plot(y, f_int, lw=2, linestyle="--", label="Integrated fuel (from tip) [N]", color="tab:green")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Cumulative force from tip to y [N]")
    plt.title("Cumulative integrals of dN, wing weight and fuel along half-span")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_integrated_dL(y=None, n=300):
    """Compute and plot cumulative integral of sectional lift dL(y,CL) from tip (b/2) to y."""
    if y is None:
        y = np.linspace(0, b/2, n)

    # dL depends on CL (module-level CL). Integrate from tip to y.
    dL_int = _integrate_from_tip(lambda yy: dL(yy, CL), y)

    plt.figure(figsize=(8,5))
    plt.plot(y, dL_int, lw=2, label="Integrated dL (from tip) [N]", color="tab:blue")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Cumulative lift from tip to y [N]")
    plt.title("Cumulative integral of sectional lift dL along half-span")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_internal_loads()
    plot_distributed_loads()
    plot_dN()
    plot_dL()
    plot_wing_and_fuel_distributions()
    plot_integrated_distributions()
    plot_integrated_dL()