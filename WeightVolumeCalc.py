import numpy as np
import scipy as sp
# Code to calculate weight
from Aircraft_parameters import b
from scipy.integrate import quad

def area_of_material (y):
    #import the necessary functions from other
    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_front as thickness
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_rear as chord_position_rear

    from Aircraft_parameters import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight
    from MOI import check_even
    from CENTROID import get_stringer_coordinates_only
    from CENTROID import get_centroid

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y
    # code to open the data file for geometry and location stringers 

    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord

    spars = []
    spars.append(chord_position_front)
    spars.append(chord_position_rear)

    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    #print(stringer_chord)

    # code to calculate MOI for front and rear spar

    A_front_spar = thickness*(y_top_front_spar-y_bottom_front_spar)
    A_rear_spar = thickness*(y_top_rear_spar-y_bottom_rear_spar)
    # code to calculate MOI for top and bottom sections of wingbox
    
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

    A_top = distance_top*skin_thickness
    A_bottom = distance_bottom*skin_thickness

    A_stringer = mass_stringer*n_stringer

    A_total = A_front_spar+A_rear_spar+A_top+A_bottom+A_stringer
   
    return A_total

def area_for_fuel(y):

    #import the necessary functions from other
    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_front as thickness
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_rear as chord_position_rear

    from Aircraft_parameters import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight
    from MOI import check_even
    from CENTROID import get_stringer_coordinates_only
    from CENTROID import get_centroid

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y
    # code to open the data file for geometry and location stringers 

    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord

    Area = ((y_top_front_spar-y_bottom_front_spar)+(y_top_rear_spar-y_bottom_rear_spar))/2*(chord_position_rear*chord-chord_position_front*chord) 

    return Area

#2780 kg/m^3
Density = 2780 

Area_at_root = area_for_fuel(0)
Area_at_tip = area_for_fuel(b/2)
print(Area_at_root)
print(Area_at_tip)

Volume_material, error1 = quad(area_of_material,0,b/2)
Volume_fuel, erro2 = quad(area_for_fuel,0,b/2)

Mass = Density*Volume_material
print("The material volume is ",Volume_material)
print("The fuel volume is ",Volume_fuel, "m^3")
print("The mass of the wingbox structure is", Mass)