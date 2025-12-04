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

    plt.annotate(f'{v_grid[-1]:2f}', (y_grid[-1], v_grid[-1]), xytext = (-65, -5), textcoords = "offset points", ha = "left", va = "bottom")
    plt.plot(y_grid[-1], v_grid[-1], marker='o', color='blue')

    plt.grid(True)
    plt.show()


# twist distribution
def plot_twist_distribution(title=None):
    """Plot twist distribution. If title provided, include it in the figure title."""
    y_grid, twist_grid = twist_function()

    if twist_grid[-1] < 0:
        plt.gca().invert_yaxis()

    plt.plot(y_grid, twist_grid * 180 / math.pi, lw=2, color="tab:blue")
    if title:
        plt.title(f"{title} — Twist distribution")
    else:
        plt.xlabel("Spanwise position [m]")
        plt.title("Twist distribution along wingspan")
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")

    plt.annotate(f'{twist_grid[-1]*180/math.pi:2f}', (y_grid[-1], twist_grid[-1]*180/math.pi), xytext = (-40, -30), textcoords = "offset points", ha = "left", va = "bottom")
    plt.plot(y_grid[-1], twist_grid[-1]*180/math.pi, marker='o', color='blue')

    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    plot_lateral_deflection()
    plot_twist_distribution()