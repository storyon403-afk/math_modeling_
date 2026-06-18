import math


# 微分方程
# y' = y - 2x / y
def f(x, y):
    return y - 2 * x / y

#返回精确解
def exact(x):
    return math.sqrt(2 * x + 1)


# 欧拉法
def euler(h):

    #定解区间 [0, 1]
    x = 0.0 
    y = 1.0

    print("Euler 方法")
    print("x\t\tapprox\t\t\texact\t\t\terror")

    while x <= 1 + 1e-10:
        y_true = exact(x)
        error = abs(y - y_true)

        print(
            f"{x:.2f}\t{y:.10f}\t{y_true:.10f}\t{error:.10f}"
        )

        y = y + h * f(x, y)
        x += h

    print()

# 隐式欧拉法，针对于这个问题，隐式欧拉法的迭代公式是：
# y_{n+1} = y_n + h * f(x_{n+1}, y_{n+1})
# 代入 f(x, y) 的表达式，可以得到一个关于 y_{n+1} 的二次方程：
# y_{n+1} = y_n + h * (y_{n+1} - 2 * x_{n+1} / y_{n+1})
# 整理后得到：
# (1 - h) * y_{n+1}^2 - y_n * y_{n+1} - 2 * h * x_{n+1} = 0
def implicit_euler(h):
    x = 0.0
    y = 1.0

    print("隐式Euler法")
    print("x\t\tapprox\t\t\texact\t\t\terror")

    while x <= 1 + 1e-10:
        y_true = exact(x)
        error = abs(y - y_true)

        print(
            f"{x:.2f}\t{y:.10f}\t{y_true:.10f}\t{error:.10f}"
        )

        x_next = x + h

        a = 1 - h
        b = -y
        c = 2 * h * x_next

        delta = b * b - 4 * a * c

        # 取正根
        y = (-b + math.sqrt(delta)) / (2 * a)

        x = x_next

    print()


# 改进欧拉法（Heun）
# Predictor-Corrector 方法，首先使用欧拉法预测 y 的值，然后使用这个预测值来计算斜率的平均值，最后更新 y 的值。
# 预测器：y_predict = y + h * f(x, y)
# 校正器：y = y + h * (f(x, y) + f(x + h, y_predict)) / 2
# 这种方法通过使用预测值来改进斜率的估计，从而提高了数值解的精度。
def improved_euler(h):
    x = 0.0
    y = 1.0

    print("改进欧拉法")
    print("x\t\tapprox\t\t\texact\t\t\terror")

    while x <= 1 + 1e-10:
        y_true = exact(x)
        error = abs(y - y_true)

        print(
            f"{x:.2f}\t{y:.10f}\t{y_true:.10f}\t{error:.10f}"
        )

        # Predictor
        k1 = f(x, y)
        y_predict = y + h * k1

        # Corrector
        k2 = f(x + h, y_predict)

        y = y + h * (k1 + k2) / 2

        x += h

    print()


# 梯形公式（隐式）
# 使用不动点迭代：
# y_new = y_n + h/2*(f(x_n,y_n)+f(x_(n+1),y_new))
def trapezoid(h):
    x = 0.0
    y = 1.0

    print("矩形公式")
    print("x\t\tapprox\t\t\texact\t\t\terror")

    while x <= 1 + 1e-10:
        y_true = exact(x)
        error = abs(y - y_true)

        print(
            f"{x:.2f}\t{y:.10f}\t{y_true:.10f}\t{error:.10f}"
        )

        x_next = x + h

        # 初值：欧拉预测
        y_new = y + h * f(x, y)

        # 不动点迭代
        for _ in range(20):
            y_new = y + h / 2 * (
                f(x, y) + f(x_next, y_new)
            )

        y = y_new
        x = x_next

    print()


# 主程序
def main():
    h = 0.1

    euler(h)

    implicit_euler(h)

    improved_euler(h)

    trapezoid(h)


if __name__ == "__main__":
    main()