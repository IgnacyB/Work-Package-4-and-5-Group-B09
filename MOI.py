# Moment of inertia calculations
import numpy as np
import scipy as sp
from Aircraft_parameters import b
import matplotlib.pyplot as plt

def MOI_single_cell(y):
    #import the necessary functions from other
    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_middle as thickness_middle
    from airfoil_geometry import t_front as thickness_front
    from airfoil_geometry import t_rear as thickness_rear
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

    t_spars = []
    t_spars.append(thickness_front)
    t_spars.append(thickness_middle)
    t_spars.append(thickness_rear)

    x_centroid, y_centroid = get_centroid(chord,spars, thickness_front, thickness_middle, thickness_rear, skin_thickness ,mass_stringer,n_stringer)
    #print("X_centroid ",x_centroid)
    #print("Y_centroid",y_centroid)

    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    #print(stringer_chord)

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness_front*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness_front
    MOI_rear_spar = thickness_rear*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness_rear

    # code to calculate MOI for top and bottom sections of wingbox
    
    alpha_top = np.arctan2((y_top_rear_spar-y_top_front_spar),(chord_position_rear*chord-chord_position_front*chord))
    alpha_bottom = np.arctan2((y_bottom_rear_spar-y_bottom_front_spar),(chord_position_rear*chord-chord_position_front*chord))

    distance_top = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_top)
    distance_bottom = chord*(chord_position_rear-chord_position_front)/np.cos(alpha_bottom)

    y_centroid_top = y_top_front_spar + (y_top_rear_spar-y_top_front_spar)/2
    y_centroid_bottom = y_bottom_front_spar + (y_bottom_rear_spar-y_bottom_front_spar)/2

    MOI_top = skin_thickness*distance_top/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_top),2) +np.power(distance_top,2) * np.power(np.sin(alpha_top),2) ) + skin_thickness*distance_top*np.power((y_centroid_top-y_centroid),2)
    MOI_bottom = skin_thickness*distance_bottom/12 * (np.power(skin_thickness,2)*np.power(np.cos(alpha_bottom),2) + np.power(distance_bottom,2) * np.power(np.sin(alpha_bottom),2)) + skin_thickness*distance_bottom*np.power((y_centroid_bottom-y_centroid),2)
    
    MOI_stringer =0
    for element in stringer_chord:
        MOI_stringer += np.power(abs(element[1]-y_centroid),2)*mass_stringer

    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_stringer + MOI_top + MOI_bottom
   
    
    return MOI_total

def check_even(n):
    if n % 2 ==0:
        even = True
    else:
        even = False

    return even


def MOI_multi_cell(y):
    #import the necessary functions from other
    from airfoil_geometry import t_skin as skin_thickness
    from airfoil_geometry import t_middle as thickness_middle
    from airfoil_geometry import t_front as thickness_front
    from airfoil_geometry import t_rear as thickness_rear
    from airfoil_geometry import a_stringer as mass_stringer
    from airfoil_geometry import n_stringer
    from airfoil_geometry import location_front as chord_position_front
    from airfoil_geometry import location_rear as chord_position_rear
    from airfoil_geometry import location_middle as chord_position_middle

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
    y_top_middle_spar_percentage, y_bottom_middle_spar_percentage = find_sparheight(chord_position_middle)

    y_top_front_spar= y_top_front_spar_percentage*chord
    y_top_rear_spar= y_top_rear_spar_percentage*chord
    y_bottom_front_spar= y_bottom_front_spar_percentage*chord
    y_bottom_rear_spar= y_bottom_rear_spar_percentage*chord
    y_top_middle_spar = y_top_middle_spar_percentage*chord
    y_bottom_middle_spar = y_bottom_middle_spar_percentage*chord

    spars = []
    spars.append(chord_position_front)
    spars.append(chord_position_middle)
    spars.append(chord_position_rear)

    t_spars = []
    t_spars.append(thickness_front)
    t_spars.append(thickness_middle)
    t_spars.append(thickness_rear)

    x_centroid, y_centroid = get_centroid(chord,spars, thickness_front, thickness_middle, thickness_rear, skin_thickness ,mass_stringer,n_stringer)
    #print("X_centroid ",x_centroid)
    #print("Y_centroid",y_centroid)

    stringer_chord = get_stringer_coordinates_only(chord,spars,n_stringer)

    #print(stringer_chord)

    # code to calculate MOI for front and rear spar

    y_centroid_front_spar = (y_top_front_spar - y_bottom_front_spar)/2
    y_centroid_rear_spar = (y_top_rear_spar-y_bottom_rear_spar)/2

    MOI_front_spar = thickness_front*np.power((y_top_front_spar-y_bottom_front_spar),3)/12 + np.power(abs(y_centroid_front_spar -y_centroid),2)*(y_top_front_spar - y_bottom_front_spar)*thickness_front
    MOI_rear_spar = thickness_rear*np.power((y_top_rear_spar-y_bottom_rear_spar),3)/12 + np.power(abs(y_centroid_rear_spar -y_centroid),2)*(y_top_rear_spar - y_bottom_rear_spar)*thickness_rear

    #middle spars
    y_centroid_middle_spar = (y_top_middle_spar - y_bottom_middle_spar)/2
    MOI_middle_spar = thickness_middle*np.power((y_top_middle_spar-y_bottom_middle_spar),3)/12 + np.power(abs(y_centroid_middle_spar -y_centroid),2)*(y_top_middle_spar - y_bottom_middle_spar)*thickness_middle

    # code to calculate MOI for top and bottom sections of wingbox
    
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

    # sum all the elements together 
    #MOI_total_2 = MOI_front_spar + MOI_rear_spar + MOI_stringer_2 + MOI_top + MOI_bottom + MOI_middle_spar

    MOI_total = MOI_front_spar + MOI_rear_spar + MOI_middle_spar + MOI_stringer + MOI_top + MOI_bottom
   
    
    return MOI_total


def plot_MOI_single_cell(y=None, n=200, figsize=(10,4), dpi=100):
    """Plot MOI_single_cell from 0 to b/2.
    Evaluates MOI_single_cell on n points (or on provided y array) and shows a simple plot.
    """
    if y is None:
        y = np.linspace(0, b/2, n)
    else:
        y = np.asarray(y)

    # evaluate (use Python loop because MOI_single_cell does internal imports and is not vectorized)
    vals = []
    for yy in y:
        try:
            vals.append(MOI_single_cell(float(yy)))
        except Exception as e:
            vals.append(np.nan)

    vals = np.asarray(vals, dtype=float)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(y, vals, lw=2, color="#1f77b4")
    ax.fill_between(y, vals, alpha=0.12, color="#1f77b4")
    ax.set_xlabel("Spanwise coordinate y (m)")
    ax.set_ylabel("MOI_single_cell [m^4]")
    ax.set_title("MOI_single_cell along half-span (0 to b/2)")
    ax.grid(True, linestyle="--", alpha=0.6)

    # mark and annotate max value (ignoring NaNs)
    if np.any(~np.isnan(vals)):
        idx = np.nanargmax(vals)
        ax.plot(y[idx], vals[idx], "o", color="#d62728")
        ax.annotate(f"{vals[idx]:.3e}", xy=(y[idx], vals[idx]),
                    xytext=(8, 8), textcoords="offset points", fontsize=9,
                    arrowprops=dict(arrowstyle="->", lw=0.8))

    plt.tight_layout()
    plt.show()


def plot_MOI_multi_cell(y=None, n=200, figsize=(10,4), dpi=100):
    """Plot MOI_multi_cell from 0 to b/2."""
    if y is None:
        y = np.linspace(0, b/2, n)
    else:
        y = np.asarray(y)

    vals = []
    for yy in y:
        try:
            vals.append(MOI_multi_cell(float(yy)))
        except Exception:
            vals.append(np.nan)

    vals = np.asarray(vals, dtype=float)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(y, vals, lw=2, color="#2ca02c", label="MOI_multi_cell")
    ax.fill_between(y, vals, alpha=0.12, color="#2ca02c")
    ax.set_xlabel("Spanwise coordinate y (m)")
    ax.set_ylabel("MOI_multi_cell [m^4]")
    ax.set_title("MOI_multi_cell along half-span (0 to b/2)")
    ax.grid(True, linestyle="--", alpha=0.6)

    if np.any(~np.isnan(vals)):
        idx = np.nanargmax(vals)
        ax.plot(y[idx], vals[idx], "o", color="#d62728")
        ax.annotate(f"{vals[idx]:.3e}", xy=(y[idx], vals[idx]),
                    xytext=(8, 8), textcoords="offset points", fontsize=9,
                    arrowprops=dict(arrowstyle="->", lw=0.8))

    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_MOI_single_cell()
    plot_MOI_multi_cell()

value_1 = MOI_single_cell(b/2)
value_2 = MOI_multi_cell(b/2)
print(value_1)
print(value_2)