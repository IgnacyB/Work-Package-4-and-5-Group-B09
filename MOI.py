# Moment of inertia calculations
import numpy as np
import scipy as sp

def MOI_single_cell(y):
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

    x_centroid, y_centroid = get_centroid(chord,spars, thickness,mass_stringer,n_stringer)
    print("X_centroid ",x_centroid)
    print("Y_centroid",y_centroid)

    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    #print(stringer_chord)

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness
    MOI_rear_spar = thickness*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness

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
    MOI_stringer =0

    for element in stringer_chord:
        MOI_stringer += np.power(abs(element[1]-y_centroid),2)*mass_stringer

    # sum all the elements together 
    #MOI_total_2 = MOI_front_spar + MOI_rear_spar + MOI_stringer_2 + MOI_top + MOI_bottom + MOI_middle_spar

    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom
   
    
    return MOI_total



def check_even(n):
    if n % 2 ==0:
        even = True
    else:
        even = False

    return even


def MOI_multi_cell(y):

    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_front as thickness
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_rear as chord_position_rear
    from airfoil_geometry import location_middle as chord_position_middle

    from Aircraft_parameters import b, c_r, c_t
    from torsional_stiffness_functions import find_sparheight
    from MOI import check_even
    from CENTROID import generate_stringer_coordinates

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
    
    spars = []

    #calculation for front spar
    spar_front = []
    spar_front_top = []
    spar_front_bottom = []
    
    spar_front_top.append(y_top_front_spar) 
    spar_front_top.append(chord_position_front)
    spar_front_bottom.append(y_bottom_front_spar)
    spar_front_bottom.append(chord_position_front)

    spar_front.append(spar_front_top)
    spar_front.append(spar_front_top)

    #calculation for rear spar
    spar_rear =[]
    spar_rear_top = []
    spar_rear_bottom = []

    spar_rear_top.append(y_top_rear_spar)
    spar_rear_top.append(chord_position_rear)
    spar_rear_bottom.append(y_bottom_rear_spar)
    spar_rear_bottom.append(chord_position_rear)

    spar_rear.append(spar_rear_top)
    spar_rear.append(spar_rear_bottom)

    #calculation for middle spar
    spar_middle = []
    spar_middle_top = []
    spar_middle_bottom = []

    spar_middle_top.append(y_top_middle_spar)
    spar_middle_top.append(chord_position_middle)
    spar_middle_bottom.append(y_bottom_middle_spar)
    spar_middle_bottom.append(chord_position_middle)

    spar_middle.append(spar_middle_top)
    spar_middle.append(spar_middle_bottom)

    #add everything together
    spars.append(spar_front)
    spars.append(spar_rear)
    spars.append(spar_middle)

    stringer_chord = generate_stringer_coordinates(spars,n_stringer)

    MOI_stringer =0

    for element in stringer_chord:
        MOI_stringer += np.power(abs(element[0]-y_centroid),2)*mass_stringer

    # sum all the elements together 
    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom + MOI_middle_spar

    return MOI_total

value = MOI_single_cell(2)
value_2 = MOI_multi_cell(0)

#print("This is the calculated value for Ixx with 2 spars method",value,"m^4")
#print("This is the calculated value for Ixx with 3 spars method",value_2, "m^4")