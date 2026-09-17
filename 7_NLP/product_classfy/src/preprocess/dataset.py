from common.config import *
import torch
from torch.utils.data import DataLoader
from datasets import load_from_disk
from transformers import DataCollatorWithPadding, AutoTokenizer

def get_dataset(type="train"):
    dataset = load_from_disk(str(PREPROCESSED_DATA_DIR / type))

    dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "token_type_ids", "label"])

    return dataset

def get_loader(tokenizer, type="train"):
    dataset = get_dataset(type)

    collate_fn = DataCollatorWithPadding(tokenizer)

    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=type=="train", collate_fn=collate_fn)

    return dataloader

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)

    dataloader = get_loader(tokenizer)

    for batch in dataloader:
        for k, v in batch.items():
            print(k, v.shape)

        break
