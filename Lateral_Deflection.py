# This is the file used to actually calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp


#import all the information from the other files
from material_properties import E
from MOI import MOI_single_cell




#test
#get from 4.1 people

def Mx(y):
    return 4*y**2

#yipee
def h(y):
    return Mx(y) / (E * MOI_single_cell(y))


def dvdy(y):
    return -1 * sp.integrate.quad(h,0,y)[0]


# Now that all calculating functions have been defined the code beneath does the actual calculations

#input the material the wingbox is made of:
#input the position along the wing span, so this is how far we integrate over the wing
y_pos = float(input("spanwise location: "))

lateral_deflection , error2 = sp.integrate.quad(dvdy,0,y_pos)

print(lateral_deflection)

