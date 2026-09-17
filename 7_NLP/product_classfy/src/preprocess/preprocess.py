from tkinter.font import names

from sqlalchemy.util import column_dict
from transformers import AutoTokenizer
from datasets import load_dataset, Features, Value, ClassLabel
from common.config import *

def preprocess():
    # 1. 加载数据
    dataset_dict = load_dataset(
        "csv",
        delimiter="\t",
        data_files={
            "train": str(RAW_DATA_DIR / "train.txt"),
            "test": str(RAW_DATA_DIR / "test.txt"),
            "valid": str(RAW_DATA_DIR / "valid.txt")
        },
        features=Features({
            "label": Value("string"),
            "text_a": Value("string")
        })
    )

    # 2. 将label保存下来并转换为标签编码
    label_list = sorted(set(dataset_dict["train"]["label"]))

    with open(LABEL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(label_list))

    dataset_dict = dataset_dict.cast_column("label", ClassLabel(names=label_list))

    # 3. 创建分词器，对数据进行分词
    tokenizer = AutoTokenizer.from_pretrained(str(PRETRAINED_MODEL))

    def tokenize(batch):
        encoded = tokenizer(
            batch["text_a"],
            truncation=True
        )

        batch["input_ids"] = encoded["input_ids"]
        batch["attention_mask"] = encoded["attention_mask"]
        batch["token_type_ids"] = encoded["token_type_ids"]

        return batch

    dataset_dict = dataset_dict.map(
        tokenize,
        batched=True
    )

    # 保存处理后的数据
    dataset_dict["train"].save_to_disk(str(PREPROCESSED_DATA_DIR / "train"))
    dataset_dict["test"].save_to_disk(str(PREPROCESSED_DATA_DIR / "test"))
    dataset_dict["valid"].save_to_disk(str(PREPROCESSED_DATA_DIR / "valid"))


if __name__ == "__main__":
    preprocess()