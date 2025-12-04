import matplotlib.pyplot as plt
import numpy as np
import math
#Importing important constants and functions
from Aircraft_parameters import b
from load_calculations import V, T, M   
#Defining y values for plotting
def plot_internal_loads(y=None, n=200, title=None):
    if y is None:
        y = np.linspace(0, b/2, n)
    V_arr = V(y) if callable(V) else np.asarray(V)
    T_arr = T(y) if callable(T) else np.asarray(T)
    M_arr = M(y) if callable(M) else np.asarray(M)

    fig, axs = plt.subplots(3, 1, figsize=(8, 10), constrained_layout=True)

    if title:
        fig.suptitle(title, fontsize=14)

    axs[0].plot(y, V_arr, lw=2, color="tab:blue")
    axs[0].axhline(0, color="k", lw=0.6)
    axs[0].set_ylabel("V(y) [N]")
    axs[0].set_title("Internal Shear Force along wing span")
    axs[0].grid(True)

    axs[1].plot(y, T_arr, lw=2, color="tab:green")
    axs[1].axhline(0, color="k", lw=0.6)
    axs[1].set_ylabel("T(y) [N·m]")
    axs[1].set_title("Internal Torque along wing span")
    axs[1].grid(True)

    axs[2].plot(y, M_arr, lw=2, color="tab:red")
    axs[2].axhline(0, color="k", lw=0.6)
    axs[2].set_xlabel("Spanwise coordinate y (m)")
    axs[2].set_ylabel("M(y) [N·m]")
    axs[2].set_title("Internal Bending Moment along wing span")
    axs[2].grid(True)

    plt.show()

def plot_all_cases_internal_distributions(Load_cases_list, load_calculations, case_indexes=None, y=None, n=300, split_legend=False):
    """Plot V(y), T(y), M(y) for multiple load cases.
    Arguments:
      - Load_cases_list: nested list as parsed in main.py
      - load_calculations: module object (imported in main) providing set_operating_conditions(), precompute_internal_loads(), V(), T(), M()
      - split_legend: if True split legend entries into two stacked boxes placed to the right
    """
    if case_indexes is None:
        case_indexes = list(range(len(Load_cases_list)))
    if y is None:
        b = getattr(load_calculations, "b", None)
        if b is None:
            raise RuntimeError("plot_all_cases_internal_distributions: cannot determine wing span 'b' from load_calculations")
        y = np.linspace(0, b/2, n)

    figV, axV = plt.subplots(figsize=(8,4))
    figT, axT = plt.subplots(figsize=(8,4))
    figM, axM = plt.subplots(figsize=(8,4))

    for idx in case_indexes:
        case = Load_cases_list[idx]
        v_cruise = case[1]
        mass_aircraft =  case[2]
        load_factor = case[3]
        rho = case[4]
        mass_fuel = case[5]

        load_calculations.set_operating_conditions(v_cruise, mass_aircraft, load_factor, rho, mass_fuel)
        load_calculations.precompute_internal_loads(n=len(y))

        V_arr = load_calculations.V(y)
        T_arr = load_calculations.T(y)
        M_arr = load_calculations.M(y)

        label = f"{case[0]} (v={v_cruise:.1f} m/s, n={case[3]:.2f})"
        axV.plot(y, V_arr, lw=1.2, label=label)
        axT.plot(y, T_arr, lw=1.2, label=label)
        axM.plot(y, M_arr, lw=1.2, label=label)

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
