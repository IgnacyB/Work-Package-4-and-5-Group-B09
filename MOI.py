# Moment of inertia calculations
import numpy as np
import scipy as sp
from Aircraft_parameters import b
import matplotlib.pyplot as plt
from thickness_distribution import t_front_func, t_middle_func, t_rear_func
#import the necessary functions from other
from airfoil_geometry import t_skin as skin_thickness
from thickness_distribution import t_middle_func
from thickness_distribution import t_front_func
from thickness_distribution import t_rear_func 
from airfoil_geometry import a_stringer as mass_stringer
from airfoil_geometry import n_stringer
from airfoil_geometry import location_front as chord_position_front
from airfoil_geometry import location_rear as chord_position_rear
from airfoil_geometry import location_middle as chord_position_middle
#import needed functions
from Aircraft_parameters import b, c_r, c_t
from torsional_stiffness_functions import find_sparheight
from CENTROID import get_stringer_coordinates_only
from CENTROID import get_centroid

"""
The main MOI function is a logic function. If check for the different cases of the design what equation to use.
So if we have a 3-spars design it allows the 3 spar design to exist up to a certain location and then go back to a 
two spar layout
"""
def MOI(y):
    #import needed parameters about geometry
    from airfoil_geometry import n_spars
    from airfoil_geometry import end_third_spar
    #check amount of spar concepts
    if n_spars > 2:
        #check if third spar still present
        if y < end_third_spar*b/2:
            MOI_value, x_centroid = MOI_multi_cell(y)
        else:
            MOI_value, x_centroid = MOI_single_cell(y)

    else:
        MOI_value, x_centroid = MOI_single_cell(y)

    return MOI_value, x_centroid

"""

The MOI_single_cell and MOI_multi_cell functions are almost identical
The only difference is that the multi_cell has additional lines to calculate the MOI_middle spar
All other MOI which are influenced by the middle spars are function created in such a way that it
does not matter if it is single cell or multi cell

Therefore more in depth working of the code is only explained in single cell, multicell is identical working principle

"""

#MOI function for if we have a single cell design, so two spars
def MOI_single_cell(y):
    thickness_front = t_front_func(y)
    thickness_middle = t_middle_func(y)
    thickness_rear = t_rear_func(y)

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y

    # code to calculate the heigts for the wing box using sparheight()
    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

    #translating height from percentage of chord to meter
    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord

    # creating a list need as input for the function to find the stringer locations
    spars = []
    spars.append(chord_position_front)
    spars.append(chord_position_rear)

    t_spars = []
    t_spars.append(thickness_front)
    t_spars.append(thickness_middle)
    t_spars.append(thickness_rear)

    #getting centroid using centroid function
    x_centroid, y_centroid = get_centroid(chord,spars, thickness_front, thickness_middle, thickness_rear, skin_thickness ,mass_stringer,n_stringer)
    #use centroid location and spar list to find the stringer coordinates
    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    #calculate centroid of spars
    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    #calculate MOI for spars using moi around own axis and parallel axis theorem to wing box centroid
    MOI_front_spar = thickness_front*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness_front
    MOI_rear_spar = thickness_rear*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness_rear

    # code to calculate MOI for top and bottom sections of wingbox
    #first calculate the angle at which flanges sit with respect to horizontal
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    #calculate length of top and bottom flanges
    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)
    #calculate flanges centroids
    y_centroid_top = y_top_front_spar + (y_top_rear_spar-y_top_front_spar)/2
    y_centroid_bottom = y_bottom_front_spar + (y_bottom_rear_spar-y_bottom_front_spar)/2
    #calculate MOI for flanges using a more general equation to calculate centroid about its own axis 
    #for this equation we needed the angle previously calculated
    MOI_top = skin_thickness*distance_top/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_top),2) +np.power(distance_top,2) * np.power(np.sin(alpha_top),2) ) + skin_thickness*distance_top*np.power((y_centroid_top-y_centroid),2)
    MOI_bottom = skin_thickness*distance_bottom/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_bottom),2) + np.power(distance_bottom,2) * np.power(np.sin(alpha_bottom),2)) + skin_thickness*distance_bottom*np.power((y_centroid_bottom-y_centroid),2)
    
    #calculate MOI of stringers combined using parallel axis theorem
    MOI_stringer =0
    for element in stringer_chord:
        MOI_stringer += np.power(abs(element[1]-y_centroid),2)*mass_stringer

    #sum all MOI contribution to find general
    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom
   
    return MOI_total, x_centroid

#calculate MOI in cases of a multicell concept so three spars
def MOI_multi_cell(y):
    #Setup thicknesses
    thickness_front = t_front_func(y)
    thickness_middle = t_middle_func(y)
    thickness_rear = t_rear_func(y)

    #calculate chord
    chord = c_r-((c_r-c_t)/(b/2))*y

    #calculate heights for the three spars
    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)
    y_top_middle_spar_percentage, y_bottom_middle_spar_percentage = find_sparheight(chord_position_middle)
    # convert heights from percentage of chord to meters
    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    y_top_middle_spar = y_top_middle_spar_percentage*chord
    y_bottom_middle_spar = y_bottom_middle_spar_percentage*chord
    #create list of spars 
    spars = []
    spars.append(chord_position_front)
    spars.append(chord_position_middle)
    spars.append(chord_position_rear)

    t_spars = []
    t_spars.append(thickness_front)
    t_spars.append(thickness_middle)
    t_spars.append(thickness_rear)

    #calculate wing box centroid
    x_centroid, y_centroid = get_centroid(chord,spars, thickness_front, thickness_middle, thickness_rear, skin_thickness ,mass_stringer,n_stringer)
    #calculate stringer positions
    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    # code to calculate MOI for front and rear spar
    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2
    MOI_front_spar = thickness_front*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness_front
    MOI_rear_spar = thickness_rear*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness_rear

    #code to calculate middle spar MOI
    y_centroid_middle_spar = (y_top_middle_spar - y_bottom_middle_spar)/2
    MOI_middle_spar = thickness_middle*np.power((y_top_middle_spar-y_bottom_middle_spar),3)/12 + np.power(abs(y_centroid_middle_spar -y_centroid),2)*(y_top_middle_spar - y_bottom_middle_spar)*thickness_middle

    # code to calculate MOI for top and bottom sections of wingbox, same as in 
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

    y_centroid_top = y_top_front_spar + (y_top_rear_spar-y_top_front_spar)/2
    y_centroid_bottom = y_bottom_front_spar + (y_bottom_rear_spar-y_bottom_front_spar)/2

    MOI_top = skin_thickness*distance_top/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_top),2) +np.power(distance_top,2) * np.power(np.sin(alpha_top),2) ) + skin_thickness*distance_top*np.power((y_centroid_top-y_centroid),2)
    MOI_bottom = skin_thickness*distance_bottom/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_bottom),2) + np.power(distance_bottom,2) * np.power(np.sin(alpha_bottom),2)) + skin_thickness*distance_bottom*np.power((y_centroid_bottom-y_centroid),2)
    
    # code to calculate parallel axis for stringer
    MOI_stringer =0

    for element in stringer_chord:
        MOI_stringer += np.power(abs(element[1]-y_centroid),2)*mass_stringer

    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_middle_spar + MOI_stringer + MOI_top + MOI_bottom
   
    return MOI_total, x_centroid


from grid_setup import y_arr
MOI_vec = np.vectorize(MOI)
MOI_grid = MOI_vec(y_arr)[0]  # extract only MOI values, not centroids
cx_grid = MOI_vec(y_arr)[1]  # extract only centroid x locations

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.plot(y_arr, MOI_grid)
    plt.title("Moment of Inertia Distribution along the Wing Span")
    plt.xlabel("Spanwise Location y (m)")
    plt.ylabel("Moment of Inertia Ixx (m^4)")
    plt.grid()
    plt.show()
