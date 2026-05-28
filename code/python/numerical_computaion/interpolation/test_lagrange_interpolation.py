import lagrange_interpolation_kernel as lik
import numpy as np
import matplotlib.pyplot as plt

### Lagrange 插值法测试 ###
# 通过插值函数 f(x) = 1/(1+25*x^2) 来测试 Lagrange 插值法的效果
# 该函数在区间 [-1,1] 上具有较大的振荡，因此是测试插值方法的一个经典函数
# 通过增加插值节点的数量来观察插值结果的变化，特别是当节点数量较多时，Lagrange 插值可能会出现 Runge 现象，即在区间边界附近出现较大的振荡。
# 通过绘制插值结果与原函数的图像来直观地比较两者的差异，并观察插值节点的位置对插值结果的影响
# 参考runge现象解释处：
#https://github.com/Yanbo-Zhu/ComputationMethod/blob/b8d28d6317162d32b779ac360de268c2f2e0cb05/01_04_%E6%8F%92%E5%80%BC%E6%B3%95/01_04_05_%E9%AB%98%E6%AC%A1%E6%8F%92%E5%80%BC%E7%9A%84Runge%E9%BE%99%E6%A0%BC%E7%8E%B0%E8%B1%A1%E5%92%8C%E5%88%86%E6%AE%B5%E4%BD%8E%E6%AC%A1%E6%8F%92%E5%80%BC.md

def f(x):
    return 1/(1+25*x**2)

#主函数
def main():

    #插值节点数量
    n_1 = 5
    n_2 = 10
    
    #生成插值节点和对应的函数值
    x_nodes_1 = np.linspace(-1,1,n_1+1)
    y_nodes_1 = f(x_nodes_1)

    x_nodes_2 = np.linspace(-1,1,n_2+1)
    y_nodes_2 = f(x_nodes_2)

    #生成用于绘制的 x 轴数据和对应的函数值
    x_plot = np.linspace(-1,1,1000)
    y_true = f(x_plot)

    #计算 Lagrange 插值结果
    y_interp_1 = np.array([
        lik.lagrange_interpolation_kernel(x, x_nodes_1, y_nodes_1)
        for x in x_plot
    ])

    y_interp_2 = np.array([
        lik.lagrange_interpolation_kernel(x, x_nodes_2, y_nodes_2)
        for x in x_plot
    ])

    ## 绘制原函数和插值结果的图像
    plt.figure(figsize = (10,6))

    plt.plot(x_plot, y_true,
         label='f(x)',
         linewidth=2)
    
    # 绘制插值结果
    plt.plot(x_plot, y_interp_1,
             label='Lagrange Interpolation (n=5)',
             linewidth = 2)

    plt.plot(x_plot, y_interp_2,
             label='Lagrange Interpolation (n=10)',
             linewidth = 2)

    # 绘制插值节点
    plt.scatter(x_nodes_1, y_nodes_1,
                s=60,
            zorder=5,
                label = 'Interpolation Nodes (n=5)')

    plt.scatter(x_nodes_2, y_nodes_2,
                s=60,
            zorder=5,
                label = 'Interpolation Nodes (n=10)')

    plt.title('10th Lagrange Interpolation of f(x)', fontsize=16)
    plt.xlabel('x', fontsize =14)
    plt.ylabel('f(x)',fontsize = 14)
    plt.legend()
    plt.grid(True)

    plt.show()

# 运行主函数
if __name__ == "__main__":
    main()
    

