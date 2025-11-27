import matplotlib.pyplot as plt
import math
from math import sin,cos,pi
import numpy as np

a1=[2,3]
b1=[2,-1]
a2=[4,2]
b2=[4,-3]
a3=[6,1]
b3=[6,-1]

t=0.2
spar=3
for i in range(1,spar+1):


spar1H=a1[1]-b1[1]

spar2H=a2[1]-b2[1]

spar3H=a3[1]-b3[1]


roofL=math.sqrt((a2[1]-a1[1])**2+(a2[0]-a1[0])**2)
BottomL=math.sqrt((b2[1]-b1[1])**2+(b2[0]-b1[0])**2)

theta1A=np.arctan((a2[0]-a1[0])/(a2[1]-a1[1]))
theta1B=np.arctan((b2[0]-b1[0])/(b2[1]-b1[1]))



centroidRoof_X=a1[0]+sin(theta1A)*roofL/2
centroidRoof_Y=a1[1]-cos(theta1A)*roofL/2


centroidBottom_X=b1[0]+sin(theta1B)*BottomL/2
centroidBottom_Y=b1[1]-cos(theta1A)*roofL/2

centroidspar1=a1[1]-spar1H/2
centroidspar2=a2[1]-spar2H/2
centroidspar3=a3[1]-spar3H/2




xprime=(spar1H*a1[0]*t +spar2H*a2[0]*t +spar3H*a3[0]*t+  roofL*centroidRoof_X*t+  BottomL*centroidBottom_X*t)/((spar1H+spar2H+spar3H+roofL+BottomL)*t)


yprime=(spar1H*centroidspar1*t +spar2H*centroidspar2*t +spar3H*centroidspar3*t+  roofL*centroidRoof_Y*t+  BottomL*centroidBottom_Y*t)/((spar1H+spar2H+spar3H+roofL+BottomL)*t)


print(xprime)
print(yprime)