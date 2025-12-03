import math
from MOI import MOI_at_tip
from CENTROID import get_centroid
from Lateral_Deflection import lateral_deflection_at_tip
from Twist_Distribution import twist_at_tip
from Aircraft_parameters import b, c_r, c_t
from airfoil_geometry import *
from airfoil_geometry import a_stringer as mass_stringer
from airfoil_geometry import n_stringer, a_stringer, location_front, location_rear


## Centroid ##

spar_positions_ratios = [location_front, location_rear]

x_centroid, y_centroid = get_centroid(c_t, spar_positions_ratios, t_front, t_middle, t_rear, t_skin, a_stringer, n_stringer)
print("The x-y location of the centroid is: ({},{})".format(x_centroid,y_centroid))

## Moment of Inertia ##

print("For two spars, the moment of inertia is {}m^4 = {}mm^4".format(MOI_at_tip,MOI_at_tip*1000))

## Lateral Deflection due to Bending ##

print("The lateral deflection at the tip is {}m or {}mm".format(lateral_deflection_at_tip,lateral_deflection_at_tip*1000))

## Twist Angle ##

print("The twist angle at the tip is {} rad or {} degrees".format(twist_at_tip,twist_at_tip*180/math.pi))