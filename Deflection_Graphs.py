import matplotlib.pyplot as plt
import math

from Aircraft_parameters import b
from Twist_Distribution import twist_function
from Lateral_Deflection import lateral_deflection_function


# lateral deflection graph
def plot_lateral_deflection(title=None):
    """Plot lateral deflection. If title provided, include it in the figure title."""
    y_grid, v_grid = lateral_deflection_function()

    plt.plot(y_grid, v_grid, lw=2, color="tab:blue")
    if title:
        plt.title(f"{title} — Lateral deflection")
    else:
        plt.title("Lateral deflection along wingspan")
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Lateral deflection [m]")
    plt.grid(True)
    plt.show()


# twist distribution
def plot_twist_distribution(title=None):
    """Plot twist distribution. If title provided, include it in the figure title."""
    y_grid, twist_grid = twist_function()

    plt.plot(y_grid, twist_grid * 180 / math.pi, lw=2, color="tab:blue")
    if title:
        plt.title(f"{title} — Twist distribution")
    else:
        plt.xlabel("Spanwise position [m]")
        plt.title("Twist distribution along wingspan")
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    plot_lateral_deflection()
    plot_twist_distribution()