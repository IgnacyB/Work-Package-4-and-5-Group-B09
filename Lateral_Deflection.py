# This is the file used to actually calculate the lateral deflection experienced by the wing

#first import the necessary packages and functions from 
import numpy as np
import scipy as sp



#get from 4.1 people
def Mx(y):
    return 4*y ** 2

def Ixx(y):

    return 4*y

def h(y):
    return Mx(y) / (E * Ixx(y))


def dvdy(y):

    return -1 * sp.integrate.quad(h,0,y)[0]


# Now that all calculating functions have been defined the code beneath does the actual calculations

#input the material the wingbox is made of:
E = float(input("Material Young's Modulus: "))
#input the position along the wing span, so this is how far we integrate over the wing
y_pos = input("spanwise location: ")


lateral_deflection , error2 = sp.integrate.quad(dvdy,0,float(y_pos))

print(lateral_deflection)

