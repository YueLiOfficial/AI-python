import torch
from torch import nn, optim
from model import AnalyzeModel
from preprocess import get_loader
from tqdm import tqdm
from config import *

def train():
    device = torch.device("cuda" if torch.cuda.is_available() 
                          else "mps" if torch.backends.mps.is_available()
                          else "cpu")

    model = AnalyzeModel().to(device)

    train_dataloader, test_dataloader = get_loader()

    # 定义损失函数和优化器
    loss_fn = nn.BCEWithLogitsLoss()

    optimizer = optim.Adam(model.parameters(), lr=LR)

    min_loss = float("inf")
    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
    
        for batch in tqdm(train_dataloader, desc="训练"):
            targets = batch.pop("label").to(device=device, dtype=torch.float).reshape(-1, 1)
            inputs = {k: v.to(device) for k, v in batch.items()}

            outputs = model(**inputs)

            loss = loss_fn(outputs, targets)

            loss.backward()

            optimizer.step()

            optimizer.zero_grad()

            total_loss += loss.item()

        avg_loss = total_loss / len(train_dataloader)

        if avg_loss < min_loss:
            torch.save(model, MODELS_DIR_PATH / "best_model.pt")
            min_loss = avg_loss

        print(f"第{epoch + 1}/{EPOCHS}轮, loss = {avg_loss}")



if __name__ == "__main__":
    train()