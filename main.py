from XFLRextraction import extract_main_wing_data
from Interpolation import interpolate
import matplotlib.pyplot as plt
import numpy as np

ylst,cllst,cdlst,cmlst = extract_main_wing_data("MainWing_a=10.00_v=10.00ms.txt")
fcl,fcd,fcm = interpolate(ylst,cllst,cdlst,cmlst)





# Example usage of the interpolated functions
ylst = np.linspace(0, max(ylst), 100)

plt.figure()
plt.plot(ylst, fcl(ylst), label="J0(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.show()
