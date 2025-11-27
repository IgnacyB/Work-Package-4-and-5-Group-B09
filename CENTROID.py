import math
import numpy as np
import scipy as sp
import json
import matplotlib.pyplot as plt
#boom


from torsional_stiffness_functions import find_sparheight as find_sparheight_func

# --- END OF IMPORT BLOCK ---


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


def calculate_wingbox_centroid(spars, stringer_coordinates, t, A_str):
    """
    Calculates the centroid based on PRE-CALCULATED geometry.
    This keeps the math separate from the geometry generation.
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

    # Process Spars
    for i, spar in enumerate(spars):
        add_line_segment(spar[0], spar[1], t, f'Spar {i + 1} Web')

    # Process Skins
    if len(spars) > 1:
        for i in range(len(spars) - 1):
            add_line_segment(spars[i][0], spars[i + 1][0], t, 'Top Skin')
            add_line_segment(spars[i][1], spars[i + 1][1], t, 'Bottom Skin')

    # Process Stringers
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
    Helper function: Converts [0.2, 0.6] -> Actual Coordinate List
    """
    spars = []
    for ratio in spar_positions_ratios:
        x_pos = ratio * c
        y_top, y_bot = find_sparheight_func(ratio)
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


def get_centroid(c, spar_positions_ratios, thickness, stringer_area, total_stringers):
    """
    Goal: Return ONLY the centroid coordinates (x, y).
    This runs the full pipeline internally but returns simple values.

    Input:
      c: Chord length
      spar_positions_ratios: List (e.g. [0.2, 0.6])
      thickness: Skin/Spar thickness
      stringer_area: Area of one stringer
      total_stringers: Number of stringers

    Output: Tuple (cx, cy)
    """
    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)

    # 2. Generate Stringers (Required for centroid calculation)
    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    # 3. Calculate Centroid
    cx, cy, _ = calculate_wingbox_centroid(
        spars, auto_stringers, thickness, stringer_area
    )

    return cx, cy


def run_analysis_and_export(c, spar_positions_ratios, thickness, stringer_area, total_stringers,
                            file_path="centroid_data.json", show_plot=True):
    """
    MASTER PIPELINE:
    1. Generates Spars
    2. Generates Stringers
    3. Calculates Centroid
    4. Saves Everything
    """

    # 1. Build Spars
    spars = build_spars_from_positions(c, spar_positions_ratios)

    # 2. Generate Stringers
    auto_stringers = generate_stringer_coordinates(spars, total_stringers)

    # 3. Calculate Centroid
    cx, cy, final_elements = calculate_wingbox_centroid(
        spars, auto_stringers, thickness, stringer_area
    )

    # 4. Save Results
    results_data = {
        "chord_length_c": c,
        "spar_positions": spar_positions_ratios,
        "centroid_x": cx,
        "centroid_y": cy,
        "stringer_area": stringer_area,
        "stringer_coordinates": [np.around(c, 4).tolist() for c in auto_stringers]
    }

    with open(file_path, 'w') as f:
        json.dump(results_data, f, indent=4)

    print(f"\n--- ANALYSIS COMPLETE ---")
    print(f"Chord: {c}, Spars at: {spar_positions_ratios}")
    print(f"Saved to: {file_path}")
    print(f"Centroid: ({cx:.4f}, {cy:.4f})")

    if show_plot:
        plot_wingbox(final_elements, cx, cy, c, len(spars))

    return results_data


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


if __name__ == '__main__':
    # Test Scenario
    C_TEST = 8.0

    print("Running 3-Spar Test [0.2c, 0.4c, 0.6c]...")
    run_analysis_and_export(C_TEST, [0.2, 0.4, 0.6], 0.005, 0.002, 16, "centroid_3spar.json", show_plot=True)

    print("\nRunning 2-Spar Test [0.2c, 0.6c]...")
    # NOTE: Here we explicitly pass the spar locations you mentioned
    run_analysis_and_export(C_TEST, [0.2, 0.6], 0.005, 0.002, 10, "centroid_2spar.json", show_plot=True)

    # EXAMPLE: How your team can get JUST stringer coordinates
    print("\n--- Example: Getting Just Stringer Coords ---")
    coords = get_stringer_coordinates_only(C_TEST, [0.2, 0.6], 10)
    print(f"Received {len(coords)} stringer coordinates.")

    # EXAMPLE: How your team can get JUST centroid coordinates
    print("\n--- Example: Getting Just Centroid ---")
    cx, cy = get_centroid(C_TEST, [0.2, 0.6], 0.005, 0.002, 10)
    print(f"Received Centroid: ({cx:.4f}, {cy:.4f})")