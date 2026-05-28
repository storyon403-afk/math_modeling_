import numpy as np
import math
import lagrange_interpolation_kernel as lik
import newton_interpolation_kernel as nik


###测试 Newton 插值与 Lagrange 插值的结果和误差###
# 选择函数 f(x) = sin(x)，在区间 [0, π] 上使用 5 个等距节点进行插值
# 计算在 x = 1.6 处的插值结果，并比较与真实值 sin(1.6) 的误差，同时估计理论截断误差。

def f(x):
    return np.sin(x)

def main():

    # 节点数
    n = 5

    # 等距节点
    x_nodes = np.linspace(0, np.pi, n + 1)

    # 函数值
    y_nodes = f(x_nodes)

    # 需要插值的点
    x = 1.6

    # 真值
    true_value = f(x)

    # Lagrange 插值
    L_value = lik.lagrange_interpolation_kernel(
        x,
        x_nodes,
        y_nodes
    )

    # Newton 插值
    N_value = nik.newton_interpolation_kernel(
        x,
        x_nodes,
        y_nodes
    )


    # 实际误差
    L_error = abs(true_value - L_value)

    N_error = abs(true_value - N_value)

    # 理论截断误差
    omega = 1

    for xi in x_nodes:

        omega *= (x - xi)

    # sin(x) 的六阶导数绝对值 <= 1
    theory_error = abs(omega) / math.factorial(6)

    # 输出结果
    print(f"真实值 sin(1.6) = {true_value:.15f}\n")

    print(" Lagrange 插值")
    print(f"插值结果 = {L_value:.15f}")
    print(f"实际误差 = {L_error:.15e}\n")

    print(" Newton 插值")
    print(f"插值结果 = {N_value:.15f}")
    print(f"实际误差 = {N_error:.15e}\n")

    print("理论截断误差估计")
    print(f"误差上界 = {theory_error:.15e}")


# 程序入口
if __name__ == "__main__":
    main()
