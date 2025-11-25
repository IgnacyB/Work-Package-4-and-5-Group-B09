import scipy as sp
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


def interpolate(ylst,cllst,cdlst,cmlst):
    fcl = sp.interpolate.interp1d(ylst, cllst, kind='cubic', fill_value="extrapolate")
    fcd = sp.interpolate.interp1d(ylst, cdlst, kind='cubic', fill_value="extrapolate")
    fcm = sp.interpolate.interp1d(ylst, cmlst, kind='cubic', fill_value="extrapolate")
    return fcl,fcd,fcm

"""
ylst = [1,2,3,4,5]
cllst = [0.2,0.5,0.4,0.3,0.2]
f1,f2,f3 = interpolate(ylst,cllst,cllst,cllst)
ylst = np.linspace(0, max(ylst), 100)

plt.figure()
plt.plot(ylst, f1(ylst), label="J0(x)")
plt.legend()
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.show()

"""

