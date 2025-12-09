# python - compute the three variants
import numpy as np
from scipy.integrate import cumulative_trapezoid

# given
def f(x):
    return 1.1191426967e-8 / 0.000002775904386521 / (2.75 - 0.21*x) ** 3

# constants for compactness
A = 1.1191426967e-8 / 0.000002775904386521

# A function whose 4th derivative equals f(x), with G(0)=0
def G(x):
    """
    Fourth antiderivative of f(x) with G(0) = 0.
    G''''(x) = f(x)
    """
    u = 2.75 - 0.21 * np.asarray(x, dtype=float)
    # base fourth antiderivative (up to additive constant)
    base = -(A / 0.42) * (u * np.log(np.abs(u)) - u)
    # subtract value at x=0 to enforce G(0)=0
    u0 = 2.75
    base0 = -(A / 0.42) * (u0 * np.log(u0) - u0)
    return base - base0

def fourth_antiderivative_numeric(f, x_grid):
    """
    Compute G(x) s.t. G''''(x) = f(x) using repeated trapezoidal integration.
    Boundary conditions:
      - after first integral: I1(b) = 0
      - after second integral: I2(b) = 0
      - after third integral: I3(0) = 0
      - after fourth integral: G(0)  = 0
    Returns (x_grid, G_grid).
    """
    x = np.asarray(x_grid, dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.all(np.diff(x) > 0):
        raise ValueError("x_grid must be a 1D strictly ascending array with at least 2 points")

    # sample f on the grid
    f_grid = np.asarray([float(f(xi)) for xi in x], dtype=float)

    # 1st integral: I1 = ∫ f dx with I1(x0)=0, then enforce I1(b)=0
    I1 = cumulative_trapezoid(f_grid, x, initial=0.0)
    I1 = I1 - I1[-1]  # shift so I1(b)=0

    # 2nd integral: I2 = ∫ I1 dx with I2(x0)=0, then enforce I2(b)=0
    I2 = cumulative_trapezoid(I1, x, initial=0.0)
    I2 = I2 - I2[-1]  # shift so I2(b)=0

    # 3rd integral: I3 = ∫ I2 dx with I3(x0)=0 (already satisfied)
    I3 = cumulative_trapezoid(I2, x, initial=0.0)

    # 4th integral: G = ∫ I3 dx with G(x0)=0 (already satisfied)
    G  = cumulative_trapezoid(I3, x, initial=0.0)

    return x, G

# Convenience wrapper (unchanged)
def G_numeric(x, x_grid=None, n=2000, xmax=8.5, f=None):
    """
    Build a grid, compute G on it for provided f, and interpolate G(x).
    """
    if f is None:
        # default f from your previous example
        def f(t):
            return 1.1191426967e-8 / 0.000002775904386521 / (2.75 - 0.21*t) ** 3
    if x_grid is None:
        x_grid = np.linspace(0.0, xmax, n)
    X, G_grid = fourth_antiderivative_numeric(f, x_grid)
    return np.interp(np.asarray(x, dtype=float), X, G_grid)

if __name__ == "__main__":
    # test with previous f and grid [0, 8.5]
    def f(t):
        return 1.1191426967e-8 / 0.000002775904386521 / (2.75 - 0.21*t) ** 3
    X = np.linspace(0.0, 8.5, 2000)
    X, G = fourth_antiderivative_numeric(f, X)

    # quick checks of boundary conditions
    print(f"I1(b)=0 and I2(b)=0 enforced; G(0)={G[0]:.3e}, G(b)={G[-1]:.3e}")


