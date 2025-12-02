import math
from MOI import MOI_at_tip
#from CENTROID import get_centroid
from Lateral_Deflection import lateral_deflection_at_tip
from Twist_Distribution import twist_at_tip
from Aircraft_parameters import b, c_r, c_t
from airfoil_geometry import t_front as thickness
from airfoil_geometry import a_stringer as mass_stringer
from airfoil_geometry import n_stringer, a_stringer, location_front, location_rear
## Centroid ##


#x_centroid, y_centroid = get_centroid(chord_at_tip, spar_positions_ratios, thickness, a_stringer, n_stringer)
#print(x_centroid,y_centroid)
## Moment of Inertia ##

print("For two spars, the moment of inertia is {}m^4 = {}mm^4".format(MOI_at_tip,MOI_at_tip*1000))

## Lateral Deflection due to Bending ##

print("The lateral deflection at the tip is {}m or {}mm".format(lateral_deflection_at_tip,lateral_deflection_at_tip*100))

## Twist Angle ##

print("The twist angle at the tip is {} rad or {} degrees".format(twist_at_tip,twist_at_tip*180/math.pi))