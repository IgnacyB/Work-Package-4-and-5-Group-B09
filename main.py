from XFLRextraction import extract_main_wing_data
from Interpolation import interpolate
from Linearmodel import linear_model
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

ylst,cllst,cdlst,cmlst,CL10 = extract_main_wing_data("MainWing_a=10.00_v=10.00ms.txt")
fcl10,fcd10,fcm10 = interpolate(ylst,cllst,cdlst,cmlst)
ylst,cllst,cdlst,cmlst,CL0 = extract_main_wing_data("MainWing_a=0.00_v=10.00ms.txt")
fcl0,fcd0,fcm0 = interpolate(ylst,cllst,cdlst,cmlst)

Cl = linear_model(fcl0,fcl10,CL10,CL0)
Cd = linear_model(fcd0,fcd10,CL10,CL0)
Cm = linear_model(fcm0,fcm10,CL10,CL0)

def alpha(CL):
    return 10*(CL-CL0)/(CL10-CL0)


# Create ranges
y_vals  = np.linspace(0, max(ylst), 200)
CL_vals = np.linspace(CL0, CL10, 200)

# Create grid
Y, CLgrid = np.meshgrid(y_vals, CL_vals)

# Evaluate your function on the grid
Z = Cd(Y, CLgrid)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(Y, CLgrid, Z)

ax.set_xlabel("y")
ax.set_ylabel("CL")
ax.set_zlabel("Cd(y, CL)")

plt.show()



"""
# Example usage of the interpolated functions
ylst = np.linspace(0, max(ylst), 100)

plt.figure()
plt.plot(ylst, fcl(ylst), label="J0(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.show()
"""