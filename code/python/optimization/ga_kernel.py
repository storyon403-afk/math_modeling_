# ga_core.py

import numpy as np


# 路径长度
def path_length(path, dist):

    n = len(path)

    L = 0

    for i in range(n - 1):
        L += dist[path[i], path[i + 1]]

    L += dist[path[-1], path[0]]

    return L


# 锦标赛选择

def tournament_selection(pop, fit, k=4):

    idx = np.random.choice(len(pop), k, replace=False)

    candidate_fit = fit[idx]

    best = np.argmin(candidate_fit)

    return pop[idx[best]].copy()


# OX顺序交叉

def OX(p1, p2):

    n = len(p1)

    a = np.random.randint(0, n - 1)
    b = np.random.randint(a + 1, n)

    c1 = -np.ones(n, dtype=int)
    c2 = -np.ones(n, dtype=int)

    # 保留片段
    c1[a:b + 1] = p1[a:b + 1]
    c2[a:b + 1] = p2[a:b + 1]

    # 填充 c1
    remain = [x for x in p2 if x not in c1]

    index = list(range(b + 1, n)) + list(range(0, a))

    for i, idx in enumerate(index):
        c1[idx] = remain[i]

    # 填充 c2
    remain = [x for x in p1 if x not in c2]

    for i, idx in enumerate(index):
        c2[idx] = remain[i]

    return c1, c2


# 交换变异

def mutation(child):

    n = len(child)

    i = np.random.randint(0, n)
    j = np.random.randint(0, n)

    child[i], child[j] = child[j], child[i]

    return child


# 遗传算法主函数

def genetic_algorithm(
        dist,
        pop_size=100,
        max_gen=500,
        Pc=0.9,
        Pm=0.2,
        elite_num=2
):
    """
    遗传算法求解TSP问题
    param dist: 距离矩阵，二维数组
    param pop_size: 种群大小
    param max_gen: 最大迭代次数
    param Pc: 交叉概率
    param Pm: 变异概率
    param elite_num: 精英保留数量
    return: 最优路径，最短距离，历史最优距离列表
    """

    n = len(dist)

    # 初始化种群
    pop = np.array([
        np.random.permutation(n)
        for _ in range(pop_size)
    ])

    best_history = []

    best_path = None
    best_fit = np.inf

    # 主循环
    for gen in range(max_gen):

        # 适应度
        fit = np.array([
            path_length(ind, dist)
            for ind in pop
        ])

        # 当前最优
        idx = np.argmin(fit)

        if fit[idx] < best_fit:
            best_fit = fit[idx]
            best_path = pop[idx].copy()

        best_history.append(best_fit)

        print(f"第 {gen + 1} 代: {best_fit:.2f}")

        # 精英保留
        sort_idx = np.argsort(fit)

        new_pop = pop[sort_idx[:elite_num]].copy()

        # 生成新种群
        while len(new_pop) < pop_size:

            # 选择
            p1 = tournament_selection(pop, fit)
            p2 = tournament_selection(pop, fit)

            # 交叉
            if np.random.rand() < Pc:
                c1, c2 = OX(p1, p2)
            else:
                c1, c2 = p1.copy(), p2.copy()

            # 变异
            if np.random.rand() < Pm:
                c1 = mutation(c1)

            if np.random.rand() < Pm:
                c2 = mutation(c2)

            new_pop = np.vstack([new_pop, c1])

            if len(new_pop) < pop_size:
                new_pop = np.vstack([new_pop, c2])

        pop = new_pop

    return best_path, best_fit, best_history