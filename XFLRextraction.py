#Importing constants and wing geometry
from Aircraft_parameters import b, c_r, c_t, c, S_w
from Load_cases import v_cruise, rho_cruise

#Importing functions from other files
from Linearmodel import linear_model
from Interpolation import interpolate

#import modules
import numpy as np
import matplotlib.pyplot as plt

#Calculating dynamic pressure at cruise
q = 0.5*rho_cruise*v_cruise**2

def extract_main_wing_data(filepath):
    y_span = []
    Cl = []
    Cm = []
    Cd_i = []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find the Cl of the whole wing
    line10 = lines[9].strip()
    CL_wing = float(line10.split("=")[1].strip())


    # Locate the "Main Wing" section
    i = 0
    while i < len(lines) and "Main Wing" not in lines[i]:
        i += 1

    # Skip the "Main Wing" line and the header line
    i += 2

    # Parse numerical table until a blank or non-numeric line is reached
    while i < len(lines):
        line = lines[i].strip()

        # Stop when reaching a blank line or next section
        if line == "" or not line[0].isdigit() and line[0] not in "-":
            break

        parts = line.split()
        if len(parts) >= 4:
            y_span.append(float(parts[0]))
            Cl.append(float(parts[3]))
            Cm.append(float(parts[7]))
            Cd_i.append(float(parts[5]))

        i += 1

    return y_span, Cl, Cd_i, Cm, CL_wing

'''
# Example usage:
file_path = "MainWing_a=10.00_v=10.00ms.txt"
y, cl, cm, cd_i, CL= extract_main_wing_data(file_path)

print("y-span:", y)
print("Cl:", cl)
print("Cm:", cm)
print("Cd_i:", cd_i)
'''

#===============Extraction and calculation of aerodynamic force distributions===============#

#Extract Cl,Cd,Cm data from XLFR for AOA=0 and AOA=10
ylst,cllst,cdlst,cmlst,CL10 = extract_main_wing_data("MainWing_a=10.00_v=10.00ms.txt")
fcl10,fcd10,fcm10 = interpolate(ylst,cllst,cdlst,cmlst)
ylst,cllst,cdlst,cmlst,CL0 = extract_main_wing_data("MainWing_a=0.00_v=10.00ms.txt")
fcl0,fcd0,fcm0 = interpolate(ylst,cllst,cdlst,cmlst)

#Define Cl,Cd,Cm as functions of y and CL using linear model between AOA=0 and AOA=10 data
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

if __name__ == "__main__":
    #Plot data for testing
    # Create ranges
    y_vals  = np.linspace(0, max(ylst), 200)
    CL_vals = np.linspace(CL0, CL10, 200)

    # Create grid
    Y, CLgrid = np.meshgrid(y_vals, CL_vals)

    # Evaluate your function on the grid
    Z = dL(Y, CLgrid)

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(Y, CLgrid, Z)

    ax.set_xlabel("y")
    ax.set_ylabel("CL")
    ax.set_zlabel("dL(y, CL)")

    plt.show()