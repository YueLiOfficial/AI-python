import pandas as pd
import torch
from tokenizer import ZhTokenizer, EnTokenizer
from sklearn.model_selection import train_test_split
import json
from config import *

def preprocess():
    print("开始进行数据预处理")

    data_df = pd.read_csv(RAW_DATA_FILE, sep='\t', header=None, names=["en", "zh"], usecols=[0, 1])

    data_df.dropna(inplace=True)

    # 划分数据集
    train_df, test_df = train_test_split(data_df, test_size=0.2, random_state=42)

    # 创建词表
    EnTokenizer.create_vocab(train_df["en"], EN_VOCAB_FILE)
    ZhTokenizer.create_vocab(train_df["zh"], ZH_VOCAB_FILE)

    # 创建分词器
    zh_tokenizer = ZhTokenizer.from_vocab(ZH_VOCAB_FILE)
    en_tokenizer = EnTokenizer.from_vocab(EN_VOCAB_FILE)

    # 分词并编码
    zh_encode_fn = lambda text: zh_tokenizer.encode(text)
    en_encode_fn = lambda text: en_tokenizer.encode(text, AddSosEos=True)
    train_df["zh"] = train_df["zh"].apply(zh_encode_fn)
    train_df["en"] = train_df["en"].apply(en_encode_fn)
    test_df["zh"] = test_df["zh"].apply(zh_encode_fn)
    test_df["en"] = test_df["en"].apply(en_encode_fn)

    # 保存编码
    with open(TRAIN_DATA_FILE, "w", encoding="utf-8") as f:
        for zh_id, en_id in zip(train_df["zh"], train_df["en"]):
            data = {"zh": zh_id, "en": en_id}

            f.write(json.dumps(data, ensure_ascii=False) + '\n')

    with open(TEST_DATA_FILE, "w", encoding="utf-8") as f:
        for zh_id, en_id in zip(test_df["zh"], test_df["en"]):
            data = {"zh": zh_id, "en": en_id}

            f.write(json.dumps(data, ensure_ascii=False) + '\n')

    print("数据预处理完毕")

if __name__ == "__main__":
    preprocess()
