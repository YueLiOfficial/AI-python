from common.load_data import load_clothes_data
from torch.utils.data import DataLoader
import torch
from torch import nn, optim

batch_size = 128
lr = 0.01
epochs = 500

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载数据
train_dataset, eval_dataset = load_clothes_data()

# 创建数据加载器
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
eval_dataloader = DataLoader(eval_dataset, batch_size=batch_size)

# 定义模型
model = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=2),
    nn.Sigmoid(),
    nn.AvgPool2d(2, 2),
    nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
    nn.Sigmoid(),
    nn.AvgPool2d(2, 2),
    nn.Flatten(),
    nn.Linear(400, 120),
    nn.Sigmoid(),
    nn.Linear(120, 84),
    nn.Sigmoid(),
    nn.Linear(84, 10)
)

model.to(device)

# 定义损失函数
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr = lr)

def init_weights(layers):
    if isinstance(layers, nn.Linear) or isinstance(layers, nn.Conv2d):
        nn.init.xavier_normal_(layers.weight)

model.apply(init_weights)

# 训练模型
for epoch in range(epochs):
    train_crr_cnt = 0
    train_total_loss = 0
    model.train()
    for input, target in train_dataloader:
        input, target = input.to(device), target.to(device)

        output = model(input)

        loss = loss_fn(output, target)

        loss.backward()

        optimizer.step()
        optimizer.zero_grad()

        train_total_loss += loss.item()
        label = output.argmax(dim=-1)
        train_crr_cnt += (label == target).sum()

    train_epoch_loss = train_total_loss / len(train_dataloader)
    train_epoch_crr = train_crr_cnt / len(train_dataset)


    eval_total_loss = 0
    eval_crr_cnt = 0
    model.eval()
    with torch.no_grad():
        for input, target in eval_dataloader:
            input, target = input.to(device), target.to(device)

            output = model(input)

            loss = loss_fn(output, target)

            eval_total_loss += loss.item()
            label = output.argmax(dim=-1)
            eval_crr_cnt += (label == target).sum()

        eval_epoch_loss = eval_total_loss / len(eval_dataloader)
        eval_epoch_crr = eval_crr_cnt / len(eval_dataset)

    print(f"[第{epoch}/{epochs}轮] train_loss: {train_epoch_loss:.6f}, eval_loss: {eval_epoch_loss:.6f}, train_crr: {train_epoch_crr:.4f}, eval_crr: {eval_epoch_crr:.4f}")
