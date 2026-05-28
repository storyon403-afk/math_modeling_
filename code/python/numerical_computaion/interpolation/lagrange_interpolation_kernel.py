def lagrange_interpolation_kernel(x, x_nodes, y_nodes):
    """
    计算 Lagrange 插值多项式在 x 处的值
    param x:需要进行插值的点
    param x_nodes:插值节点的x的数组
    param y_nodes:插值节点的函数值的数组
    param P:插值结果
    """

    m = len(x_nodes)

    #插值结果
    P = 0

    for i in range(m):

        #计算 L_i(x):第i个基函数
        li = 1

        for j in range(m):

            #跳过 i=j 的情况
            if j != i:
                #计算 L_i(x) 的乘积项
                li *= (x-x_nodes[j])/(x_nodes[i]-x_nodes[j])

        #将 L_i(x) 乘以对应的 y_nodes[i] 并累加到 L 中
        P += y_nodes[i]*li
    

    return P