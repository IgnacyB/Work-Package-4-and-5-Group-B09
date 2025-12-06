#Importing constants and wing geometry
from Aircraft_parameters import b, c_r, c_t, c, S_w

#Importing functions from other files
from Linearmodel import linear_model
from Interpolation import interpolate
from Load_cases import v_cruise, rho_cruise

#import modules
import numpy as np
import matplotlib.pyplot as plt
import io

# NOTE: Do NOT import runtime flight variables from main at module import time.
# Provide a setter so other modules (e.g. load_calculations.set_operating_conditions)
# can configure the flight conditions (rho, v) before calling dL/dD/dM.
_q = None
def set_flight_conditions(rho, v):
    global _q
    _q = 0.5 * rho * v**2

#Calculating dynamic pressure at cruise is deferred until set_flight_conditions is called.

def extract_main_wing_data(filepath):
    y_span = []
    Cl = []
    Cm = []
    Cd_i = []

    with io.open(filepath, 'r',encoding="iso-8859-1") as f:
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
    if _q is None:
        raise RuntimeError("Call XFLRextraction.set_flight_conditions(rho, v) before using dL/dD/dM")
    return Cl(y,CL)*_q*c(y)
def dD(y,CL):
    if _q is None:
        raise RuntimeError("Call XFLRextraction.set_flight_conditions(rho, v) before using dL/dD/dM")
    return Cd(y,CL)*_q*c(y)
def dM(y,CL):
    if _q is None:
        raise RuntimeError("Call XFLRextraction.set_flight_conditions(rho, v) before using dL/dD/dM")
    return Cm(y,CL)*_q*(c(y))**2

def dL_array(y_arr, CL):
    return np.asarray([dL(float(yy), CL) for yy in y_arr], dtype=float)
def dD_array(y_arr, CL):
    return np.asarray([dD(float(yy), CL) for yy in y_arr], dtype=float)
def dM_array(y_arr, CL):
    return np.asarray([dM(float(yy), CL) for yy in y_arr], dtype=float)
#Define AOA as function of CL
def alpha(CL):
    return 10*(CL-CL0)/(CL10-CL0)

def plot_Cm_surface(y_steps=200, CL_steps=200):
    """Plot Cm(y, CL) as a 3D surface (same style as the dL surface plot)."""
    y_vals  = np.linspace(0, max(ylst), y_steps)
    CL_vals = np.linspace(CL0, CL10, CL_steps)

    Y, CLgrid = np.meshgrid(y_vals, CL_vals)
    Z = Cm(Y, CLgrid)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(Y, CLgrid, Z, cmap="viridis", edgecolor='none')

    ax.set_xlabel("y")
    ax.set_ylabel("CL")
    ax.set_zlabel("Cm(y, CL)")
    fig.colorbar(surf, shrink=0.6, label="Cm")

    plt.title("Sectional pitching moment coefficient Cm(y, CL)")
    plt.show()
    
if __name__ == "__main__":
    # quick check (user must set flight conditions before plotting)
    set_flight_conditions(1.225, 10.0)
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

    # also show Cm surface (same style)
    plot_Cm_surface()