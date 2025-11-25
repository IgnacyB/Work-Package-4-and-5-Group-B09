# Moment of inertia calculations
import numpy as np
import scipy as sp

def MOI(chord,chord_position_front,chord_position_rear,
        thickness,skin_thickness,
        n_stringer, mass_stringer):
    
    MOI_total = 0
    # code to open the data file for geometry and centroid

    y_top_front_spar_percentage, y_bottom_front_spar_percentage = find_sparheight(chord_position_front)
    y_top_rear_spar_percentage, y_bottom_rear_spar_percentage = find_sparheight(chord_position_rear)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    print(y_top_front_spar)
    y_centroid = 0

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness
    print(MOI_front_spar)
    MOI_rear_spar = thickness*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness
    print(MOI_rear_spar)
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
    
def find_sparheight(chord_pos):
    x_pos_upper = [1.00000, 0.95033, 0.90066, 0.85090, 0.80103, 0.75107, 0.70101, 0.65086, 0.60064, 0.55035, 0.50000,  0.44962, 0.39923, 0.34884, 0.29846, 0.24881, 0.19781, 0.14757, 0.09746, 0.07247, 0.04757, 0.02283, 0.01059, 0.00580, 0.00347, 0.00000]
    x_pos_lower = [0.00000, 0.00653, 0.00920, 0.01441, 0.02717, 0.05243, 0.07753, 0.10254, 0.15243, 0.20219, 0.25189, 0.30154, 0.35116, 0.40077, 0.45038, 0.50000, 0.54965, 0.59936, 0.64914, 0.69899, 0.74893, 0.79897, 0.84910, 0.89934, 0.94967, 1.00000]
    y_pos_upper = [0.00000, 0.00986, 0.01979, 0.02974, 0.03935, 0.04847, 0.05686, 0.06440, 0.07085, 0.07602, 0.07963, 0.08139, 0.08139, 0.07971, 0.07658, 0.07193, 0.06562, 0.05741, 0.04672, 0.04010, 0.03227, 0.02234, 0.01588, 0.01236, 0.01010, 0.00000]
    y_pos_lower = [0.00000, -0.00810, -0.00956, -0.01160, -0.01490, -0.01963, -0.02314, -0.02604, -0.03049, -0.03378, -0.03613, -0.03770, -0.03851, -0.03855, -0.03759, -0.03551, -0.03222, -0.02801, -0.02320, -0.01798, -0.01267, -0.00751, -0.00282, 0.00089, 0.00278, 0.00000]
    y_upper = sp.interpolate.interp1d(x_pos_upper, y_pos_upper, kind="linear", fill_value="extrapolate")
    y_lower = sp.interpolate.interp1d(x_pos_lower, y_pos_lower, kind="linear", fill_value="extrapolate")

    return float(y_upper(chord_pos)), float(y_lower(chord_pos))
    

value = MOI(2,0.2,0.7,0.02,0.02,8,0.1)

print(value)