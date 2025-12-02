import math

from MOI import value, MOI_single_cell
#from CENTROID import cx,cy
from Lateral_Deflection import lateral_deflection_at_tip
from Twist_Distribution import twist_at_tip
## Centroid ##

#print(cx,cy)

## Moment of Inertia ##

print("For two spars, the moment of inertia is {}m^4 = {}mm^4".format(value,value*1000))

## Lateral Deflection due to Bending ##

print("The lateral deflection at the tip is {}m or {}mm".format(lateral_deflection_at_tip,lateral_deflection_at_tip*100))

## Twist Angle ##

print("The twist angle at the tip is {} rad or {} degrees".format(twist_at_tip,twist_at_tip*180/math.pi))