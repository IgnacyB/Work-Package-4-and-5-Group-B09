import scipy as sp
import numpy as np




def linear_model(fcl0,fcl10,CL10,CL0):
    #Cl(y,CL)=Clb(y)+(dCl(y)/dCL)*(CL-CL0)

    def Clb(y):
        return fcl0(y)
    
    def m(y):
        return(fcl10(y)-Clb(y))/(CL10-CL0)
    
    def Cl(y,CL):
        return Clb(y)+m(y)*(CL-CL0)

    
    
    return Cl