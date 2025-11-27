
import scipy as sp

#importing variables/functions from other files
from material_properties import G
from torsional_stiffness_functions import torsional_constant_singlecell


def T(y):
    return y

def dthetady(y):
    return T(y) / (G * torsional_constant_singlecell(y))

y_pos = int(input("Spanwise location: "))

twist = sp.integrate.quad(dthetady,0,float(y_pos))[0]

print(twist)