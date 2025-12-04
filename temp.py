# python - compute the three variants
import numpy as np
from scipy import integrate

b = 8.5
def f(x):
    return 1.1191426967e-8 / 0.000002775904386521 / (2.75 - 0.21*x) ** 3

# single integral
I_b, _ = integrate.quad(f, 0, b)

# case A: all dims 0..b (original)
quad_all = I_b * b**3

# case B: first three dims 0..x (choose x), last 0..b
x = 4.25
I_x, _ = integrate.quad(f, 0, x)
case_B = I_x * x**2 * b

# case C: nested integrals 0<=x1<=x2<=x3<=x4<=b
# equals integral of f(t)*(b-t)^3 / 6
def integrand_for_nested(t):
    return f(t) * (b - t)**3 / 6.0
nested, _ = integrate.quad(integrand_for_nested, 0, b)

print("I(b) =", I_b)
print("quad_all (0..b)^4 =", quad_all)
print("case_B (three dims 0..x, last 0..b) with x=", x, "=>", case_B)
print("nested (iterated) =", nested)
