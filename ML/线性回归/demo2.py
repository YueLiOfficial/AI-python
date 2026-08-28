import numpy as np
import matplotlib.pyplot as plt

X = np.array([5, 8, 10, 12, 15, 3, 7, 9, 14, 6]).reshape(-1, 1)
y = np.array([55, 65, 70, 75, 85, 50, 60, 72, 80, 58]).reshape(-1, 1)

X = np.hstack((np.ones((10, 1)), X))

lr = 0.01
beta = np.array([[1], [1]])
n = X.shape[0]
iter = 10000

def loss(beta):
    return np.sum((X @ beta - y) ** 2) / n

def grad(beta):
    return X.T @ (X @ beta - y) * 2 / n

loss_lst = []
for i in range(iter):
    loss_lst.append(loss(beta))
    beta = beta - lr * grad(beta)

plt.plot(range(iter), loss_lst)
plt.show()

print(beta)
