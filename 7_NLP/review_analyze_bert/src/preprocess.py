from datasets import load_dataset, load_from_disk
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
import os
from config import *

def preprocess():
    if os.path.exists(PROCESSED_DIR_PATH / "train") and os.path.exists(PROCESSED_DIR_PATH / "test"):
        print("数据已存在")
        return 

    dataset = load_dataset("csv", data_files=str(RAW_DATA_PATH))["train"]

    # 数据清洗
    dataset = dataset.filter(
        lambda x: x["review"] is not None 
        and x["review"].strip() != "" and x["label"] in [0, 1]
    )

    datast_dict = dataset.train_test_split(test_size=0.2)

    train_dataset = datast_dict["train"]
    test_dataset = datast_dict["test"]

    tokenizer = AutoTokenizer.from_pretrained(str(PRETRAINED_DIR_PATH / "bert-base-chinese"))

    def tokenize(batch):
        encoded = tokenizer(
            batch["review"],
            padding="max_length",
            truncation=True,
            max_length=MAX_LEN
        )

        batch["input_ids"] = encoded["input_ids"]
        batch["attention_mask"] = encoded["attention_mask"]
        batch["token_type_ids"] = encoded["token_type_ids"]

        return batch

    train_dataset = train_dataset.map(tokenize, batched=True)
    test_dataset = test_dataset.map(tokenize, batched=True)

    train_dataset = train_dataset.remove_columns(["cat", "review"])
    test_dataset = test_dataset.remove_columns(["cat", "review"])

    train_dataset.save_to_disk(str(PROCESSED_DIR_PATH / "train"))
    test_dataset.save_to_disk(str(PROCESSED_DIR_PATH / "test"))

def get_loader():
    train_dataset = load_from_disk(str(PROCESSED_DIR_PATH / "train"))
    test_dataset = load_from_disk(str(PROCESSED_DIR_PATH / "test"))

    train_dataset.set_format(
        type="torch",
        columns=["input_ids", "label", "attention_mask", "token_type_ids"]
    )

    test_dataset.set_format(
        type="torch",
        columns=["input_ids", "label", "attention_mask", "token_type_ids"]
    )

    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

    return train_dataloader, test_dataloader
    

if __name__ == "__main__":
    preprocess()
    train_dataloader, test_dataloader = get_loader()

    for batch in train_dataloader:
        print(batch)
        break