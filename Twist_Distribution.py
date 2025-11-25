
import scipy as sp

#importing variables/functions from other files
from material_properties import G



def T(y):
    return y

def J(y):
    return 2*y

def dthetady(y):
    return T(y) / (G * J(y))

y_pos = int(input("Spanwise location: "))

twist = sp.integrate.quad(dthetady,0,float(y_pos))[0]

print(twist)