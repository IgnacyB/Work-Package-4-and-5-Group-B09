import matplotlib.pyplot as plt
import math

from Aircraft_parameters import b
from Twist_Distribution import twist
from Lateral_Deflection import lateral_deflection


#lateral deflection graph
def lateral_deflection_graph():
    spanpos = []
    lateral_dist = []

    y_position = 0

    while y_position <= b/2:
        spanpos.append(y_position)
        lateral_dist.append(lateral_deflection(y_position))
        y_position += 0.5

    plt.plot(spanpos, lateral_dist)
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Lateral deflection [m]")
    plt.show


#twist distribution
def twist_distribution_graph():
    spanpos = []
    twist_dist = []

    y_position = 0

    while y_position <= b/2:
        spanpos.append(y_position)
        twist_dist.append(twist(y_position)*180/math.pi)
        y_position += 0.5

    plt.plot(spanpos, twist_dist)
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Angle of twist [degree]")
    plt.show

if __name__ == "__main__":
    lateral_deflection_graph()
    twist_distribution_graph()