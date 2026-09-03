from common.load_data import load_house_prices_data
import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

batch_size = 32
lr = 0.01
epochs = 500

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 创建数据集和数据加载器
x_train, x_eval, y_train, y_eval = load_house_prices_data()

train_dataset = TensorDataset(x_train, y_train)
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True, drop_last=True)

eval_dataset = TensorDataset(x_eval, y_eval)
eval_dataloader = DataLoader(eval_dataset, batch_size=32)

feature_number = x_train.shape[1]

# 定义模型
model = nn.Sequential(
    nn.Linear(feature_number, 128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(128, 1),
)

model.to(device)

# 定义损失函数
def log_rmse(pred, target):
    mse = nn.MSELoss()

    pred.squeeze_()
    pred = torch.clamp(pred, min=1)

    y_pred = torch.log(pred)
    y_true = torch.log(target)

    return torch.sqrt(mse(y_pred, y_true))

optimizer = optim.Adam(model.parameters(), lr=lr)

train_loss_list = []
eval_loss_list = []

# 训练模型
for epoch in range(epochs):
    train_epoch_total_loss = 0
    eval_epoch_total_loss = 0

    model.train()
    for input, target in train_dataloader:
        input, target = input.to(device), target.to(device)

        output = model(input)

        loss = log_rmse(output, target)

        loss.backward()

        optimizer.step()

        optimizer.zero_grad()

        train_epoch_total_loss += loss.item()

    train_epoch_avg_loss = train_epoch_total_loss / len(train_dataloader)

    train_loss_list.append(train_epoch_avg_loss)

    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():
        for input, target in eval_dataloader:
            input, target = input.to(device), target.to(device)

            output = model(input)

            loss = log_rmse(output, target)

            eval_epoch_total_loss += loss.item()

            y_true.append(target.cpu())
            y_pred.append(output.cpu())

    y_true = torch.cat(y_true)
    y_pred = torch.cat(y_pred)

    r2 = r2_score(y_true, y_pred)

    eval_epoch_avg_loss = eval_epoch_total_loss / len(eval_dataloader)

    eval_loss_list.append(eval_epoch_avg_loss)

    print(f"第{epoch + 1}/{epochs}轮, train_loss: {train_epoch_avg_loss:.6f}, eval_loss: {eval_epoch_avg_loss:.6f}, r2: {r2:.4f}")

plt.plot(train_loss_list, c="r", label="train_loss")
plt.plot(eval_loss_list, c="b", label="eval_loss")

plt.show()
