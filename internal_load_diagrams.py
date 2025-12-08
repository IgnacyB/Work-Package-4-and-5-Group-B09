import os
import numpy as np
import matplotlib.pyplot as plt
import math
#Importing important constants and functions
from Aircraft_parameters import b
from load_calculations import V, T, M   

#importing y grid
from grid_setup import y_arr

def _eval_on_grid(f, y):
    try:
        return np.asarray(f(y), dtype=float)  # function expects y
    except TypeError:
        return np.asarray(f(), dtype=float)   # function returns cached array

def _colors_for_cases(n, cmap_name_sequence=("tab20", "Set3", "Accent", "Dark2", "Paired", "hsv", "nipy_spectral")):
    """Return n distinct RGBA colors sampled from a suitable colormap."""
    for name in cmap_name_sequence:
        try:
            cmap = plt.get_cmap(name)
            colors = cmap(np.linspace(0.0, 1.0, max(n, 2)))
            return colors[:n]
        except Exception:
            continue
    # fallback
    cmap = plt.get_cmap("viridis")
    return cmap(np.linspace(0.0, 1.0, max(n, 2)))[:n]

def plot_internal_loads(title=None, case_id=None, save=False, save_dir=None):
    """Plot V, T, M as three separate figures. Optionally save with naming:
       'LC-XX Shear distribution', 'LC-XX Torque distribution', 'LC-XX Bending moment distribution'."""
    V_arr = _eval_on_grid(V, y_arr)
    T_arr = _eval_on_grid(T, y_arr)
    M_arr = _eval_on_grid(M, y_arr)

    # Shear force — separate figure
    figV, axV = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title:
        figV.suptitle(f"{title} — Shear V(y)", fontsize=14)
    axV.plot(y_arr, V_arr, lw=2, color="tab:blue")
    axV.axhline(0, color="k", lw=0.6)
    axV.set_xlabel("Spanwise coordinate y [m]")
    axV.set_ylabel("V(y) [N]")
    axV.set_title("Internal Shear Force along wing span")
    axV.grid(True)

    # Torque — separate figure
    figT, axT = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title:
        figT.suptitle(f"{title} — Torque T(y)", fontsize=14)
    axT.plot(y_arr, T_arr, lw=2, color="tab:green")
    axT.axhline(0, color="k", lw=0.6)
    axT.set_xlabel("Spanwise coordinate y [m]")
    axT.set_ylabel("T(y) [N·m]")
    axT.set_title("Internal Torque along wing span")
    axT.grid(True)

    # Bending moment — separate figure
    figM, axM = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title:
        figM.suptitle(f"{title} — Bending Moment M(y)", fontsize=14)
    axM.plot(y_arr, M_arr, lw=2, color="tab:red")
    axM.axhline(0, color="k", lw=0.6)
    axM.set_xlabel("Spanwise coordinate y [m]")
    axM.set_ylabel("M(y) [N·m]")
    axM.set_title("Internal Bending Moment along wing span")
    axM.grid(True)

    # Optional saving with required naming convention
    if save and case_id:
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            mk = lambda name: os.path.join(save_dir, f"{case_id} {name}.png")
        else:
            mk = lambda name: f"{case_id} {name}.png"

        figV.savefig(mk("Shear distribution"), dpi=150, bbox_inches="tight")
        figT.savefig(mk("Torque distribution"), dpi=150, bbox_inches="tight")
        figM.savefig(mk("Bending moment distribution"), dpi=150, bbox_inches="tight")

    plt.show()

def plot_all_cases_internal_distributions(Load_cases_list, load_calculations, case_indexes=None, split_legend=False):

    if case_indexes is None:
        case_indexes = list(range(len(Load_cases_list)))

    figV, axV = plt.subplots(figsize=(8,4))
    figT, axT = plt.subplots(figsize=(8,4))
    figM, axM = plt.subplots(figsize=(8,4))

    # generate a distinct color per case
    colors = _colors_for_cases(len(case_indexes))

    for i, idx in enumerate(case_indexes):
        case = Load_cases_list[idx]
        v_cruise = case[1]
        mass_aircraft =  case[2]
        load_factor = case[3]
        rho = case[4]
        mass_fuel = case[5]

        load_calculations.set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel)

        V_arr = load_calculations.V()
        T_arr = load_calculations.T()
        M_arr = load_calculations.M()
        label = f"{case[0]} (v={v_cruise:.1f} m/s, n={case[3]:.2f})"
        color = colors[i % len(colors)]
        axV.plot(y_arr, V_arr, lw=1.6, color=color, label=label)
        axT.plot(y_arr, T_arr, lw=1.6, color=color, label=label)
        axM.plot(y_arr, M_arr, lw=1.6, color=color, label=label)
    for fig, ax in ((figV, axV), (figT, axT), (figM, axM)):
        ax.set_xlabel("y [m]")
        ax.grid(True)

    axV.set_title("Internal Shear V(y) — multiple load cases")
    axV.set_ylabel("V(y) [N]")

    axT.set_title("Internal Torque T(y) — multiple load cases")
    axT.set_ylabel("T(y) [N·m]")

    axM.set_title("Bending Moment M(y) — multiple load cases")
    axM.set_ylabel("M(y) [N·m]")

    if split_legend:
        # make room on the right for two stacked legend boxes
        for fig in (figV, figT, figM):
            fig.subplots_adjust(right=0.72)

        for ax in (axV, axT, axM):
            handles, labels = ax.get_legend_handles_labels()
            if not labels:
                continue
            mid = math.ceil(len(labels) / 2)
            leg1 = ax.legend(handles[:mid], labels[:mid],
                             bbox_to_anchor=(1.02, 1.0), loc='upper left', fontsize='small', frameon=True)
            leg2 = ax.legend(handles[mid:], labels[mid:],
                             bbox_to_anchor=(1.02, 0.45), loc='upper left', fontsize='small', frameon=True)
            ax.add_artist(leg1)
    else:
        # single legend with two columns (compact)
        for ax in (axV, axT, axM):
            ax.legend(ncol=2, loc="best", fontsize="small")

    plt.show()

if __name__ == "__main__":
    plot_internal_loads()
