import numpy as np

def composite_trapezoid(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    return h / 2 * (
        y[0]
        + 2 * np.sum(y[1:-1])
        + y[-1]
    )
