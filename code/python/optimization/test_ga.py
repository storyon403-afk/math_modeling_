import numpy as np
import matplotlib.pyplot as plt

from ga_kernel import genetic_algorithm


# 城市坐标

city = np.array([
    [1304,2312],
    [3639,1315],
    [4177,2244],
    [3712,1399],
    [3488,1535],
    [3326,1556],
    [3238,1229],
    [4196,1004],
    [4312,790],
    [4386,570],
    [3007,1970],
    [2562,1756],
    [2788,1491],
    [2381,1676],
    [1332,695],
    [3715,1678],
    [3918,2179],
    [4061,2370],
    [3780,2212],
    [3676,2578],
    [4029,2838],
    [4263,2931],
    [3429,1908],
    [3507,2367],
    [3394,2643],
    [3439,3201],
    [2935,3240],
    [3140,3550],
    [2545,2357],
    [2778,2826],
    [2370,2975]
])

n = len(city)


# 距离矩阵

dist = np.zeros((n, n))

for i in range(n):
    for j in range(n):

        dist[i, j] = np.linalg.norm(
            city[i] - city[j]
        )


# 调用遗传算法

best_path, best_distance, best_history = genetic_algorithm(
    dist,
    pop_size=100,
    max_gen=500,
    Pc=0.9,
    Pm=0.2,
    elite_num=2
)

# 闭合路径
path = np.append(best_path, best_path[0])

print("\n最优路径：")
print(path + 1)  # 转成1开始编号

print("\n最短距离：")
print(best_distance)


# 收敛曲线

plt.figure()

plt.plot(best_history, linewidth=2)

plt.xlabel("Generation")
plt.ylabel("Best Distance")
plt.title("GA Convergence")

plt.grid(True)


# 最优路径图

plt.figure()

# 城市点
for i in range(n):

    plt.plot(
        city[i,0],
        city[i,1],
        'ro'
    )

    plt.text(
        city[i,0] + 20,
        city[i,1] + 20,
        str(i + 1)
    )

# 路径
for i in range(n):

    c1 = path[i]
    c2 = path[i + 1]

    plt.plot(
        [city[c1,0], city[c2,0]],
        [city[c1,1], city[c2,1]],
        'b-',
        linewidth=1.5
    )

plt.title(f"Best Path, Distance = {best_distance:.2f}")

plt.axis("equal")

plt.grid(True)

plt.show()