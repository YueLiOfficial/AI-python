from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

X = np.array([5, 8, 10, 12, 15, 3, 7, 9, 14, 6]).reshape(-1, 1)
y = np.array([55, 65, 70, 75, 85, 50, 60, 72, 80, 58]).reshape(-1, 1)

model = LinearRegression()

model.fit(X, y)

# print(model.coef_, model.intercept_)

x_line = np.arange(0, 20, 0.1).reshape(-1, 1)
y_line = model.predict(x_line)

plt.plot(x_line, y_line)

plt.scatter(X, y)

plt.scatter(11, model.predict([[11]]), c="r")

plt.show()
