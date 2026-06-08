import numpy as np
import composite_trapezoid_kernel as ctk
import composite_simpson_kernel as csk

def f(x):
    return 2 + np.sin(2 * x)

def main():
    a = 0
    b = 10
    n = 100

    result_trapezoid = ctk.composite_trapezoid(f, a, b, n)
    result_simpson = csk.composite_simpson(f, a, b, n)

    print("使用复合梯形公式计算的积分结果：", result_trapezoid)
    print("使用复合Simpson公式计算的积分结果：", result_simpson)

if __name__ == "__main__":
    main()