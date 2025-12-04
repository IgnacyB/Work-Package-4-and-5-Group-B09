# python - compute the three variants
import numpy as np

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
    Compute a function G(x) whose 4th derivative equals f(x), using
    repeated trapezoidal integration on a supplied ascending grid x_grid.
    Enforces G(0)=0 (i.e., G at the first grid point = 0).
    Returns (x_grid, G_grid) suitable for interpolation.
    """
    x = np.asarray(x_grid, dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.all(np.diff(x) > 0):
        raise ValueError("x_grid must be a 1D strictly ascending array with at least 2 points")

    # sample f on the grid
    f_grid = np.asarray([float(f(xi)) for xi in x], dtype=float)

    # helper: cumulative trapezoid integral with initial 0
    def cumtrap(y, x):
        # integral from x[0] to x[i]
        out = np.zeros_like(y, dtype=float)
        out[1:] = np.cumsum((y[:-1] + y[1:]) * np.diff(x) * 0.5)
        return out

    # Integrate 4 times
    I1 = cumtrap(f_grid, x)
    I2 = cumtrap(I1, x)
    I3 = cumtrap(I2, x)
    G  = cumtrap(I3, x)

    # G(x[0]) is already 0 by construction
    return x, G

# Example usage with your current f(x)
def G_numeric(x, x_grid=None, n=2000, xmax=8.5):
    """
    Convenience wrapper: builds a uniform grid, computes G on it,
    and interpolates G(x).
    """
    if x_grid is None:
        x_grid = np.linspace(0.0, xmax, n)
    X, G_grid = fourth_antiderivative_numeric(f, x_grid)
    return np.interp(np.asarray(x, dtype=float), X, G_grid)

if __name__ == "__main__":
    xs = np.array([0.0, 2.0, 4.0, 6.0, 8.0, 8.5])
    # compute G on a grid and interpolate
    print("G(0) =", G_numeric(0.0))
    print("G(8.5) =", G_numeric(8.5))

    # quick numeric check: finite-difference 4th derivative of G_numeric vs f
    def d4_numeric(g, x, h=1e-3):
        return (g(x+2*h) - 4*g(x+h) + 6*g(x) - 4*g(x-h) + g(x-2*h)) / (h**4)

    for x in xs:
        print(f"x={x:.2f}  f(x)={f(x):.6e}  d4G≈{d4_numeric(lambda t: G_numeric(t), x):.6e}")


