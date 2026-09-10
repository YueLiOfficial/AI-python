import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from config import *

class TranslationDataset(Dataset):
    def __init__(self, data_path):
        super().__init__()

        self.data = pd.read_json(data_path, lines=True).to_dict(orient="records")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        zh_data = torch.tensor(self.data[index]["zh"])
        en_data = torch.tensor(self.data[index]["en"])

        return zh_data, en_data

def collate_fn(batch):
    zh_data = [data[0] for data in batch]
    en_data = [data[1] for data in batch]

    zh_batch = pad_sequence(zh_data, batch_first=True)
    en_batch = pad_sequence(en_data, batch_first=True)

    return zh_batch, en_batch

def get_dataloader(train=True):
    path = TRAIN_DATA_FILE if train else TEST_DATA_FILE

    dataset = TranslationDataset(path)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=train, collate_fn=collate_fn)

    return loader

if __name__ == "__main__":
    train_loader = get_dataloader()

    for zh, en in train_loader:
        print(zh.shape)
        print(en.shape)
        break
