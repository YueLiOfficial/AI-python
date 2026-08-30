import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

data_df = pd.read_csv("./data/Advertising.csv")

# print(data_df.columns)
data_df.drop(["Unnamed: 0"], axis=1, inplace=True)
# print(data_df)
# print(data_df.isna().sum())

# 计算皮尔逊相关系数
x = data_df.drop(["Sales"], axis=1)
y = data_df["Sales"]

corr = x.corrwith(y, method="pearson")

# print(corr)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=22)

# 训练集标准化
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

model = LinearRegression()
model.fit(x_train, y_train)

# print(model.coef_, model.intercept_)

y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
print(f"均方误差: {mse}")

train_score = model.score(x_train, y_train)
print(f"训练集决定系数: {train_score}")
test_score = model.score(x_test, y_test)
print(f"测试集决定系数: {test_score}")
