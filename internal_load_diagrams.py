import matplotlib.pyplot as plt
import numpy as np
#Importing important constants and functions
from Wing_geometry import b
from load_calculations import V, T, M   
#Defining y values for plotting
y = np.linspace(0, b/2, 100)

#Creating shear force, torque and bending moment arrays
V_arr = np.array([V(yy) for yy in y], dtype=float)
T_arr = np.array([T(yy) for yy in y], dtype=float)
M_arr = np.array([M(yy) for yy in y], dtype=float)

#Function to plot shear force
def plot_shear(y, V_arr):
    plt.figure()
    plt.plot(y, V_arr, lw=2, color='tab:blue')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Shear V(y) [N]")
    plt.title("Internal Shear Force along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Function to plot torque
def plot_torque(y, T_arr):
    plt.figure()
    plt.plot(y, T_arr, lw=2, color='tab:green')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Torque T(y) [N·m]")
    plt.title("Internal Torque along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Function to plot bending moment
def plot_moment(y, M_arr):
    plt.figure()
    plt.plot(y, M_arr, lw=2, color='tab:red')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Bending Moment M(y) [N·m]")
    plt.title("Internal Bending Moment along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Calling the plotting functions
plot_shear(y, V_arr)
plot_torque(y, T_arr)
plot_moment(y, M_arr)