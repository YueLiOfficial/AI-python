import torch
import torch.nn as nn
from torchsummary import summary

DEVICE = "cuda" if torch.cuda.is_available else "cpu"

model = nn.Sequential(
    nn.Linear(3, 4),
    nn.Tanh(),
    nn.Linear(4, 4),
    nn.ReLU(),
    nn.Linear(4, 2),
    nn.Softmax(dim=-1)
).to(DEVICE)

# x = torch.tensor([1, 2, 3], dtype=torch.float)

# print(model.forward(x))

X = torch.randn(10, 3).to(DEVICE)
print(model(X))

# 查看模型参数
params = model.named_parameters()
for param in params:
    print(param)


# 使用summary查看模型信息
summary(model=model, input_size=(3,), batch_size=10, device=DEVICE)