import matplotlib.pyplot as plt
import math

from Aircraft_parameters import b
from Twist_Distribution import twist_function
from Lateral_Deflection import lateral_deflection_function


#lateral deflection graph
def plot_lateral_deflection():
    y_grid, v_grid = lateral_deflection_function()

    plt.plot(y_grid, v_grid, lw = 2, color = "tab:blue")
    plt.title("Lateral deflection along wingspan")
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Lateral deflection [m]")
    plt.show()

plot_lateral_deflection()

#twist distribution
def plot_twist_distribution():
    y_grid, twist_grid = twist_function()

    plt.plot(y_grid, twist_grid, lw = 2, color = "tab:blue")
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")
    plt.show()

plot_twist_distribution()
