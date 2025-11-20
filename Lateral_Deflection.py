
import scipy as sp


E = float(input("Material Young's Modulus: "))


def Mx(y):
    return 4*y ** 2

def Ixx(y):
    return 4*y

def h(y):
    return Mx(y) / (E * Ixx(y))


def dvdy(y):
    return -1 * sp.integrate.quad(h,0,y)[0]

y_pos = input("spanwise location: ")

lateral_deflection , error2 = sp.integrate.quad(dvdy,0,float(y_pos))

print(lateral_deflection)

