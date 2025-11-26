import matplotlib.pyplot as plt
import numpy as np
#Importing important constants and functions
from Wing_geometry import b
from load_calculations import V, T, M   
#Defining y values for plotting
y = np.linspace(0, b/2, 100)



#Function to plot shear force
def plot_shear(y, V):
    plt.figure()
    plt.plot(y, V, lw=2, color='tab:blue')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Shear V(y) [N]")
    plt.title("Internal Shear Force along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Function to plot torque
def plot_torque(y, T):
    plt.figure()
    plt.plot(y, T, lw=2, color='tab:green')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Torque T(y) [N·m]")
    plt.title("Internal Torque along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Function to plot bending moment
def plot_moment(y, M):
    plt.figure()
    plt.plot(y, M, lw=2, color='tab:red')
    plt.axhline(0, color='k', lw=0.6)
    plt.xlabel("Spanwise coordinate y (m)")
    plt.ylabel("Internal Bending Moment M(y) [N·m]")
    plt.title("Internal Bending Moment along wing span")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#Calling the plotting functions
plot_shear(y, V(y))
plot_torque(y, T(y))
plot_moment(y, M(y))