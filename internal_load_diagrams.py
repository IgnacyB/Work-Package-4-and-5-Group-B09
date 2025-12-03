import matplotlib.pyplot as plt
import numpy as np
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

def plot_all_cases_internal_distributions(Load_cases_list, load_calculations, case_indexes=None, y=None, n=300):
    """Plot V(y), T(y), M(y) for multiple load cases.
    Arguments:
      - Load_cases_list: nested list as parsed in main.py
      - load_calculations: module object (imported in main) providing set_operating_conditions(), precompute_internal_loads(), V(), T(), M()
    """
    if case_indexes is None:
        case_indexes = list(range(len(Load_cases_list)))
    if y is None:
        y = np.linspace(0, b/2, n)

    figV, axV = plt.subplots(figsize=(8,4))
    figT, axT = plt.subplots(figsize=(8,4))
    figM, axM = plt.subplots(figsize=(8,4))

    for idx in case_indexes:
        case = Load_cases_list[idx]
        mass_aircraft = case[2] * case[3]
        v_cruise = case[1]
        rho = case[4]
        mass_fuel = case[5]

        # set operating conditions and precompute grid for speed/consistency
        load_calculations.set_operating_conditions(mass_aircraft, v_cruise, rho, mass_fuel)
        # ensure precompute uses same grid length as y for consistent interpolation
        load_calculations.precompute_internal_loads(n=len(y))

        V_arr = load_calculations.V(y)
        T_arr = load_calculations.T(y)
        M_arr = load_calculations.M(y)

        label = f"{case[0]} (v={v_cruise:.1f} m/s, n={case[3]:.2f})"
        axV.plot(y, V_arr, lw=1.2, label=label)
        axT.plot(y, T_arr, lw=1.2, label=label)
        axM.plot(y, M_arr, lw=1.2, label=label)

    axV.set_title("Internal Shear V(y) — multiple load cases")
    axV.set_xlabel("y (m)"); axV.set_ylabel("V(y) [N]"); axV.grid(True); axV.legend(loc="best", fontsize="small")

    axT.set_title("Internal Torque T(y) — multiple load cases")
    axT.set_xlabel("y (m)"); axT.set_ylabel("T(y) [N·m]"); axT.grid(True); axT.legend(loc="best", fontsize="small")

    axM.set_title("Bending Moment M(y) — multiple load cases")
    axM.set_xlabel("y (m)"); axM.set_ylabel("M(y) [N·m]"); axM.grid(True); axM.legend(loc="best", fontsize="small")

    plt.show()

if __name__ == "__main__":
    plot_internal_loads()
