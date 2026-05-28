import numpy as np

def lu(A):

    n = A.shape[0]
    U = A.copy()
    L = np.eye(n)

    for i in range(n-1):
        for j in range(i+1,n):
            L[j,i] = U[j,i]/U[i,i]
            U[j,i:] = U[j,i:] - L[j,i]*U[i,i:]

    return L,U

#求解下三角阵
def forward_substitution(L,b,unit_diagonal=False):

    n = len(b)
    y = np.zeros(n)

    for i in range(n):
        
        s =  np.dot(L[i,:i],y[:i])
        ##考虑到计算资源
        if unit_diagonal:
            y[i] = b[i] - s
        else:
            y[i] = (b[i] - s) / L[i,i]

    return y

#求解上三角阵
def backward_substitution(U,y):

    n = len(y)
    x = np.zeros(n)

    for i in reversed(range(n)):
        x[i] = (y[i] - np.dot(U[i,i+1:],x[i+1:]))/U[i,i]

    return x

def solve(A,b):

    L,U = lu(A)

    y = forward_substitution(L,b)

    x = backward_substitution(U,y)

    return x

A = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,10]
], dtype=float) 
b = np.array([1,5,10], dtype=float)
x = solve(A,b)
print(x)
L,U = lu(A)
print("L =")
print(L)        
print("\nU =")
print(U)