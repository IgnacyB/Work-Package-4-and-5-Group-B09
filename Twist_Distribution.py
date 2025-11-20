import math as np
import scipy as sp
#from scipy.integrate import dblquad

G = int(input("Material G Modulus: "))

def T(y):
    return y


def J(y):
    return 2*y

def dthetady(y):
    return T(y) / (G * J(y))

y_pos = int(input("Spanwise location: "))

twist = sp.integrate.quad(dthetady,0,float(y_pos))[0]

print(twist)