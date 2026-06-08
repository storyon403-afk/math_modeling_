import numpy as np
import least_squares_kernel as lsk
from matplotlib import pyplot as plt

def main():

    x = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]) 
    y = np.array([3.206, 3.230, 3.255, 3.279, 3.288, 3.314, 3.312, 3.333, 3.349, 3.330])

    degree = 3

    coeffs_0 = lsk.least_squares_kernel(x, y, degree)
    coeffs_1 = lsk.least_squares_kernel_1(x, y, degree)

    # 打印拟合多项式的系数
    print("使用numpy的lstsq函数求解最小二乘问题得到的拟合多项式的系数：\n", coeffs_0)
    print("使用正规方程和lu分解内核求解线性方程组得到的拟合多项式的系数：\n", coeffs_1)
    # 计算在2025年的拟合值
    fit_value_0 = lsk.fit_value(coeffs_0, 2025)
    fit_value_1 = lsk.fit_value_1(coeffs_1, 2025)
    print("使用numpy的polyval函数计算的2025年的拟合值：\n", fit_value_0)
    print("使用循环实现多项式值计算的2025年的拟合值：\n", fit_value_1)

    print("系数误差:")
    print(coeffs_0 - coeffs_1)

    # 可视化拟合结果
    x_plot = np.linspace(2015, 2025, 500)


    y_plot_1 = np.array([
        lsk.fit_value_1(coeffs_1, xi)
        for xi in x_plot
    ])

    plt.figure(figsize=(8, 5))

    # 原始数据
    plt.scatter(x, y, label='Data')

    # 拟合曲线
    plt.plot(x_plot, y_plot_1, color='red',
             label=f'{degree}-degree polynomial fit (custom)')

    # 预测点
    plt.scatter([2025], [fit_value_1],
                s=80,
                marker='*',
                label='Prediction (2025)')

    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.title("Least Squares Polynomial Fitting")

    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()