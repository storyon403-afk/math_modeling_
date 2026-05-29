import numpy as np


def simulated_annealing(
        objective,
        is_feasible,
        generate_initial_solution,
        lb,
        ub,

        # SA参数，可根据需要调整
        T=100,
        Tmin=1e-6,
        alpha=0.98,
        inner_iter=100,
        step=0.1
):
    """
    模拟退火算法
    param objective: 目标函数
    param is_feasible: 可行性检查函数，输入解，输出布尔值
    param generate_initial_solution: 生成初始解的函数，输出一个可行解
    param lb: 变量下界，数组
    param ub: 变量上界，数组
    param T: 初始温度
    param Tmin: 最小温度
    param alpha: 降温速率
    param inner_iter: 每个温度的内循环次数
    param step: 邻域搜索的步长
    return: 最优解，最优目标值，搜索路径，历史目标值
    """



    # 初始解
    x = generate_initial_solution()

    f = objective(x)

    best_x = x.copy()
    best_f = f

    path = [x.copy()]
    history = [f]

    # SA主循环
    while T > Tmin:

        for _ in range(inner_iter):

            # 邻域搜索
            x_new = x + step * np.random.randn(len(x))

            # 边界裁剪
            x_new = np.maximum(x_new, lb)
            x_new = np.minimum(x_new, ub)

            # 可行性检查
            if not is_feasible(x_new):
                continue

            f_new = objective(x_new)

            dE = f_new - f

            # Metropolis
            if dE < 0 or np.random.rand() < np.exp(-dE / T):

                x = x_new
                f = f_new

                path.append(x.copy())

                # 更新历史最优
                if f < best_f:

                    best_x = x.copy()
                    best_f = f

            history.append(f)

        # 降温
        T *= alpha

    return best_x, best_f, np.array(path), history