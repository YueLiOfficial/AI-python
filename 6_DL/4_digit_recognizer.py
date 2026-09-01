"""
    手写数字识别案例: 训练模型
"""

import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
from torch.xpu import device

from common.load_data import load_digit_data

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 设置超参数
lr = 0.1
epochs = 30
batch_size = 64

# 准备数据
x_train, x_val, y_train, y_val = load_digit_data()

train_dataset = TensorDataset(x_train, y_train)
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
val_dataset = TensorDataset(x_val, y_val)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, drop_last=True)

# 定义模型
model = nn.Sequential(
    nn.Linear(784, 50),
    nn.ReLU(),
    nn.Linear(50, 100),
    nn.ReLU(),
    nn.Linear(100, 10)
).to(device=DEVICE)

# 定义损失模型和优化器
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr)

# 模型训练
for epoch in range(epochs):
    # 训练
    train_total_loss = 0
    train_crr_cnt = 0
    model.train()
    for input, target in train_dataloader:
        input = input.to(device=DEVICE)
        target = target.to(device=DEVICE)
    
        # 前向传播，预测结果
        output = model(input)

        # 计算损失
        loss = loss_fn(output, target)

        # 反向传播，计算梯度
        loss.backward()

        # 更新参数
        optimizer.step()

        # 每轮训练前清空梯度
        optimizer.zero_grad()

        train_total_loss += loss.item()

        pred_label = output.argmax(dim=-1)
        train_crr_cnt += (pred_label == target).sum()

    train_avg_loss = train_total_loss / len(train_dataloader)
    train_crr = train_crr_cnt / len(train_dataset)

    # 验证
    val_total_loss = 0
    val_crr_cnt = 0
    model.eval()
    with torch.no_grad():
        for input, target in val_dataloader:
            input = input.to(DEVICE)
            target = target.to(DEVICE)

            # 前向传播
            output = model(input)

            # 计算损失
            loss = loss_fn(output, target)

            val_total_loss += loss.item()

            pred_label = output.argmax(dim=-1)
            val_crr_cnt += (pred_label == target).sum()

    val_avg_loss = val_total_loss / len(val_dataloader)
    val_crr = val_crr_cnt / len(val_dataset)

    print(f"[第{epoch + 1}/{epochs}轮], train_loss: {train_avg_loss:.6f}, train_crr: {train_crr:.4f}, val_loss: {val_avg_loss:.6f}, val_crr: {val_crr:.4f}")