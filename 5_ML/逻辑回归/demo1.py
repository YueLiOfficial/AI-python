from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import log_loss
import pandas as pd

data_df = pd.read_csv("./data/heart_disease.csv")

# print(data_df)
# print(data_df.isna().sum())

# 提取特征值和目标值
X = data_df.drop(columns="是否患有心脏病")
y = data_df["是否患有心脏病"]

# 数据处理
cat_cols = ["胸痛类型", "静息心电图结果", "峰值ST段的斜率", "地中海贫血"]
num_cols = ["年龄", "静息血压", "胆固醇", "最大心率", "运动后的ST下降", "主血管数量"]
bin_cols = ["性别", "空腹血糖", "运动性心绞痛"]

preprocesser = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), cat_cols),
    ("num", StandardScaler(), num_cols),
    ("bin", "passthrough", bin_cols)
])

model = Pipeline([
    ("preprecesser", preprocesser),
    ("regresser", LogisticRegression())
])

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
)

model.fit(x_train, y_train)

y_pred = model.predict(x_test)
y_pred_proba = model.predict_proba(x_test)
print(y_pred)
print(y_pred_proba)
print(f"准确率: {model.score(x_test, y_test)}")
print(f"损失函数值: {log_loss(y_test, y_pred_proba)}")
