"""
    加载各种数据的包
"""

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from torch.utils.data import TensorDataset, DataLoader

def load_digit_data():
    df = pd.read_csv('./data/train.csv')

    # 划分输入特征和输出特征
    X = df.drop('label', axis=1)
    y = df['label']

    # 划分数据集和测试集
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, random_state=42
    )

    # 特征转换：归一化
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # 将数据转换为张量
    x_train = torch.tensor(x_train).float()
    x_test = torch.tensor(x_test).float()
    y_test = torch.tensor(y_test.values)
    y_train = torch.tensor(y_train.values)

    return x_train, x_test, y_train, y_test

def load_house_prices_data():
    df = pd.read_csv("./data/house_prices.csv")

    df.drop("Id", axis=1, inplace=True)

    X = df.drop("SalePrice", axis=1)
    y = df["SalePrice"]
    
    num_cols = X.select_dtypes(include="number").columns.to_list()
    cat_cols = X.select_dtypes(include="str").columns.to_list()

    num_cols.remove("MSSubClass")
    cat_cols.append("MSSubClass")

    num_pipeline = Pipeline([
        ("mean", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("fillna", SimpleImputer(strategy="constant", fill_value="missing")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    transformer = ColumnTransformer([
        ("num_cols", num_pipeline, num_cols),
        ("cat_cols", cat_pipeline, cat_cols)
    ])

    x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    x_train = transformer.fit_transform(x_train)
    x_test = transformer.transform(x_test)

    x_train = torch.tensor(x_train, dtype=torch.float)
    x_test = torch.tensor(x_test, dtype=torch.float)
    y_train = torch.tensor(y_train.values)
    y_test = torch.tensor(y_test.values)

    return x_train, x_test, y_train, y_test


def load_clothes_data():
    train_df = pd.read_csv("./data/fashion-mnist_train.csv")
    test_df = pd.read_csv("./data/fashion-mnist_test.csv")

    x_train = train_df.drop("label", axis=1)
    y_train = train_df["label"]
    x_test = test_df.drop("label", axis=1)
    y_test = test_df["label"]

    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    x_train = torch.tensor(x_train, dtype=torch.float)
    x_test = torch.tensor(x_test, dtype=torch.float)
    y_train = torch.tensor(y_train)
    y_test = torch.tensor(y_test)
    
    x_train = x_train.reshape(-1, 1, 28, 28)
    x_test = x_test.reshape(-1, 1, 28, 28)

    train_dataset = TensorDataset(x_train, y_train)
    test_dataset = TensorDataset(x_test, y_test)

    return train_dataset, test_dataset

if __name__ == '__main__':
    # x_train, x_test, y_train, y_test = load_digit_data()

    # print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
    # print(x_train.dtype, x_test.dtype, y_train.dtype, y_test.dtype)

    # x_train, x_test, y_train, y_test = load_house_prices_data()
    # print(x_train.dtype, x_test.dtype, y_train.dtype, y_test.dtype)

    load_clothes_data()
