import matplotlib.pyplot as plt
import numpy as np
from Aircraft_parameters import b
from load_calculations import V, T, M

def plot_internal_loads(y=None, n=200, title=None):
    if y is None:
        y = np.linspace(0, b/2, n)

    V_arr = V(y) if callable(V) else np.asarray(V)
    T_arr = T(y) if callable(T) else np.asarray(T)
    M_arr = M(y) if callable(M) else np.asarray(M)

    # Shear force — separate figure
    figV, axV = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title: figV.suptitle(f"{title} — Shear V(y)")
    axV.plot(y, V_arr, lw=2, color="tab:blue")
    axV.axhline(0, color="k", lw=0.6)
    axV.set_xlabel("Spanwise coordinate y (m)")
    axV.set_ylabel("V(y) [N]")
    axV.set_title("Internal Shear Force along wing span")
    axV.grid(True)

    # Torque — separate figure
    figT, axT = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title: figT.suptitle(f"{title} — Torque T(y)")
    axT.plot(y, T_arr, lw=2, color="tab:green")
    axT.axhline(0, color="k", lw=0.6)
    axT.set_xlabel("Spanwise coordinate y (m)")
    axT.set_ylabel("T(y) [N·m]")
    axT.set_title("Internal Torque along wing span")
    axT.grid(True)

    # Bending moment — separate figure
    figM, axM = plt.subplots(figsize=(8, 4), constrained_layout=True)
    if title: figM.suptitle(f"{title} — Bending Moment M(y)")
    axM.plot(y, M_arr, lw=2, color="tab:red")
    axM.axhline(0, color="k", lw=0.6)
    axM.set_xlabel("Spanwise coordinate y (m)")
    axM.set_ylabel("M(y) [N·m]")
    axM.set_title("Internal Bending Moment along wing span")
    axM.grid(True)

    plt.show()

if __name__ == "__main__":
    plot_internal_loads()