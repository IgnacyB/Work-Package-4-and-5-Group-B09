import matplotlib.pyplot as plt
import math
import numpy as np

# choose a plotting style from available styles with sensible fallbacks
preferred_styles = ["seaborn-darkgrid", "seaborn", "seaborn-whitegrid", "ggplot", "classic", "default"]
for style in preferred_styles:
    if style in plt.style.available:
        plt.style.use(style)
        break
else:
    plt.style.use("default")

from Aircraft_parameters import b
from Twist_Distribution import twist_function
from Lateral_Deflection import lateral_deflection_function

# apply a clean plotting style and sensible defaults
DEFAULT_FIGSIZE = (9, 5)
DEFAULT_DPI = 120
LABEL_FONTSIZE = 12
TITLE_FONTSIZE = 14
TICK_FONTSIZE = 10
LINEWIDTH = 2.0
MARKERSIZE = 6

# lateral deflection graph
def plot_lateral_deflection(title=None, figsize=DEFAULT_FIGSIZE, dpi=DEFAULT_DPI):
    """Plot lateral deflection. If title provided, include it in the figure title."""
    y_grid, v_grid = lateral_deflection_function()
    y = np.asarray(y_grid)
    v = np.asarray(v_grid)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(y, v, lw=LINEWIDTH, color="#1f77b4", label="Lateral deflection")
    ax.fill_between(y, 0, v, alpha=0.12, color="#1f77b4")
    # mark and annotate peak absolute deflection
    idx_max = np.argmax(np.abs(v))
    ax.plot(y[idx_max], v[idx_max], "o", color="#d62728", markersize=MARKERSIZE)
    ax.annotate(f"{v[idx_max]:.3f} m", xy=(y[idx_max], v[idx_max]),
                xytext=(8, 8), textcoords="offset points", fontsize=TICK_FONTSIZE,
                arrowprops=dict(arrowstyle="->", lw=1))

    ax.axhline(0, color="k", lw=0.8, alpha=0.6)
    if title:
        ax.set_title(f"{title} — Lateral deflection", fontsize=TITLE_FONTSIZE)
        ax.legend(fontsize=TICK_FONTSIZE)
    else:
        ax.set_title("Lateral deflection along wingspan", fontsize=TITLE_FONTSIZE)

    ax.set_xlabel("Spanwise position [m]", fontsize=LABEL_FONTSIZE)
    ax.set_ylabel("Lateral deflection [m]", fontsize=LABEL_FONTSIZE)
    ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    fig.tight_layout()
    plt.show()


# twist distribution
def plot_twist_distribution(title=None, figsize=DEFAULT_FIGSIZE, dpi=DEFAULT_DPI):
    """Plot twist distribution. If title provided, include it in the figure title."""
    y_grid, twist_grid = twist_function()
    y = np.asarray(y_grid)
    twist_deg = np.asarray(twist_grid) * 180.0 / math.pi

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(y, twist_deg, lw=LINEWIDTH, color="#2ca02c", label="Twist (deg)")
    # mark zero line and peak twist
    ax.axhline(0, color="k", lw=0.8, alpha=0.6)
    idx_max = np.argmax(np.abs(twist_deg))
    ax.plot(y[idx_max], twist_deg[idx_max], "o", color="#ff7f0e", markersize=MARKERSIZE)
    ax.annotate(f"{twist_deg[idx_max]:.2f}°", xy=(y[idx_max], twist_deg[idx_max]),
                xytext=(8, 8), textcoords="offset points", fontsize=TICK_FONTSIZE,
                arrowprops=dict(arrowstyle="->", lw=1))

    if title:
        ax.set_title(f"{title} — Twist distribution", fontsize=TITLE_FONTSIZE)
        ax.legend(fontsize=TICK_FONTSIZE)
    else:
        ax.set_title("Twist distribution along wingspan", fontsize=TITLE_FONTSIZE)

    ax.set_xlabel("Spanwise position [m]", fontsize=LABEL_FONTSIZE)
    ax.set_ylabel("Angle of twist [degree]", fontsize=LABEL_FONTSIZE)
    ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_lateral_deflection()
    plot_twist_distribution()