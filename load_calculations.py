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

#=========WEIGHT CALCULATIONS=========#

#WEIGHT DISTRIBUTION (HALF OF SPAN)
def weight_distribution(mass_wing, b, c_r, c_t):

    y_0 = b / 2 * c_r / (c_r - c_t) #location where the load distribution becomes zero

    A = 3 / 2 * mass_wing*g / 2 / (y_0**3-(y_0 - b/2)**3)
    def w_dist(y):
        return A * (y_0 - y)**2
    
    return w_dist

# create distribution function and plot from 0 to b/2
y_0 = b / 2 * c_r / (c_r - c_t)
w_dist = weight_distribution(mass_wing, b, c_r, c_t)
y = np.linspace(0, b/2, 500)
w = w_dist(y)

plt.figure()
plt.plot(y, w, lw=2)
plt.xlabel("Spanwise coordinate y (m)")
plt.ylabel("Weight per unit length w(y) (N/m)")
plt.title("Wing weight distribution (half-span)")
plt.grid(True)
plt.tight_layout()
plt.show()