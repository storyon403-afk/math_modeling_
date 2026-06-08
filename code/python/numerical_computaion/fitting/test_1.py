import numpy as np
import least_squares_kernel as lsk
from matplotlib import pyplot as plt

def main():

    # 原始年份
    years = np.array([2015, 2016, 2017, 2018, 2019,
                      2020, 2021, 2022, 2023, 2024])

    y = np.array([3.206, 3.230, 3.255, 3.279, 3.288,
                  3.314, 3.312, 3.333, 3.349, 3.330])

    #数值稳定化处理：将年份转换为相对于2015年的偏移量
    base_year = years[0]
    x = years - base_year
    # x = [0,1,2,3,4,5,6,7,8,9] 

    degree = 3

    coeffs_0 = lsk.least_squares_kernel(x, y, degree)
    coeffs_1 = lsk.least_squares_kernel_1(x, y, degree)

    print("使用numpy的lstsq函数求解最小二乘问题得到的拟合多项式系数：")
    print(coeffs_0)

    print("使用正规方程+LU分解得到的拟合多项式系数：")
    print(coeffs_1)

    print("系数误差：")
    print(coeffs_0 - coeffs_1)

    # 预测2025
    x_pred = 2025 - base_year

    fit_value_0 = lsk.fit_value(coeffs_0, x_pred)
    fit_value_1 = lsk.fit_value_1(coeffs_1, x_pred)

    print("2025年预测值(lstsq)：")
    print(fit_value_0)

    print("2025年预测值(正规方程+LU)：")
    print(fit_value_1)

    print("预测误差：")
    print(abs(fit_value_0 - fit_value_1))

    # 绘图
    x_plot = np.linspace(0, 10, 500)

    y_plot_0 = np.polyval(coeffs_0[::-1], x_plot)

    y_plot_1 = np.array([
        lsk.fit_value_1(coeffs_1, xi)
        for xi in x_plot
    ])

    plt.figure(figsize=(8, 5))

    plt.scatter(x, y, label='Data')

    plt.plot(
        x_plot,
        y_plot_0,
        label='lstsq',
        linewidth=2
    )

    plt.plot(
        x_plot,
        y_plot_1,
        '--',
        label='normal equation + LU',
        linewidth=2
    )

    plt.scatter(
        [x_pred],
        [fit_value_1],
        marker='*',
        s=100,
        label='Prediction (2025)'
    )

    plt.xlabel("Year - 2015")
    plt.ylabel("Value")
    plt.title("Least Squares Polynomial Fitting")

    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()