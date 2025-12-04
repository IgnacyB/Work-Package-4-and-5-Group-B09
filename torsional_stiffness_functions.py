import numpy as np
import scipy as sp
from scipy import interpolate


#function that takes the chordwise position of a spar as input and outputs the y-coordinates of the upper and lower airfoil surfaces
#function is done
def find_sparheight(chord_pos):
    x_pos_upper = [1.00000, 0.95033, 0.90066, 0.85090, 0.80103, 0.75107, 0.70101, 0.65086, 0.60064, 0.55035, 0.50000,  0.44962, 0.39923, 0.34884, 0.29846, 0.24881, 0.19781, 0.14757, 0.09746, 0.07247, 0.04757, 0.02283, 0.01059, 0.00580, 0.00347, 0.00000]
    x_pos_lower = [0.00000, 0.00653, 0.00920, 0.01441, 0.02717, 0.05243, 0.07753, 0.10254, 0.15243, 0.20219, 0.25189, 0.30154, 0.35116, 0.40077, 0.45038, 0.50000, 0.54965, 0.59936, 0.64914, 0.69899, 0.74893, 0.79897, 0.84910, 0.89934, 0.94967, 1.00000]
    y_pos_upper = [0.00000, 0.00986, 0.01979, 0.02974, 0.03935, 0.04847, 0.05686, 0.06440, 0.07085, 0.07602, 0.07963, 0.08139, 0.08139, 0.07971, 0.07658, 0.07193, 0.06562, 0.05741, 0.04672, 0.04010, 0.03227, 0.02234, 0.01588, 0.01236, 0.01010, 0.00000]
    y_pos_lower = [0.00000, -0.00810, -0.00956, -0.01160, -0.01490, -0.01963, -0.02314, -0.02604, -0.03049, -0.03378, -0.03613, -0.03770, -0.03851, -0.03855, -0.03759, -0.03551, -0.03222, -0.02801, -0.02320, -0.01798, -0.01267, -0.00751, -0.00282, 0.00089, 0.00278, 0.00000]
    y_upper = sp.interpolate.interp1d(x_pos_upper, y_pos_upper, kind="linear", fill_value="extrapolate")
    y_lower = sp.interpolate.interp1d(x_pos_lower, y_pos_lower, kind="linear", fill_value="extrapolate")

    return float(y_upper(chord_pos)), float(y_lower(chord_pos))


#import data
from airfoil_geometry import *
from Aircraft_parameters import c_r, c_t, b
from material_properties import G

def torsional_constant(y):
    #calculating J for MULTICELL -> THREE SPARS
    if n_spars > 2 and y < end_third_spar*b/2: 

            #calculate c as a function of y
            c = c_r-((c_r-c_t)/(b/2))*y

            #calculate distance to upper and lower surface for 3 spars
            h_upper_front, h_lower_front = find_sparheight(location_front)
            h_upper_middle, h_lower_middle = find_sparheight(location_middle)
            h_upper_rear, h_lower_rear = find_sparheight(location_rear)

            #calculate lenghts of upper and lower wingbox components
            l_upper_1 = np.sqrt(((location_middle-location_front)*c)**2+((h_upper_middle-h_upper_front)*c)**2)
            l_lower_1 = np.sqrt(((location_middle-location_front)*c)**2+((h_lower_middle-h_lower_front))**2)
            l_upper_2 = np.sqrt(((location_rear-location_middle)*c)**2+((h_upper_rear-h_upper_middle)*c)**2)
            l_lower_2 = np.sqrt(((location_rear-location_middle)*c)**2+((h_lower_rear-h_lower_middle))**2)

            #calculate enclosed areas 
            A_1 = ((location_middle-location_front)*c*c*((h_upper_front-h_lower_front)+(h_upper_middle-h_lower_middle)))/2
            A_2 = ((location_rear-location_middle)*c*c*((h_upper_middle-h_lower_middle)+(h_upper_rear-h_lower_rear)))/2

            #set up system of equations with variables: q_1, q_2, twist_rate.
            lefthand_matrix = np.array([[2*A_1, 2*A_2, 0.], [(-1/(2*A_1))*((((h_upper_middle-h_lower_middle)*c)/(G*t_middle))+((l_upper_1)/(G*t_skin))+(((h_upper_front-h_lower_front)*c)/(G*t_front))+((l_lower_1)/(G*t_skin))), (((h_upper_middle-h_lower_middle)*c)/(2*A_1*G*t_middle)), 1], [(((h_upper_middle-h_lower_middle)*c)/(2*A_2*G*t_middle)), ((-1/(2*A_2))*((((h_upper_rear-h_lower_rear)*c)/(G*t_rear))+((l_upper_2)/(G*t_skin))+(((h_upper_middle-h_lower_middle)*c)/(G*t_middle))+((l_lower_2)/(G*t_skin)))), 1]])
            righthand_matrix = np.array([1, 0, 0])

            #solve system of equations
            solution = np.linalg.solve(lefthand_matrix, righthand_matrix)
            twist_rate = solution[2]

            J_y = 1/(G*twist_rate)


    #calculating J for SINGLE CELL -> TWO SPARS
    else:
            #calculate c as a function of y
            c = c_r-((c_r-c_t)/(b/2))*y

            #calculate distance to upper and lower surface for 2 spars
            h_upper_front, h_lower_front = find_sparheight(location_front)
            h_upper_rear, h_lower_rear = find_sparheight(location_rear)

            #calculate lengths of upper and lower wingbox components
            l_upper = np.sqrt(((location_rear-location_front)*c)**2+((h_upper_rear-h_upper_front)*c)**2)
            l_lower = np.sqrt(((location_rear-location_front)*c)**2+((h_lower_rear-h_lower_front))**2)

            #calculate enclosed area, integral and torsional stiffness
            A = ((location_rear-location_front)*c*c*((h_upper_front-h_lower_front)+(h_upper_rear-h_lower_rear)))/2
            int = (l_upper/t_skin)+(l_lower/t_skin)+((h_upper_front-h_lower_front)*c/t_front)+((h_upper_rear-h_lower_rear)*c/t_rear)
            J_y = (4*A*A)/int

    return J_y






# #torsional constant function for a single-cell wingbox. ALL VALUES IN SI UNITS
# #function is done
# def torsional_constant_singlecell(y):
#     #calculate c as a function of y
#     c = c_r-((c_r-c_t)/(b/2))*y

#     #calculate distance to upper and lower surface for 2 spars
#     h_upper_front, h_lower_front = find_sparheight(location_front)
#     h_upper_rear, h_lower_rear = find_sparheight(location_rear)

#     #calculate lengths of upper and lower wingbox components
#     l_upper = np.sqrt(((location_rear-location_front)*c)**2+((h_upper_rear-h_upper_front)*c)**2)
#     l_lower = np.sqrt(((location_rear-location_front)*c)**2+((h_lower_rear-h_lower_front))**2)

#     #calculate enclosed area, integral and torsional stiffness
#     A = ((location_rear-location_front)*c*c*((h_upper_front-h_lower_front)+(h_upper_rear-h_lower_rear)))/2
#     int = (l_upper/t_skin)+(l_lower/t_skin)+((h_upper_front-h_lower_front)*c/t_front)+((h_upper_rear-h_lower_rear)*c/t_rear)
#     J_y = (4*A*A)/int

#     return J_y


# #torsional constant function for a double-cell wingbox
# #assume both closed sections are trapezoidal
# #function is done

# def torsional_constant_multicell(y):
#     #calculate c as a function of y
#     c = c_r-((c_r-c_t)/(b/2))*y

#     #calculate distance to upper and lower surface for 3 spars
#     h_upper_front, h_lower_front = find_sparheight(location_front)
#     h_upper_middle, h_lower_middle = find_sparheight(location_middle)
#     h_upper_rear, h_lower_rear = find_sparheight(location_rear)

#     #calculate lenghts of upper and lower wingbox components
#     l_upper_1 = np.sqrt(((location_middle-location_front)*c)**2+((h_upper_middle-h_upper_front)*c)**2)
#     l_lower_1 = np.sqrt(((location_middle-location_front)*c)**2+((h_lower_middle-h_lower_front))**2)
#     l_upper_2 = np.sqrt(((location_rear-location_middle)*c)**2+((h_upper_rear-h_upper_middle)*c)**2)
#     l_lower_2 = np.sqrt(((location_rear-location_middle)*c)**2+((h_lower_rear-h_lower_middle))**2)

#     #calculate enclosed areas 
#     A_1 = ((location_middle-location_front)*c*c*((h_upper_front-h_lower_front)+(h_upper_middle-h_lower_middle)))/2
#     A_2 = ((location_rear-location_middle)*c*c*((h_upper_middle-h_lower_middle)+(h_upper_rear-h_lower_rear)))/2

#     #set up system of equations with variables: q_1, q_2, twist_rate.
#     lefthand_matrix = np.array([[2*A_1, 2*A_2, 0.], [(-1/(2*A_1))*((((h_upper_middle-h_lower_middle)*c)/(G*t_middle))+((l_upper_1)/(G*t_skin))+(((h_upper_front-h_lower_front)*c)/(G*t_front))+((l_lower_1)/(G*t_skin))), (((h_upper_middle-h_lower_middle)*c)/(2*A_1*G*t_middle)), 1], [(((h_upper_middle-h_lower_middle)*c)/(2*A_2*G*t_middle)), ((-1/(2*A_2))*((((h_upper_rear-h_lower_rear)*c)/(G*t_rear))+((l_upper_2)/(G*t_skin))+(((h_upper_middle-h_lower_middle)*c)/(G*t_middle))+((l_lower_2)/(G*t_skin)))), 1]])
#     righthand_matrix = np.array([1, 0, 0])

#     #solve system of equations
#     solution = np.linalg.solve(lefthand_matrix, righthand_matrix)
#     twist_rate = solution[2]

#     J_y = 1/(G*twist_rate)

#     return J_y

# print(torsional_constant_multicell(b/2))


#test
# print(torsional_constant_singlecell(0.001, 0.001, 0.2, 0.7, 0.003, 2))