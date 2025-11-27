
import scipy as sp

#importing variables/functions from other files
from material_properties import G
from torsional_stiffness_functions import torsional_constant_singlecell
from load_calculations import T


def dthetady(y):
    return T(y) / (G * torsional_constant_singlecell(y))

#y_pos = int(input("Spanwise location: "))

def twist(y):
    return sp.integrate.quad(dthetady,0,float(y))[0]

print(twist(5))