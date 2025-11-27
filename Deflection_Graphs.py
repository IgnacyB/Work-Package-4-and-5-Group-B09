from Wing_geometry import b
from Twist_Distribution import twist
# from Lateral_Deflection import

y_position = 0
spanpos = []
twist_dist = []
lateral_dist = []

#lateral deflection graph

#twist distribution

while y_position <= b/2:
    twist_dist.append(twist(y_position))
    y += 0.5


