import numpy as np
import matplotlib.pyplot as plt

from sa_kernel import simulated_annealing


# 目标函数
# 这是一个非凸函数，具有多个局部最优解
def objective(x):

    x1, x2 = x

    return (
        x1**2
        + x2**2
        + 2*np.sin(2*x1)
        + np.cos(x2)
    )


# 可行域
def is_feasible(x):

    x1, x2 = x

    return (
        x1 + x2 >= 1
        and x1**2 + x2**2 <= 9
        and np.sin(x1) + x2 <= 1.5
        and x1 >= 0
        and x2 >= 0
    )


# 初始解
def generate_initial_solution():

    while True:

        x = np.random.rand(2)

        if is_feasible(x):
            return x


# 变量边界
lb = np.array([0, 0])
ub = np.array([3, 3])


# 调用SA
best_x, best_f, path, history = simulated_annealing(
    objective=objective,
    is_feasible=is_feasible,
    generate_initial_solution=generate_initial_solution,
    lb=lb,
    ub=ub
)


# 输出结果
print("最优解:")
print(best_x)

print("最优函数值:")
print(best_f)


# 收敛曲线
plt.plot(history)

plt.xlabel("Iteration")
plt.ylabel("f(x)")
plt.title("SA Convergence")

plt.grid(True)

plt.show()