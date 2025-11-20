#Importing necessary libraries
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

#Importing necessary constants
from constants import g, rho_air
b = 15  # Wing span in meters (example value)
mass_wing = 690 # Mass of the wing in kg (example value)
c_r = 2.75  # Root chord length in meters (example value)
c_t = 1 # Tip chord length in meters (example value)
mass_fuel = 1200  # Total fuel mass in kg (example value)
n_fuel = 0.8  # Fraction of fuel in the wing (example value)

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

jhadsjhjkldhask