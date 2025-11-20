from XFLRextraction import extract_main_wing_data
from Interpolation import interpolate
from Linearmodel import linear_model
import matplotlib.pyplot as plt
import numpy as np

ylst,cllst,cdlst,cmlst,CL10 = extract_main_wing_data("MainWing_a=10.00_v=10.00ms.txt")
fcl10,fcd10,fcm10 = interpolate(ylst,cllst,cdlst,cmlst)
ylst,cllst,cdlst,cmlst,CL0 = extract_main_wing_data("MainWing_a=0.00_v=10.00ms.txt")
fcl0,fcd0,fcm0 = interpolate(ylst,cllst,cdlst,cmlst)

Cl = linear_model(fcl0,fcl10,CL10,CL0)



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