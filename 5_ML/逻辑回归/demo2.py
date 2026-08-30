import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

data_df = pd.read_csv("./data/train.csv")

X = data_df.drop(columns="label")
y = data_df["label"]

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

model = LogisticRegression(max_iter=10000)

model.fit(x_train, y_train)

print(model.score(x_test, y_test))

digit = x_test[123].reshape(1, -1)
res = model.predict(digit)
print(res)
plt.imshow(digit.reshape(28, 28))
plt.show()