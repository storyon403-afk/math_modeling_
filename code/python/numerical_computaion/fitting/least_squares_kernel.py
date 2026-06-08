import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from linalg_solve import lu_kernel as lu_k

# 利用numpy的vander函数构造Vandermonde矩阵
# 使用numpy的lstsq函数求解最小二乘问题，得到拟合多项式的系数。最后，使用numpy的polyval函数计算拟合值。
def least_squares_kernel(x, y, degree):
    """
    最小二乘拟合核函数
    :param x: 自变量数据点
    :param y: 因变量数据点
    :param degree: 多项式的阶数
    :return: 拟合多项式的系数
    """
    # 构造 Vandermonde 矩阵
    A = np.vander(x, degree + 1, increasing=True)
    
    # 使用最小二乘法求解系数
    coeffs = np.linalg.lstsq(A, y, rcond=None)[0]

    return coeffs

def fit_value(coeffs, x):
    """
    使用拟合多项式的系数计算拟合值
    :param coeffs: 拟合多项式的系数
    :param x: 需要计算拟合值的自变量
    :return: 拟合值
    """
    # 计算拟合值
    fit_value = np.polyval(coeffs[::-1], x)
    
    return fit_value    

# 另一种实现方式，直接构造设计矩阵并使用正规方程求解系数
# 可以使用之前实现的lu分解内核来求解线性方程组，
# 从而完全不依赖于numpy的线性代数模块。
def least_squares_kernel_1(x, y, degree):
    """
    : param x : 自变量数据点
    : param y : 因变量数据点
    : param degree : int  多项式阶数

    Returns : 拟合系数
    """

    x = np.asarray(x)
    y = np.asarray(y)

    m = len(x)

    # 构造矩阵A，其中A[i, j] = x[i] ** j，实现一个 Vandermonde 矩阵
    A = np.zeros((m, degree + 1))

    for i in range(m):
        for j in range(degree + 1):
            A[i, j] = x[i] ** j

    # 正规方程
    ATA = A.T @ A
    ATy = A.T @ y

    # 使用lu分解内核求解线性方程组
    #from lu_kernel import solve
    #coeffs = solve(ATA, ATy)
    coeffs = lu_k.solve(ATA, ATy)

    return coeffs

#循环实现多项式值的计算
def fit_value_1(coeffs, x):
    s = 0
    for i in range(len(coeffs)):
        s += coeffs[i] * x**i

    return s