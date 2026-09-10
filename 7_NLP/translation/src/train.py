from dataset import get_dataloader
import torch
from torch import nn, optim
from model import TranslationModel
from tokenizer import ZhTokenizer, EnTokenizer
from config import *

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 获取训练数据
    loader = get_dataloader(train=True)

    # 获取词表大小
    zh_tokenizer = ZhTokenizer.from_vocab(ZH_VOCAB_FILE)
    en_tokenizer = EnTokenizer.from_vocab(EN_VOCAB_FILE)

    model = TranslationModel(zh_tokenizer.vocab_size, en_tokenizer.vocab_size)
    model.to(device)

    # 定义损失函数和优化器
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = optim.Adam(model.parameters(), LR)

    # 开始训练
    min_loss = float("inf")

    for epoch in range(EPOCHS):
        print(f"正在训练{epoch + 1}/{EPOCHS}...")
        loss = train_one_epoch(loader, model, loss_fn, optimizer, device)
        print(f"训练完成, 损失为{loss}")

        if loss < min_loss:
            min_loss = loss
            torch.save(model, MODEL_FILE)

def train_one_epoch(dataloader, model, loss_fn, optimizer, device):
    total_loss = 0

    model.train()
    for inputs, targets in dataloader:
        inputs, targets = inputs.to(device), targets.to(device)

        decoder_inputs = targets[:, : -1]
        decoder_targets = targets[:, 1: ]

        # 定义掩码
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(decoder_inputs.shape[1]).bool().to(device)
        src_key_padding_mask = (inputs == 0)
        tgt_key_padding_mask = (decoder_inputs == 0)

        # 前向传播
        output = model(inputs, decoder_inputs, tgt_mask, src_key_padding_mask, tgt_key_padding_mask)

        # 计算损失
        loss = loss_fn(output.transpose(1, 2), decoder_targets)

        # 反向传播
        loss.backward()

        # 更新参数
        optimizer.step()

        # 清空梯度
        optimizer.zero_grad()

        total_loss += loss.item()

    return total_loss / len(dataloader)

if __name__ == "__main__":
    train()
