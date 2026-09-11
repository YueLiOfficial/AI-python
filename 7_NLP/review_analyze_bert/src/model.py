import torch
from torch import nn
from transformers import AutoModel
from config import *

class AnalyzeModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.bert = AutoModel.from_pretrained(str(PRETRAINED_DIR_PATH / "bert-base-chinese"))

        self.linear = nn.Linear(self.bert.config.hidden_size, 1)

    def forward(self, inputs_ids, attention_mask):
        bert_output = self.bert(inputs_ids=inputs_ids, attention_mask=attention_mask)

        output = self.linear(bert_output.last_hidden_step[:, [0], :])

        return output