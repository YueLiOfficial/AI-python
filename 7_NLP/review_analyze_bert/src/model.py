import torch
from torch import nn
from transformers import AutoModel
from config import *

class AnalyzeModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained(str(PRETRAINED_DIR_PATH / "bert-base-chinese"))

        self.linear = nn.Linear(self.bert.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)

        cls_output = bert_output.last_hidden_state[:, 0, :]

        output = self.linear(cls_output)

        return output