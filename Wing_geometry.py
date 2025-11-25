from xflr_geometry_extraction import wing_geometry

#Here put all of the wing geometry parameters
b, c_r, c_t = wing_geometry("Plane Name.avl")
'''
b = 17.05  # Wing span in meters
c_r = 2.75  # Root chord length in meters
c_t = 1  # Tip chord length in meters
'''
S_w = 31.95  # Wing area in square meters
AR = 9.1  # Aspect ratio
eff_AR = 10.1  # Effective aspect ratio
taper_ratio = c_t / c_r  # Taper ratio
sweep_LE = 15  # Leading edge sweep angle in degrees
sweep_quarter = 10  # Quarter-chord sweep angle in degrees
dihedral = 5  # Dihedral angle in degrees
