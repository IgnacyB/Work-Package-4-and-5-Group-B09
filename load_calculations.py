#Importing necessary libraries
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#Importing necessary constants
from constants import g, rho_air
# Import only structural/static parameters from Aircraft_parameters (no runtime masses)
from Aircraft_parameters import mass_wing, n_fuel, b, c_r, c_t, c, S_w
from scipy.integrate import cumulative_trapezoid
#importing functions from other files if needed
from XFLRextraction import dL_array, dD_array, dM_array, alpha, set_flight_conditions

#importing y grid
from grid_setup import y_arr
# add module-level operating-condition holders
mass_aircraft_op = None
v_cruise_op = None
rho_op = None
mass_fuel_op = None
CL_op = None
mass_wing_op = None

# placeholders for distributions that depend on operating conditions
w_dist = None
f_dist = None

#Assumptions
#The wing and fuel weight force act in the centroid of the wingbox
x_bar_c = 1/2 #location of centroid of wing box assumed to be at half the chord (Should be update with more accurate data!!!)
x_lift = 1/4 #location of aerodynamic lift assumed to be at quarter chord

#WEIGHT DISTRIBUTION (HALF OF SPAN)
def weight_distribution(mass_wing, b, c_r, c_t):
    y_0 = (b / 2) * c_r / (c_r - c_t) #location where the load distribution becomes zero
    A = mass_wing*g / (y_0**2-(y_0 - b/2)**2) #It is divided by 2 since we are only considering half the span and thus half of the weight
    w = A * (y_0 - y_arr)
    return w

#FUEL DISTRIBUTION (HALF OF SPAN)
def fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t):
    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero
    A = 3 / 2 * n_fuel * mass_fuel*g / (y_0**3-(y_0 - b/2)**3) #It is divided by 2 since we are only considering half the span and thus half of the weight
    f = A * (y_0 - y_arr)**2
    return f

def set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel):
    """Store per-load-case operating conditions used by other functions.
    Must be called from main before calling M(), T(), dN(), etc.
    """
    global mass_aircraft_op, v_cruise_op, rho_op, mass_fuel_op, CL_op, w_dist, f_dist, mass_wing_op
    mass_aircraft_op = load_factor * mass_aircraft
    v_cruise_op = v_cruise
    rho_op = rho
    mass_fuel_op = load_factor * mass_fuel
    mass_wing_op = load_factor * mass_wing
    # compute CL for level flight using aircraft constants (S_w, g)
    CL_op = 2 * mass_aircraft_op * g / (rho_op * v_cruise_op**2 * S_w)

    # inform aerodynamic module about flight conditions (sets dynamic pressure q)
    set_flight_conditions(rho_op, v_cruise_op)

    # build distributions that depend on current mass_fuel (fuel distribution) and wing mass (fixed)
    w_dist = weight_distribution(mass_wing_op, b, c_r, c_t)
    f_dist = fuel_distribution(mass_fuel_op, n_fuel, b, c_r, c_t)

#DISTANCE FROM LIFT TO CENTROID OF WINGBOX AS FUNCTION OF SPANWISE LOCATION
def distance_lift_centroid(x_bar_c, x_lift):
    return (x_bar_c - x_lift) * c(y_arr)

def dN():
    if CL_op is None:
        raise RuntimeError("Call set_operating_conditions(...) before computing dN")
    return dL_array(y_arr, CL_op) * np.cos(np.radians(alpha(CL_op))) + dD_array(y_arr, CL_op) * np.sin(np.radians(alpha(CL_op)))

#SHIFTING N FROM LIFT TO WINGBOX CENTROID
def dM_N():
    return dN() * distance_lift_centroid(x_bar_c, x_lift)
#======== internal loads ========
def dV():
    y_arr_copy = np.asarray(y_arr)
    if w_dist is None or f_dist is None:
        raise RuntimeError("Call set_operating_conditions(...) before computing internal loads")
    return -dN(y_arr) + w_dist + f_dist

def dT():
    if CL_op is None:
        raise RuntimeError("Call set_operating_conditions(...) before computing internal loads")
    return -dM_N(y_arr) - dM_array(y_arr, CL_op)


def V():
    y_arr_copy = np.asarray(y_arr)
    dV_arr = dV(y_arr_copy)
    V_flip = cumulative_trapezoid(np.flip(dV_arr), np.flip(y_arr_copy), initial=0)
    V_arr = -1 * np.flip(V_flip)
    return V_arr

def T():
    y_arr_copy = np.asarray(y_arr)
    dT_arr = dT(y_arr_copy)
    T_flip = cumulative_trapezoid(np.flip(dT_arr), np.flip(y_arr_copy), initial=0)
    T_arr = -1 * np.flip(T_flip)
    return T_arr

def M(y_arr):
    y_arr_copy = np.asarray(y_arr)
    V_arr = V(y_arr_copy)
    M_flip = cumulative_trapezoid(np.flip(V_arr), np.flip(y_arr_copy), initial=0)
    M_arr = np.flip(M_flip)
    return M_arr

def plot_internal_loads(y_arr):
    V_arr = V(y_arr)
    T_arr = T(y_arr) 
    M_arr = M(y_arr) 

    fig, axs = plt.subplots(3, 1, figsize=(8, 10), constrained_layout=True)

    axs[0].plot(y_arr, V_arr, lw=2, color="tab:blue")
    axs[0].axhline(0, color="k", lw=0.6)
    axs[0].set_ylabel("V(y) [N]")
    axs[0].set_title("Internal Shear Force along wing span")
    axs[0].grid(True)

    axs[1].plot(y_arr, T_arr, lw=2, color="tab:green")
    axs[1].axhline(0, color="k", lw=0.6)
    axs[1].set_ylabel("T(y) [N·m]")
    axs[1].set_title("Internal Torque along wing span")
    axs[1].grid(True)

    axs[2].plot(y_arr, M_arr, lw=2, color="tab:red")
    axs[2].axhline(0, color="k", lw=0.6)
    axs[2].set_xlabel("Spanwise coordinate y (m)")
    axs[2].set_ylabel("M(y) [N·m]")
    axs[2].set_title("Internal Bending Moment along wing span")
    axs[2].grid(True)

    plt.show()

def plot_distributed_loads(y_arr):
    # use existing helper to evaluate funcs on arrays
    dV_arr = dV(y_arr)
    dT_arr = dT(y_arr)

    plt.figure(figsize=(8,5))
    plt.plot(y_arr, dV_arr, lw=2, label="dV/dy (q(y))", color="tab:orange")
    plt.plot(y_arr, dT_arr, lw=2, linestyle="--", label="dT/dy", color="tab:purple")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Distributed loads")
    plt.title("Distributed loads along half-span: dV/dy and dT/dy")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_dN(y_arr):
    dN_arr = dN(y_arr)

    plt.figure(figsize=(8,4))
    plt.plot(y_arr, dN_arr, lw=2, color="tab:orange")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("dN(y) [N/m]")
    plt.title("Net distributed normal force dN(y) along half-span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_dL(y_arr):

    # dL in XFLRextraction expects (y, CL)
    dL_arr = dL_array(y_arr, CL_op)

    plt.figure(figsize=(8,4))
    plt.plot(y_arr, dL_arr, lw=2, color="tab:blue")
    plt.axhline(0, color="k", lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("dL(y) [N/m]")
    plt.title("Sectional lift distribution dL(y) along half-span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_wing_and_fuel_distributions(y_arr):

    plt.figure(figsize=(8,5))
    plt.plot(y_arr, w_dist, lw=2, label="Wing weight distribution w(y) [N/m]", color="tab:blue")
    plt.plot(y_arr, f_dist, lw=2, linestyle="--", label="Fuel distribution f(y) [N/m]", color="tab:green")
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
    f_arr = func(y_arr)
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
    f_func = fuel_distribution(mass_fuel_op, n_fuel, b, c_r, c_t)

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
    dL_int = _integrate_from_tip(lambda yy: dL_array(yy, CL_op), y)

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
    plot_internal_loads(y_arr)
    plot_distributed_loads(y_arr)
    plot_dN(y_arr)
    plot_dL(y_arr)
    plot_wing_and_fuel_distributions(y_arr)
    plot_integrated_distributions(y_arr)
    plot_integrated_dL(y_arr)