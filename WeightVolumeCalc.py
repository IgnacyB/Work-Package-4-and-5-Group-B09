import numpy as np

# Code to calculate weight
from Aircraft_parameters import b
from scipy.integrate import quad

def area_of_material (y):
    #import the necessary functions from other
    from airfoil_geometry import t_skin as skin_thickness
    #from airfoil_geometry import t_front as thickness_front
    #from airfoil_geometry import t_middle as thickness_middle
    #from airfoil_geometry import t_rear as thickness_rear
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_middle as chord_position_middle
    from airfoil_geometry import location_rear as chord_position_rear
    from airfoil_geometry import n_spars 
    from airfoil_geometry import end_third_spar

    from Aircraft_parameters import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight
    import thickness_distribution as t

    thickness_front = t.t_front_func(y)
    thickness_middle =  t.t_middle_func(y)
    thickness_rear = t.t_rear_func(y)


    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y
    # code to open the data file for geometry and location stringers 

    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)
    y_top_middle_spar_percentage, y_bottom_middle_spar_percentage = find_sparheight(chord_position_middle)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    y_top_middle_spar = y_top_middle_spar_percentage*chord
    y_bottom_middle_spar = y_bottom_middle_spar_percentage*chord

    A_front_spar = thickness_front*(y_top_front_spar-y_bottom_front_spar)
    A_rear_spar = thickness_rear*(y_top_rear_spar-y_bottom_rear_spar)

    # code to calculate MOI for front and rear spar
    if n_spars > 2 and y < end_third_spar*b/2:

        A_middle_spar = thickness_middle*(y_top_middle_spar-y_bottom_middle_spar)
        
        A_flange_top_front = skin_thickness*np.sqrt(np.power((y_top_middle_spar-y_top_front_spar),2) + np.power((chord_position_middle*chord-chord_position_front*chord),2))
        A_flange_bottom_front = skin_thickness*np.sqrt(np.power((y_bottom_middle_spar-y_bottom_front_spar),2) + np.power((chord_position_middle*chord-chord_position_front*chord),2))
        A_top = A_flange_top_front + A_flange_bottom_front

        A_flange_top_rear = skin_thickness*np.sqrt(np.power((y_top_middle_spar-y_top_rear_spar),2) + np.power((chord_position_middle*chord-chord_position_rear*chord),2))
        A_flange_bottom_rear = skin_thickness*np.sqrt(np.power((y_bottom_middle_spar-y_bottom_front_spar),2) + np.power((chord_position_middle*chord-chord_position_front*chord),2))
        A_bottom = A_flange_top_rear + A_flange_bottom_rear
        
    else:

        alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
        alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

        distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
        distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

        A_top = distance_top*skin_thickness
        A_bottom = distance_bottom*skin_thickness
        A_middle_spar = 0

    A_stringer = mass_stringer*n_stringer

    A_total = A_front_spar+A_rear_spar+A_top+A_bottom+A_stringer + A_middle_spar
   
    return A_total

def area_for_fuel(y):

    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_middle as chord_position_middle
    from airfoil_geometry import location_rear as chord_position_rear
    from airfoil_geometry import n_spars 
    from airfoil_geometry import end_third_spar

    from Aircraft_parameters import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y
    # code to open the data file for geometry and location stringers 

        #
    if n_spars > 2 and y < end_third_spar*b/2:

        y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
        y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)
        y_top_middle_spar_percentage, y_bottom_middle_spar_percentage = find_sparheight(chord_position_middle)

        y_top_front_spar= y_top_front_spar_percentage*chord
        y_top_rear_spar= y_top_rear_spar_percentage*chord
        y_bottom_front_spar= y_bottom_front_spar_percentage*chord
        y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
        y_top_middle_spar = y_top_middle_spar_percentage*chord
        y_bottom_middle_spar = y_bottom_middle_spar_percentage*chord

        Area_1 = ((y_top_front_spar-y_bottom_front_spar)+(y_top_middle_spar-y_bottom_middle_spar))/2*(chord_position_middle*chord-chord_position_front*chord)
        Area_2 = ((y_top_rear_spar-y_bottom_rear_spar)+ (y_top_middle_spar-y_bottom_middle_spar))/2*(chord_position_rear*chord - chord_position_middle*chord)
        Area = Area_1+Area_2

        return Area

    else:

        y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
        y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

        y_top_front_spar= y_top_front_spar_percentage*chord
        y_top_rear_spar= y_top_rear_spar_percentage*chord
        y_bottom_front_spar= y_bottom_front_spar_percentage*chord
        y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord

        Area = ((y_top_front_spar-y_bottom_front_spar)+(y_top_rear_spar-y_bottom_rear_spar))/2*(chord_position_rear*chord-chord_position_front*chord) 

    return Area

#2780 kg/m^3
from material_properties import rho as Density
from grid_setup import y_arr

Volume_material, error1 = quad(area_of_material,0,b/2)
Volume_fuel, error2 = quad(area_for_fuel,0,b/2)

Mass = Density*Volume_material
print("The volume is ",Volume_material)
print("The fuel volume is ",Volume_fuel, "m^3")
print("The mass of the wingbox structure is", Mass, "kg")