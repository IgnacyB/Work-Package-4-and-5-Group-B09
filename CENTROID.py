import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from torsional_stiffness_functions import find_sparheight as find_sparheight_func
import airfoil_geometry as ag



def generate_stringer_coordinates(spars, total_stringers):
    """
    INTERNAL FUNCTION: Calculates coordinates based on spar geometry objects.
    (Users generally won't call this directly; they use the wrapper functions below).
    """
    num_spars = len(spars)
    stringer_coords = []

    # 1. Identify Corner Stringers
    for spar in spars:
        stringer_coords.append(spar[0])  # Top
        stringer_coords.append(spar[1])  # Bottom

    min_stringers = len(stringer_coords)
    remaining_stringers = total_stringers - min_stringers

    if remaining_stringers <= 0:
        return stringer_coords

    # 2. Distribute Extra Stringers
    num_cells = num_spars - 1
    if num_cells <= 0:
        return stringer_coords

    count_top_extra = remaining_stringers // 2 + (remaining_stringers % 2)
    count_bot_extra = remaining_stringers // 2

    def get_intermediate_points(start, end, count):
        pts = []
        if count == 0: return pts
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        for i in range(1, count + 1):
            fraction = i / (count + 1)
            pts.append([start[0] + dx * fraction, start[1] + dy * fraction])
        return pts

    for i in range(num_cells):
        curr_spar = spars[i]
        next_spar = spars[i + 1]

        cell_top_count = count_top_extra // num_cells + (1 if i < count_top_extra % num_cells else 0)
        cell_bot_count = count_bot_extra // num_cells + (1 if i < count_bot_extra % num_cells else 0)

        stringer_coords.extend(get_intermediate_points(curr_spar[0], next_spar[0], cell_top_count))
        stringer_coords.extend(get_intermediate_points(curr_spar[1], next_spar[1], cell_bot_count))

    return stringer_coords


def calculate_wingbox_centroid(spars, stringer_coordinates, t_spars, t_top_list, t_bot_list, A_str):
    """
    New Inputs:
      t_spars:    LIST of spar thicknesses. Size = Number of Spars.
                  Ex: [0.005, 0.005, 0.005]
      t_top_list: LIST of top skin thicknesses. Size = Number of Spars - 1.
                  Ex: [0.002, 0.002]
      t_bot_list: LIST of bottom skin thicknesses. Size = Number of Spars - 1.
    """
    elements = []

    def add_line_segment(p1, p2, thickness, type_name):
        length = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        area = length * thickness
        elements.append({
            'area': area, 'x': mid_x, 'y': mid_y,
            'type': type_name, 'p1': p1, 'p2': p2
        })
        return length

    # --- PROCESS SPARS (Use t_spars list) ---
    for i, spar in enumerate(spars):
        # Safety check to avoid crashing if list is too short
        t_val = t_spars[i] if i < len(t_spars) else t_spars[-1]
        add_line_segment(spar[0], spar[1], t_val, f'Spar {i + 1} Web')

    # --- PROCESS SKINS (Use t_top_list and t_bot_list) ---
    if len(spars) > 1:
        # Loop through each "cell" (gap between spars)
        for i in range(len(spars) - 1):
            # 1. Determine Top Skin Thickness for this cell
            t_top_val = t_top_list[i] if i < len(t_top_list) else t_top_list[-1]

            # 2. Determine Bottom Skin Thickness for this cell
            t_bot_val = t_bot_list[i] if i < len(t_bot_list) else t_bot_list[-1]

            # Add the segments
            add_line_segment(spars[i][0], spars[i + 1][0], t_top_val, f'Top Skin Cell {i + 1}')
            add_line_segment(spars[i][1], spars[i + 1][1], t_bot_val, f'Bottom Skin Cell {i + 1}')

    # --- PROCESS STRINGERS (Unchanged) ---
    for coord in stringer_coordinates:
        elements.append({
            'area': A_str, 'x': coord[0], 'y': coord[1], 'type': 'stringer'
        })

    # Summation
    sum_Area = sum(el['area'] for el in elements)
    sum_Mx = sum(el['area'] * el['x'] for el in elements)
    sum_My = sum(el['area'] * el['y'] for el in elements)

    if sum_Area == 0: return 0, 0, elements

    x_bar = sum_Mx / sum_Area
    y_bar = sum_My / sum_Area

    return x_bar, y_bar, elements

def build_spars_from_positions(c, spar_positions_ratios):
    """
    Helper function: Converts [0.2, 0.6] -> Actual Coordinate List
    """
    spars = []
    for ratio in spar_positions_ratios:
        x_pos = ratio * c
        y_top, y_bot = find_sparheight_func(ratio)
        y_bot = y_bot*c
        y_top = y_top*c
        spars.append([[x_pos, y_top], [x_pos, y_bot]])
    return spars

# =========================================================
#  PUBLIC FUNCTIONS (This is what your team will call)
# =========================================================

def get_stringer_coordinates_only(c, spar_positions_ratios, total_stringers):
    """
    Goal: "People will want the coordinate of the stringers"
    Input: Chord (c), Spar Ratios (e.g. [0.2, 0.6]), Total Stringers
    Output: List of [x, y] coordinates
    """
    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)

    # 2. Generate Stringers
    stringer_coords = generate_stringer_coordinates(spars, total_stringers)

    return stringer_coords


def get_centroid(c, spar_positions_ratios, t_spars, t_skin, stringer_area, total_stringers):
    """
    Simplified wrapper: Accepts different spar thicknesses (list)
    but a constant skin thickness (float).
    """
    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)
    num_cells = len(spars) - 1

    # --- INTERNAL CONVERSION ---
    t_top_list = [t_skin] * num_cells
    t_bot_list = [t_skin] * num_cells

    # 2. Generate Stringers
    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    # 3. Calculate
    cx, cy, final_elements = calculate_wingbox_centroid(
        spars,
        auto_stringers,
        t_spars,      # List
        t_top_list,   # Converted List
        t_bot_list,   # Converted List
        stringer_area
    )

    return cx, cy


def run_analysis(c, spar_positions_ratios, t_spars, t_skin, stringer_area, total_stringers, show_plot=True):
    """
    Inputs:
      t_spars: LIST of thicknesses for spars. Ex: [0.005, 0.010]
      t_skin:  SINGLE number for all skin (top & bot). Ex: 0.002
    """

    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)
    num_spars = len(spars)
    num_cells = num_spars - 1

    # --- INTERNAL CONVERSION ---
    # We turn the single 't_skin' into lists because the calculator expects lists
    t_top_list = [t_skin] * num_cells  # e.g., [0.002, 0.002]
    t_bot_list = [t_skin] * num_cells  # e.g., [0.002, 0.002]

    # Check Spars
    if len(t_spars) != num_spars:
        print(f"WARNING: You have {num_spars} spars but provided {len(t_spars)} thicknesses!")

    # 2. Generate Stringers
    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    # 3. Calculate Centroid
    # (We pass the lists we just created: t_top_list, t_bot_list)
    cx, cy, final_elements = calculate_wingbox_centroid(
        spars, auto_stringers, t_spars, t_top_list, t_bot_list, stringer_area
    )

    print(f"\n--- ANALYSIS COMPLETE ---")
    print(f"Centroid: ({cx:.4f}, {cy:.4f})")

    if show_plot:
        plot_wingbox(final_elements, cx, cy, c, len(spars))

    return cx, cy

def plot_wingbox(elements, cx, cy, c, num_spars):
    """Helper function to visualize the wingbox geometry."""
    plt.figure(figsize=(10, 6))

    for el in elements:
        if 'p1' in el:
            p1, p2 = el['p1'], el['p2']
            color = 'black' if 'Spar' in el['type'] else 'blue'
            lw = 2 if 'Spar' in el['type'] else 1.5
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=lw)

    str_x = [el['x'] for el in elements if el['type'] == 'stringer']
    str_y = [el['y'] for el in elements if el['type'] == 'stringer']
    plt.scatter(str_x, str_y, c='green', s=40, zorder=5, label='Stringers')
    plt.scatter(cx, cy, c='red', marker='x', s=100, zorder=10, label='Centroid')

    plt.title(f"Wing Box Cross-Section (c={c}, Spars={num_spars})")
    plt.xlabel("Chordwise Position (x)")
    plt.ylabel("Height (y)")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()
    #jj



C_TEST = 8.0

# Example: 2 Spars
# Front Spar = 5mm (0.005)
# Rear Spar = 10mm (0.010)
# All Skin = 2mm (0.002)

cx, cy = run_analysis(
    C_TEST,
    [0.2, 0.6],         # Spar locations
    [0.005, 0.010],     # t_spars (List)
    0.002,              # t_skin (Single Number)
    0.002,              # Stringer Area
    10                  # Total Stringers
)
# Test Scenario
C_TEST = 8.0

print("Running 3-Spar Test ...")
run_analysis(C_TEST, [ag.location_front,ag.location_middle,ag.location_rear], ag.t_front, ag.a_stringer, ag.n_stringer, show_plot=True)

