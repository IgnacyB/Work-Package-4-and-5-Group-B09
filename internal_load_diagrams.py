import os
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import math
from Aircraft_parameters import b
from load_calculations import V, T, M
from grid_setup import y_arr

def _eval_on_grid(f, y):
    try:
        return np.asarray(f(y), dtype=float)  # vector path
    except TypeError:
        return np.asarray(f(), dtype=float)   # cached path

def _big_distinct_palette(n, hsv_sat=0.97, hsv_val=0.92, hsv_offset=0.11, mix=0.6):
    """
    Generate n visually distinct RGBA colors by:
    - sampling HSV hues evenly (high saturation/value),
    - mixing with categorical palettes to increase variation.
    """
    if n <= 0:
        return np.empty((0, 4), dtype=float)

    # HSV base
    hues = (np.linspace(0.0, 1.0, n, endpoint=False) + hsv_offset) % 1.0
    hsv_rgbs = np.array([colorsys.hsv_to_rgb(h, hsv_sat, hsv_val) for h in hues], dtype=float)

    # categorical palettes for variety
    cat_names = ["tab20", "Set3", "Accent", "Dark2", "Paired", "tab20b", "tab20c"]
    cat_rgbs = []
    for name in cat_names:
        cmap = plt.get_cmap(name)
        m = max(n, 20)
        cat_rgbs.append(cmap(np.linspace(0, 1, m))[:, :3])
    cat_rgbs = np.vstack(cat_rgbs)
    cat_pick = cat_rgbs[np.linspace(0, len(cat_rgbs) - 1, n).astype(int)]

    # mix HSV and categorical colors
    rgbs = (mix * hsv_rgbs + (1.0 - mix) * cat_pick)
    rgbs = np.clip(rgbs, 0.0, 1.0)
    return np.hstack([rgbs, np.ones((n, 1))])  # add alpha=1

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

def plot_all_cases_internal_distributions(Load_cases_list, load_calculations, case_indexes=None, split_legend=False, save=False, save_dir=None):
    """
    Plot V/T/M for multiple cases with a big distinct palette.
    If save=True, writes three files:
      'shear distribution all relevant cases.png'
      'torque distribution all relevant cases.png'
      'bending distribution all relevant cases.png'
    """
    if case_indexes is None:
        case_indexes = list(range(len(Load_cases_list)))

    figV, axV = plt.subplots(figsize=(9, 4))
    figT, axT = plt.subplots(figsize=(9, 4))
    figM, axM = plt.subplots(figsize=(9, 4))

    colors = _big_distinct_palette(len(case_indexes))

    for i, idx in enumerate(case_indexes):
        case = Load_cases_list[idx]
        v_cruise, mass_aircraft, load_factor, rho, mass_fuel = case[1], case[2], case[3], case[4], case[5]
        load_calculations.set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel)

        V_arr = load_calculations.V()
        T_arr = load_calculations.T()
        M_arr = load_calculations.M()
        label = f"{case[0]} (v={v_cruise:.1f} m/s, n={load_factor:.2f})"
        color = colors[i]

        axV.plot(y_arr, V_arr, lw=1.8, color=color, label=label)
        axT.plot(y_arr, T_arr, lw=1.8, color=color, label=label)
        axM.plot(y_arr, M_arr, lw=1.8, color=color, label=label)

    for ax in (axV, axT, axM):
        ax.set_xlabel("y [m]")
        ax.grid(True, linestyle="--", alpha=0.5)

    axV.set_title("Internal Shear V(y) — multiple load cases")
    axV.set_ylabel("V(y) [N]")
    axT.set_title("Internal Torque T(y) — multiple load cases")
    axT.set_ylabel("T(y) [N·m]")
    axM.set_title("Bending Moment M(y) — multiple load cases")
    axM.set_ylabel("M(y) [N·m]")

    if split_legend:
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
        for ax in (axV, axT, axM):
            ax.legend(ncol=2, loc="best", fontsize="small")

    # saving for “all relevant cases”
    if save:
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            pathV = os.path.join(save_dir, "shear distribution all relevant cases.png")
            pathT = os.path.join(save_dir, "torque distribution all relevant cases.png")
            pathM = os.path.join(save_dir, "bending distribution all relevant cases.png")
        else:
            pathV = "shear distribution all relevant cases.png"
            pathT = "torque distribution all relevant cases.png"
            pathM = "bending distribution all relevant cases.png"

        figV.savefig(pathV, dpi=150, bbox_inches="tight")
        figT.savefig(pathT, dpi=150, bbox_inches="tight")
        figM.savefig(pathM, dpi=150, bbox_inches="tight")

    plt.show()

if __name__ == "__main__":
    plot_internal_loads()
