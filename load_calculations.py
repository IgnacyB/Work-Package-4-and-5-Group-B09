#Importing necessary libraries
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#Importing necessary constants
from constants import g, rho_air
from Wing_geometry import b, c_r, c_t
from mass import mass_wing, mass_fuel, n_fuel

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

def dN(y, CL):
    return dL(y, CL) * np.cos(alpha(CL)) + dD(y, CL) * np.sin(alpha(CL))

#=========FORCE AND MOMENT IN CROSS SECTION=========#

#SHIFTING N FROM LIFT TO WINGBOX CENTROID
#Force is the same since it acts vertically, only the moment changes
def dM_N(y, CL):
    return dN(y, CL) * distance_lift_centroid(x_bar_c, x_lift, y)

#=========COMPUTING INTERNAL SHEAR FORCE AND BENDING MOMENT=========#
def dV(y, CL):
    return -dN(y, CL) + w_dist(y) + f_dist(y)
def dT(y, CL):
    return -dM_N(y, CL) - dM(y, CL)


#=========PLOTTING WEIGHT AND FUEL DISTRIBUTIONS=========#
# create distribution function and plot from 0 to b/2
w_dist = weight_distribution(mass_wing, b, c_r, c_t)
f_dist = fuel_distribution(mass_fuel, n_fuel, b, c_r, c_t)

y = np.linspace(0, b/2, 500)
w = w_dist(y)
f = f_dist(y)

plt.figure()
plt.plot(y, w, lw=2, label="Wing weight w(y)")
plt.plot(y, f, lw=2, linestyle="--", label="Fuel distribution f(y)")
plt.xlabel("Spanwise coordinate y (m)")
plt.ylabel("Weight per unit length (N/m)")
plt.title("Wing and Fuel weight distributions (0 to b/2)")
plt.grid(True)
plt.ylim(bottom=0)
plt.legend()
plt.tight_layout()
plt.show()

