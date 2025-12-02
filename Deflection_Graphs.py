import matplotlib.pyplot as plt
import math

from Aircraft_parameters import b
from Twist_Distribution import twist_function
from Lateral_Deflection import lateral_deflection_function


#lateral deflection graph
def plot_lateral_deflection():
    spanpos = []
    lateral_dist = []

    y_position = 0

    while y_position <= b/2:
        spanpos.append(y_position)
        lateral_dist.append(lateral_deflection_function(y_position))
        y_position += 0.5
        # print(y_position)

    plt.plot(spanpos, lateral_dist)
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Lateral deflection [m]")
    plt.show()


#twist distribution
def plot_twist_distribution():
    spanpos = []
    twist_dist = []

    y_position = 0

    while y_position <= b/2:
        spanpos.append(y_position)
        twist_dist.append(twist_function(y_position)*180/math.pi)
        y_position += 0.5
        # print(y_position)

    plt.plot(spanpos, twist_dist)
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")
    plt.show()

plot_twist_distribution()