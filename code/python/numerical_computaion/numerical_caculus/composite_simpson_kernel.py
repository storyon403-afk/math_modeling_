import numpy as np

def composite_simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n必须为偶数")

    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    y = f(x)

    result = h / 2 * (
        y[0]
        + 2 * np.sum(y[1:-1])
        + y[-1]
    )

    return result