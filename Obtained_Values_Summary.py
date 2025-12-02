import math

from MOI import value
from
from CENTROID import get_centroid
from Lateral_Deflection import lateral_deflection_at_tip
from Twist_Distribution import twist_at_tip
from airfoil_geometry import t_front as thickness
from airfoil_geometry import a_stringer as mass_stringer
from airfoil_geometry import n_stringer
## Centroid ##
#chord_at_tip = c_r-((c_r-c_t)/(b/2))*(b/2)
#x_centroid, y,centroid = get_centroid(chord_at_tip,spars, thickness,mass_stringer,n_stringer)

## Moment of Inertia ##

print("For two spars, the moment of inertia is {}m^4 = {}mm^4".format(value,value*1000))

## Lateral Deflection due to Bending ##

print("The lateral deflection at the tip is {}m or {}mm".format(lateral_deflection_at_tip,lateral_deflection_at_tip*100))

## Twist Angle ##

print("The twist angle at the tip is {} rad or {} degrees".format(twist_at_tip,twist_at_tip*180/math.pi))