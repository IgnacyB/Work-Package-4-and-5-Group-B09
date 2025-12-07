import matplotlib.pyplot as plt
import math

from Aircraft_parameters import b
from Twist_Distribution import twist_function
from Lateral_Deflection import lateral_deflection_function

#Importing y grid
from grid_setup import y_arr

# lateral deflection graph
def plot_lateral_deflection(title=None):
    """Plot lateral deflection. If title provided, include it in the figure title."""

    plt.plot(y_grid, v_grid, lw=2, color="tab:blue")
    if v_grid[-1] < 0:
        plt.gca().invert_yaxis()

    if title:
        plt.title(f"{title} — Lateral deflection")
    else:
        plt.title("Lateral deflection along wingspan")

    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Lateral deflection [m]")

    plt.plot(y_arr[-1], lateral_deflection_function()[-1], marker='o', color='blue')

    plt.annotate(
        f'{lateral_deflection_function()[-1]:.2f}',
        (y_arr[-1], lateral_deflection_function()[-1]),
        xytext=(-40, -10),
        textcoords="offset points",
        ha="left",
        va="bottom")

    plt.grid(True)
    plt.show()



def plot_twist_distribution(title=None):
    """Plot twist distribution. If title provided, include it in the figure title."""
    twist_grid = twist_function()

    # Convert radians → degrees
    twist_deg = twist_grid * 180 / math.pi

    # Plot twist distribution
    plt.plot(y_arr, twist_deg, lw=2, color="tab:blue")

    if title:
        plt.title(f"{title} — Twist distribution")
    else:
        plt.title("Twist distribution along wingspan")

    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")

    plt.plot(y_arr[-1], twist_deg[-1], marker='o', color='blue')

    plt.annotate(
        f'{twist_deg[-1]:.2f}',
        (y_arr[-1], twist_deg[-1]),
        xytext=(-15, -20),
        textcoords="offset points",
        ha="left",
        va="bottom")

    plt.grid(True)
    plt.show()

