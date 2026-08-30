"""
    加载各种数据的包
"""

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def load_digit_data():
    df = pd.read_csv('../data/train.csv')

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

if __name__ == '__main__':
    x_train, x_test, y_train, y_test = load_digit_data()

    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
    print(x_train.dtype, x_test.dtype, y_train.dtype, y_test.dtype)
