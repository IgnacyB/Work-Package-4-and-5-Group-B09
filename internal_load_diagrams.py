import matplotlib.pyplot as plt
import numpy as np
#Importing important constants and functions
from Wing_geometry import b
from load_calculations import V, T, M   
#Defining y values for plotting
def plot_internal_loads(y=None, n=200):
    if y is None:
        y = np.linspace(0, b/2, n)
    V_arr = V(y) if callable(V) else np.asarray(V)
    T_arr = T(y) if callable(T) else np.asarray(T)
    M_arr = M(y) if callable(M) else np.asarray(M)

    fig, axs = plt.subplots(3, 1, figsize=(8, 10), constrained_layout=True)

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

if __name__ == "__main__":
    plot_internal_loads()
