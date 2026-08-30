import torch
import torch.nn as nn
import torchsummary as summary

# 自定义模型需要继承nn.Module类
class MyModel(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 定义三个层
        # 输入层->第一隐藏层
        self.linear1 = nn.Linear(3, 4)
        # 第一隐藏层->第二隐藏层
        self.linear2 = nn.Linear(4, 4)
        # 第二隐藏层->输出层
        self.out = nn.Linear(4, 2)

    # 前向传播
    def forward(self, x):
        x = self.linear1(x)
        x = torch.tanh(x)

        x = self.linear2(x)
        x = torch.relu(x)

        x = self.out(x)
        y = torch.softmax(x, dim=-1)

        return y

if __name__ == "__main__":
    DEVICE = "cuda" if torch.cuda.is_available else "cpu"

    model = MyModel().to(DEVICE)

    # x = torch.tensor([1, 2, 3], dtype=torch.float)

    # print(model.forward(x))

    X = torch.randn(10, 3).to(DEVICE)
    print(model(X))

    # 查看模型参数
    # params = model.named_parameters()
    # for param in params:
    #     print(param)
    

    # 使用summary查看模型信息
    summary.summary(model=model, input_size=(3,), batch_size=10, device=DEVICE)
