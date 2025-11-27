     #Here put all relevant aircraft parameters

#============WING GEOMETRY PARAMETERS=========#
from xflr_geometry_extraction import wing_geometry

#Here put all of the wing geometry parameters
b, c_r, c_t = wing_geometry("Plane Name.avl")
S_w = 31.95  # Wing area in square meters
AR = 9.1  # Aspect ratio
eff_AR = 10.1  # Effective aspect ratio
taper_ratio = c_t / c_r  # Taper ratio
sweep_LE = 15  # Leading edge sweep angle in degrees
sweep_quarter = 10  # Quarter-chord sweep angle in degrees
dihedral = 5  # Dihedral angle in degrees

# Chord distribution function
def c(y):
    return c_r - (c_r - c_t)*(2*y)/b

#=============MASS PARAMETERS============#
from Load_cases import mass_aircraft, mass_fuel
mass_aircraft = mass_aircraft  # Mass of the aircraft in kg
mass_fuel = mass_fuel  # Total fuel mass in kg
mass_wing = 690  # Mass of the wing
n_fuel = 0.8  # Fraction of fuel in the wing
