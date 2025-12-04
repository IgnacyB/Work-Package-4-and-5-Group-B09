import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from torsional_stiffness_functions import find_sparheight as find_sparheight_func
import airfoil_geometry as ag



def generate_stringer_coordinates(spars, total_stringers):

    num_spars = len(spars)
    stringer_coords = []

    if not total_stringers ==0:
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


def calculate_wingbox_centroid(spars, stringer_coordinates, t_front, t_mid, t_rear, t_skin, A_str):

    elements = []

    # --- LOGIC TO HANDLE 2 VS 3 SPARS ---
    num_spars = len(spars)

    # We build the list dynamically based on how many spars exist
    if num_spars == 2:
        # If only 2 spars, we ignore t_mid
        active_spar_thicknesses = [t_front, t_rear]
    elif num_spars == 3:
        # If 3 spars, we use all three
        active_spar_thicknesses = [t_front, t_mid, t_rear]
    else:
        # Fallback for unexpected cases (assumes all are front thickness)
        active_spar_thicknesses = [t_front] * num_spars

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

    # 1. Process Spars (Using our new active_spar_thicknesses list)
    for i, spar in enumerate(spars):
        t_val = active_spar_thicknesses[i]
        add_line_segment(spar[0], spar[1], t_val, f'Spar {i + 1} Web')

    # 2. Process Skins (Using the SINGLE t_skin value)
    if len(spars) > 1:
        for i in range(len(spars) - 1):
            add_line_segment(spars[i][0], spars[i + 1][0], t_skin, 'Top Skin')
            add_line_segment(spars[i][1], spars[i + 1][1], t_skin, 'Bottom Skin')

    # 3. Process Stringers
    for coord in stringer_coordinates:
        elements.append({
            'area': A_str, 'x': coord[0], 'y': coord[1], 'type': 'stringer'
        })

    # Summation
    sum_Area = sum(el['area'] for el in elements)
    sum_Mx = sum(el['area'] * el['x'] for el in elements)
    sum_My = sum(el['area'] * el['y'] for el in elements)

    if sum_Area == 0:
        return 0, 0, elements

    x_bar = sum_Mx / sum_Area
    y_bar = sum_My / sum_Area

    return x_bar, y_bar, elements


def build_spars_from_positions(c, spar_positions_ratios):
    """
    UPDATED: Filters out None or 0 values so they don't become accidental spars.
    """
    spars = []

    # FILTER STEP: Only keep ratios that are not None and greater than 0
    valid_ratios = [r for r in spar_positions_ratios if r is not None and r > 0]

    # Sort them just in case (e.g. if you pass [0.7, 0.2], it fixes it to [0.2, 0.7])
    valid_ratios.sort()

    for ratio in valid_ratios:
        x_pos = ratio * c
        y_top, y_bot = find_sparheight_func(ratio)
        y_bot = y_bot * c
        y_top = y_top * c
        spars.append([[x_pos, y_top], [x_pos, y_bot]])

    return spars
# =========================================================
#  PUBLIC FUNCTIONS
# =========================================================

def get_stringer_coordinates_only(c, spar_positions_ratios, total_stringers):
    """
    Input: Chord (c), Spar Ratios (e.g. [0.2, 0.6]), Total Stringers
    Output: List of [x, y] coordinates
    """
    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)

    # 2. Generate Stringers
    stringer_coords = generate_stringer_coordinates(spars, total_stringers)

    return stringer_coords


def get_centroid(c, spar_positions_ratios, t_front, t_mid, t_rear, t_skin, stringer_area, total_stringers):


    spars = build_spars_from_positions(c, spar_positions_ratios)

    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    cx, cy, final_elements = calculate_wingbox_centroid(
        spars,
        auto_stringers,
        t_front,
        t_mid,
        t_rear,
        t_skin,
        stringer_area
    )

    return cx, cy


def run_analysis(c, spar_positions_ratios, t_front, t_mid, t_rear, t_skin, stringer_area, total_stringers, show_plot=True):
    # 1. Build Spars
    # (Relies on build_spars_from_positions filtering out 'None' values correctly)
    spars = build_spars_from_positions(c, spar_positions_ratios)

    # 2. Generate Stringers
    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    # 3. Calculate Centroid
    cx, cy, final_elements = calculate_wingbox_centroid(
        spars,
        auto_stringers,
        t_front,
        t_mid,
        t_rear,
        t_skin,
        stringer_area
    )

    print(f"\n--- ANALYSIS COMPLETE ---")
    print(f"Chord: {c}")
    print(f"Active Spars: {len(spars)}")
    print(f"Centroid: ({cx:.4f}, {cy:.4f})")

    if show_plot:
        # UPDATED: We pass 'total_stringers' here so the plot title works
        plot_wingbox(final_elements, cx, cy, c, len(spars), total_stringers)

    return cx, cy

def plot_wingbox(elements, cx, cy, c, num_spars, n_stringers):
    """
    Changes:
    - Added 'n_stringers' to inputs.
    - Updated plt.title to use 'n_stringers'.
    """
    plt.figure(figsize=(12, 6))

    # --- 1. DEFINE AIRFOIL COORDINATES ---
    x_pos_upper = [1.00000, 0.95033, 0.90066, 0.85090, 0.80103, 0.75107, 0.70101, 0.65086, 0.60064, 0.55035, 0.50000,
                   0.44962, 0.39923, 0.34884, 0.29846, 0.24881, 0.19781, 0.14757, 0.09746, 0.07247, 0.04757, 0.02283,
                   0.01059, 0.00580, 0.00347, 0.00000]
    x_pos_lower = [0.00000, 0.00653, 0.00920, 0.01441, 0.02717, 0.05243, 0.07753, 0.10254, 0.15243, 0.20219, 0.25189,
                   0.30154, 0.35116, 0.40077, 0.45038, 0.50000, 0.54965, 0.59936, 0.64914, 0.69899, 0.74893, 0.79897,
                   0.84910, 0.89934, 0.94967, 1.00000]
    y_pos_upper = [0.00000, 0.00986, 0.01979, 0.02974, 0.03935, 0.04847, 0.05686, 0.06440, 0.07085, 0.07602, 0.07963,
                   0.08139, 0.08139, 0.07971, 0.07658, 0.07193, 0.06562, 0.05741, 0.04672, 0.04010, 0.03227, 0.02234,
                   0.01588, 0.01236, 0.01010, 0.00000]
    y_pos_lower = [0.00000, -0.00810, -0.00956, -0.01160, -0.01490, -0.01963, -0.02314, -0.02604, -0.03049, -0.03378,
                   -0.03613, -0.03770, -0.03851, -0.03855, -0.03759, -0.03551, -0.03222, -0.02801, -0.02320, -0.01798,
                   -0.01267, -0.00751, -0.00282, 0.00089, 0.00278, 0.00000]

    # --- 2. SCALE AND PLOT AIRFOIL ---
    plt.plot([x * c for x in x_pos_upper], [y * c for y in y_pos_upper],
             color='gray', linestyle='--', alpha=0.5, label='Airfoil Contour')
    plt.plot([x * c for x in x_pos_lower], [y * c for y in y_pos_lower],
             color='gray', linestyle='--', alpha=0.5)

    # --- 3. PLOT WINGBOX ELEMENTS ---
    for el in elements:
        if 'p1' in el:
            p1, p2 = el['p1'], el['p2']
            color = 'blue' if 'Spar' in el['type'] else 'black'
            lw = 2 if 'Spar' in el['type'] else 1.5
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=lw)

    # --- 4. PLOT STRINGERS AND CENTROID ---
    str_x = [el['x'] for el in elements if el['type'] == 'stringer']
    str_y = [el['y'] for el in elements if el['type'] == 'stringer']

    plt.scatter(str_x, str_y, c='green', s=40, zorder=5, label='Stringers')
    plt.scatter(cx, cy, c='red', marker='x', s=100, zorder=10, label='Centroid')

    # --- 5. FORMATTING ---
    # UPDATED: Use n_stringers passed in the argument
    plt.title(f"Wing Box Cross-Section (chord length={c}m, Spars={num_spars}, Number of Stringers={n_stringers})")
    plt.xlabel("Chordwise Position (x) [m]")
    plt.ylabel("Height (y) [m]")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

if __name__ == "__main__": 
    run_analysis(9,[ag.location_front,ag.location_middle,ag.location_rear],ag.t_front,ag.t_middle,ag.t_rear,ag.t_skin,ag.a_stringer,ag.n_stringer,show_plot=True)

'''cx, cy = run_analysis(
    C_TEST,
    [ag.location_front,ag.location_middle,ag.location_rear],         # Spar locations
    [],     # t_spars (List)
                  # t_skin (Single Number)
    ag.a_stringer,              # Stringer Area
    ag.n_stringer                  # Total Stringers
)
'''