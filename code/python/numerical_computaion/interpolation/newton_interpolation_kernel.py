import numpy as np

def newton_interpolation_kernel(x, x_nodes, y_nodes):

    """
    计算 Newton 插值多项式在 x 处的值
    param x:需要进行插值的点
    param x_nodes:插值节点的x的数组
    param y_nodes:插值节点的函数值的数组
    param P:插值结果
    """

    m = len(x_nodes)

    # 构造差商表
    D = np.zeros((m, m))

    # 第一列
    D[:, 0] = y_nodes

    # 计算差商, j = 0 是已经填充的第一列
    for j in range(1, m):

        # 计算第 j 列的差商
        for i in range(m - j):

            #采用向前差分表的方式计算差商
            D[i, j] = (
                (D[i + 1, j - 1] - D[i, j - 1])
                /
                (x_nodes[i + j] - x_nodes[i])
            )

    # 初始化插值结果
    P = D[0, 0]

    # 计算 Newton 插值多项式的值
    prod_term = 1

    # 从第一项开始累加, j=0 的项已经包含在 P 中
    #使用Newton向前插值公式
    for k in range(1, m):

        prod_term *= (x - x_nodes[k - 1])

        P += D[0, k] * prod_term

    return P