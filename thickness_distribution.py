from airfoil_geometry import t_front, t_middle, t_rear, t_front_2, t_middle_2, t_rear_2, end_third_spar
from Aircraft_parameters import b

def t_front(y):
    t = t_front - (t_front-t_front_2)*y*2/b
    return t

def t_middle(y):
    t = t_middle - (t_middle-t_middle_2)*y*2/(end_third_spar*b)
    return t

def t_rear(y):
    t = t_rear - (t_rear-t_rear_2)*y*2/b
    return t