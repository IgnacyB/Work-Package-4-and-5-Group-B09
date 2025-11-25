# Moment of inertia calculations
import numpy as np
import scipy as sp

def MOI_single_cell(y):

    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_front as thickness
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_rear as chord_position_rear

    from Wing_geometry import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y

    # code to open the data file for geometry and centroid

    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    y_centroid = 0

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness
    MOI_rear_spar = thickness*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness
    # code to calculate MOI for middle spar

    MOI_middle_spar = 0

    # code to calculate MOI for top and bottom sections of wingbox
    
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

    y_centroid_top = y_top_front_spar + (y_top_rear_spar-y_top_front_spar)/2
    y_centroid_bottom = y_bottom_front_spar + (y_bottom_rear_spar-y_bottom_front_spar)/2

    MOI_top = skin_thickness*distance_top/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_top),2) +np.power(distance_top,2) * np.power(np.sin(alpha_top),2) ) + thickness*distance_top*np.power((y_centroid_top-y_centroid),2)
    MOI_bottom = skin_thickness*distance_bottom/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_bottom),2) + np.power(distance_bottom,2) * np.power(np.sin(alpha_bottom),2)) + thickness*distance_bottom*np.power((y_centroid_bottom-y_centroid),2)
    # code to calculate parallel axis for stringer

    MOI_stringer = np.power(abs(y_top_front_spar - y_centroid),2)*mass_stringer + np.power(abs(y_bottom_front_spar-y_centroid),2)*mass_stringer + np.power(abs(y_top_rear_spar-y_centroid),2)*mass_stringer + np.power(abs(y_bottom_rear_spar - y_centroid),2)*mass_stringer 

    if n_stringer > 4:

        check = check_even(n_stringer)
        n_stringer_after_corners = n_stringer - 4

        if not check:
            n_stringer_top  = round(n_stringer_after_corners/2)
            n_stringer_bottom = n_stringer_top -1

            for i in range(n_stringer_top):
                slope_step_top = (y_top_rear_spar-y_top_front_spar)/(n_stringer_top+1)

                y_new_position_top = y_top_front_spar + slope_step_top*i

                MOI_stringer += abs(y_new_position_top-y_centroid)*mass_stringer

            for i in range(n_stringer_bottom):
                slope_step_bottom = (y_bottom_rear_spar-y_bottom_front_spar)/(n_stringer_bottom+1)

                y_new_position_bottom = y_bottom_front_spar + slope_step_bottom*i

                MOI_stringer += abs(y_new_position_bottom-y_centroid)*mass_stringer

        else:
            n_stringer_top  = int(n_stringer_after_corners/2)
            n_stringer_bottom = n_stringer_top

            for i in range(n_stringer_top):
                slope_step_top = (y_top_rear_spar-y_top_front_spar)/n_stringer_top

                y_new_position_top = y_top_front_spar + slope_step_top*i

                MOI_stringer += abs(y_new_position_top-y_centroid)*mass_stringer

            for i in range(n_stringer_bottom):
                slope_step_bottom = (y_bottom_rear_spar-y_bottom_front_spar)/n_stringer_bottom

                y_new_position_bottom = y_bottom_front_spar + slope_step_bottom*i

                MOI_stringer += abs(y_new_position_bottom-y_centroid)*mass_stringer
    # sum all the elements together 
    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom + MOI_middle_spar

    return MOI_total



def check_even(n):
    if n % 2 ==0:
        even = True
    else:
        even = False

    return even


def MOI_multi_cell(y,chord_position_front,chord_position_middle,chord_position_rear,
        thickness,skin_thickness,
        n_stringer, mass_stringer):

    chord = c_r-((c_r-c_t)/(b/2))*y

    MOI_total = 0
    
    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)
    y_top_middle_spar_percentage, y_bottom_middle_spar_percentage = find_sparheight(chord_position_middle)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    y_top_middle_spar = y_top_middle_spar_percentage*chord
    y_bottom_middle_spar = y_bottom_middle_spar_percentage*chord

    y_centroid = 0

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness
    MOI_rear_spar = thickness*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness

    # code to calculate MOI for middle spar

    y_centroid_middle_spar = (y_top_middle_spar - y_bottom_middle_spar)/2
    MOI_middle_spar = thickness*np.power((y_top_middle_spar-y_bottom_middle_spar),3)/12 + np.power(abs(y_centroid_middle_spar -y_centroid),2)*(y_top_middle_spar - y_bottom_middle_spar)*thickness
   
    # code to calculate MOI for top and bottom sections of wingbox
    
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

    y_centroid_top = y_top_front_spar + (y_top_rear_spar-y_top_front_spar)/2
    y_centroid_bottom = y_bottom_front_spar + (y_bottom_rear_spar-y_bottom_front_spar)/2

    MOI_top = skin_thickness*distance_top/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_top),2) +np.power(distance_top,2) * np.power(np.sin(alpha_top),2) ) + thickness*distance_top*np.power((y_centroid_top-y_centroid),2)
    MOI_bottom = skin_thickness*distance_bottom/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_bottom),2) + np.power(distance_bottom,2) * np.power(np.sin(alpha_bottom),2)) + thickness*distance_bottom*np.power((y_centroid_bottom-y_centroid),2)
    
    # code to calculate parallel axis for stringer
    # there is a minimum of 8 for a multicell design
    MOI_stringer = np.power(abs(y_top_front_spar - y_centroid),2)*mass_stringer + np.power(abs(y_bottom_front_spar-y_centroid),2)*mass_stringer + np.power(abs(y_top_rear_spar-y_centroid),2)*mass_stringer + np.power(abs(y_bottom_rear_spar - y_centroid),2)*mass_stringer + 2*np.power(abs(y_top_middle_spar-y_centroid),2)*mass_stringer + 2* np.power(abs(y_bottom_middle_spar-y_centroid),2)*mass_stringer

    # sum all the elements together 
    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom + MOI_middle_spar

    return MOI_total

value = MOI_single_cell(2)

print(value)