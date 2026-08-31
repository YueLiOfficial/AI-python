"""
    手写数字识别案例
"""

import torch
from common import load_data
from torch import  nn

x_train, x_test, y_train, y_test = load_data.load_digit_data()

# 创建模型
model = nn.Sequential(
    nn.Linear(784, 50),
    nn.ReLU(),
    nn.Linear(50, 100),
    nn.ReLU(),
    nn.Linear(100, 10),
)

# 加载数据
model_dict = torch.load("./data/nn_example.pt")
model.load_state_dict(model_dict)

y_pred = model(x_test)
# print(f"模型原始输出:\n{y_pred}")
# print(f"输出形状:{y_pred.shape}")

# 获取预测值
y_pred = torch.argmax(y_pred, dim=1)

# 计算准确率
crr_cnt = (y_pred == y_test).sum()
total = len(y_test)
crr = crr_cnt / total
print(f"准确率: {crr}")