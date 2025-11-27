import matplotlib.pyplot as plt

from Wing_geometry import b
from Twist_Distribution import twist
# from Lateral_Deflection import


#lateral deflection graph
def lateral_deflection_graph():
    spanpos = []
    lateral_dist = []

    y_position = 0

    while y_position <= b/2:
        spanpos.append(y_position)
        lateral_dist.append()
        y_position += 0.5

#twist distribution
def twist_distribution_graph():
    spanpos = []
    twist_dist = []

    y_position = 0
    
    while y_position <= b/2:
        spanpos.append(y_position)
        twist_dist.append(twist(y_position))
        y_position += 0.5

    plt.plot(spanpos, twist_dist)
    plt.xlabel("Spanwise position [m]")
    plt.ylabel("Twist distribution [UNIT]")
    plt.show
