from XFLRextraction import extract_main_wing_data
from Interpolation import interpolate
from Linearmodel import linear_model
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from Wing_geometry import b, c_r, c_t

#Extract Cl,Cd,Cm data from XLFR for AOA=0 and AOA=10
ylst,cllst,cdlst,cmlst,CL10 = extract_main_wing_data("MainWing_a=10.00_v=10.00ms.txt")
fcl10,fcd10,fcm10 = interpolate(ylst,cllst,cdlst,cmlst)
ylst,cllst,cdlst,cmlst,CL0 = extract_main_wing_data("MainWing_a=0.00_v=10.00ms.txt")
fcl0,fcd0,fcm0 = interpolate(ylst,cllst,cdlst,cmlst)

#Define chord distribution function and ask for q
def c(y):
    return c_r - (c_r - c_t)*(2*y)/b
q = float(input("Enter dynamic pressure q in N/m^2: "))
Cl = linear_model(fcl0,fcl10,CL10,CL0)
Cd = linear_model(fcd0,fcd10,CL10,CL0)
Cm = linear_model(fcm0,fcm10,CL10,CL0)

#Apply linear model to get L, D, M per unit span as functions of y and CL
def dL(y,CL):
    return Cl(y,CL)*q*c(y)
def dD(y,CL):
    return Cd(y,CL)*q*c(y)
def dM(y,CL):
    return Cm(y,CL)*q*(c(y))**2
    
#Define AOA as function of CL
def alpha(CL):
    return 10*(CL-CL0)/(CL10-CL0)




#Plot data for testing
# Create ranges
y_vals  = np.linspace(0, max(ylst), 200)
CL_vals = np.linspace(CL0, CL10, 200)

# Create grid
Y, CLgrid = np.meshgrid(y_vals, CL_vals)

# Evaluate your function on the grid
Z = Cm(Y, CLgrid)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(Y, CLgrid, Z)

ax.set_xlabel("y")
ax.set_ylabel("CL")
ax.set_zlabel("dL(y, CL)")

plt.show()


