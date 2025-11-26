import math
import numpy as np
import json
import sys  # <-- Added sys for program termination on fatal error

# Note: Matplotlib is removed as plotting is disabled, simplifying dependencies.

# --- START OF SIMPLIFIED IMPORT BLOCK (Updated for Exit on Failure) ---
# We now assume the external function find_sparheight(x_pos) exists in torsion_stiffness_functions.py
try:
    # Attempt to import the specific function directly
    from torsional_stiffness_functions import find_sparheight as find_sparheight_func

    print("find_sparheight successfully imported from torsion_stiffness_functions.")
except ImportError as e:
    # Action: Print error and exit the program as requested by the user.
    print("-" * 50)
    print(f"FATAL ERROR: Required function 'find_sparheight' could not be imported.")
    print(f"Details: {e}")
    print("The external file 'torsion_stiffness_functions.py' must be present to define wing box geometry.")
    print("Program terminating.")
    print("-" * 50)
    sys.exit(1)


# --- END OF SIMPLIFIED IMPORT BLOCK ---


def generate_stringer_coordinates(spars, total_stringers):
    """
    Calculates the coordinates of stringers based on specific rules for the wing box.

    Rules:
    1. Minimum stringers: All spar corners.
    2. Extra stringers are distributed evenly on the roof and bottom skins of the outer cells.

    Args:
        spars (list): List of spars, each [[x_top, y_top], [x_bot, y_bot]].
        total_stringers (int): The total number of stringers desired.

    Returns:
        list: A list of [x, y] coordinates for all stringers.
    """

    num_spars = len(spars)
    stringer_coords = []

    # --- 1. Identify Corner Stringers (Minimum Required) ---
    for spar in spars:
        stringer_coords.append(spar[0])  # Top
        stringer_coords.append(spar[1])  # Bottom

    min_stringers = len(stringer_coords)

    # --- 2. Handle Extra Stringers ---
    remaining_stringers = total_stringers - min_stringers

    if remaining_stringers <= 0:
        return stringer_coords

    # --- 3. Distribute Extra Stringers on Skins ---
    num_cells = num_spars - 1
    if num_cells <= 0:
        return stringer_coords

    count_top_extra = remaining_stringers // 2 + (remaining_stringers % 2)
    count_bot_extra = remaining_stringers // 2

    # --- Interpolation Function ---
    def get_intermediate_points(start, end, count):
        pts = []
        if count == 0: return pts

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Distribute 'count' points evenly into 'count + 1' segments
        for i in range(1, count + 1):
            fraction = i / (count + 1)
            nx = start[0] + dx * fraction
            ny = start[1] + dy * fraction
            pts.append([nx, ny])
        return pts

    # --- Distribute Across Cells ---
    for i in range(num_cells):
        curr_spar = spars[i]
        next_spar = spars[i + 1]

        cell_top_count = count_top_extra // num_cells + (1 if i < count_top_extra % num_cells else 0)
        cell_bot_count = count_bot_extra // num_cells + (1 if i < count_bot_extra % num_cells else 0)

        top_points = get_intermediate_points(curr_spar[0], next_spar[0], cell_top_count)
        stringer_coords.extend(top_points)

        bot_points = get_intermediate_points(curr_spar[1], next_spar[1], cell_bot_count)
        stringer_coords.extend(bot_points)

    return stringer_coords


def calculate_wingbox_centroid(spars, stringer_coordinates, t, A_str):
    """
    Calculates the centroid of a wing box with variable number of spars and stringers.

    Returns:
        tuple: (x_bar, y_bar, elements_list)
    """
    elements = []

    # Helper to add a line segment (for skins and spar webs)
    def add_line_segment(p1, p2, thickness, type_name):
        length = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        area = length * thickness

        elements.append({
            'area': area,
            'x': mid_x,
            'y': mid_y,
            'type': type_name,
            'p1': p1,
            'p2': p2
        })
        return length

    # --- 2. PROCESS SPARS (WEBS) ---
    for i, spar in enumerate(spars):
        p_top, p_bot = spar[0], spar[1]
        add_line_segment(p_top, p_bot, t, f'Spar {i + 1} Web')

    # --- 3. PROCESS SKINS ---
    if len(spars) > 1:
        for i in range(len(spars) - 1):
            curr_spar = spars[i]
            next_spar = spars[i + 1]
            add_line_segment(curr_spar[0], next_spar[0], t, 'Top Skin')
            add_line_segment(curr_spar[1], next_spar[1], t, 'Bottom Skin')

    # --- 4. PROCESS STRINGERS ---
    for coord in stringer_coordinates:
        elements.append({
            'area': A_str,
            'x': coord[0],
            'y': coord[1],
            'type': 'stringer'
        })

    # --- 5. SUMMATION ---
    sum_Area = 0.0
    sum_Mx = 0.0
    sum_My = 0.0

    for el in elements:
        sum_Area += el['area']
        sum_Mx += el['area'] * el['x']
        sum_My += el['area'] * el['y']

    if sum_Area == 0:
        return 0, 0, elements

    x_bar = sum_Mx / sum_Area
    y_bar = sum_My / sum_Area

    return x_bar, y_bar, elements


def run_analysis_and_export(c, num_spars, thickness, stringer_area, total_stringers_desired,
                            file_path="centroid_data.json"):
    """
    Runs the full centroid analysis pipeline, prints results, and saves them to a JSON file.

    Args:
        c (float): The local chord length.
        num_spars (int): The number of spars (2 or 3).
        thickness (float): Constant thickness of skins and spars (t).
        stringer_area (float): Constant area of stringers (A_str).
        total_stringers_desired (int): Total number of stringers.
        file_path (str): File path to save the results.

    Returns:
        dict: The results data (Centroid X, Centroid Y, and Stringer Coords).
    """

    # 1. Determine Spar X-Positions based on c and num_spars
    if num_spars == 3:
        spar_chord_positions = [0.2 * c, 0.4 * c, 0.6 * c]
    elif num_spars == 2:
        spar_chord_positions = [0.2 * c, 0.6 * c]
    else:
        raise ValueError("Unsupported number of spars. Only 2 or 3 supported for automatic positioning.")

    # 2. Generate Full Spar Coordinates using Geometry Function
    spars = []
    for x_pos in spar_chord_positions:
        # Assumes find_sparheight_func returns [y_top, y_bottom]
        y_top, y_bot = find_sparheight_func(x_pos)

        # Spar is defined as [[x_top, y_top], [x_bot, y_bot]]
        spar_coords = [[x_pos, y_top], [x_pos, y_bot]]
        spars.append(spar_coords)

    # 3. Generate Stringer Coordinates
    auto_stringers = generate_stringer_coordinates(spars, total_stringers_desired)

    # 4. Calculate Centroid
    cx, cy, final_elements = calculate_wingbox_centroid(
        spars,
        auto_stringers,
        thickness,
        stringer_area
    )

    # 5. Compile and Save Results
    results_data = {
        "chord_length_c": c,
        "num_spars": num_spars,
        "centroid_x": cx,
        "centroid_y": cy,
        "stringer_area": stringer_area,
        "stringer_coordinates": [np.around(c, 4).tolist() for c in auto_stringers]
    }

    with open(file_path, 'w') as f:
        json.dump(results_data, f, indent=4)

    print(f"--- RESULTS SAVED TO: {file_path} ---")
    print("\n--- CENTROID SUMMARY ---")
    print(f"Chord Length (c): {c:.2f}")
    print(f"Number of Spars: {num_spars}")
    print(f"Actual Stringers: {len(auto_stringers)}")
    print(f"Centroid X: {cx:.4f}")
    print(f"Centroid Y: {cy:.4f}")

    return results_data


# ==========================================
# STANDALONE EXECUTION (Runs when the script is executed directly)
# ==========================================
if __name__ == '__main__':
    # --- ANALYSIS SCENARIO 1: Three Spars ---
    C_TEST = 8.0  # Example chord length in meters
    NUM_SPARS_TEST = 3

    print("--- Running Analysis for 3-Spar Configuration ---")
    results_3_spar = run_analysis_and_export(
        c=C_TEST,
        num_spars=NUM_SPARS_TEST,
        thickness=0.005,
        stringer_area=0.002,
        total_stringers_desired=16,
        file_path="centroid_data_3spar.json"
    )

    print("\n--- GENERATED STRINGER COORDINATES (3 Spars) ---")
    print(results_3_spar["stringer_coordinates"])

    # --- ANALYSIS SCENARIO 2: Two Spars ---
    print("\n--- Running Analysis for 2-Spar Configuration ---")
    results_2_spar = run_analysis_and_export(
        c=C_TEST,
        num_spars=2,
        thickness=0.005,
        stringer_area=0.002,
        total_stringers_desired=10,
        file_path="centroid_data_2spar.json"
    )

    print("\n--- GENERATED STRINGER COORDINATES (2 Spars) ---")
    print(results_2_spar["stringer_coordinates"])
