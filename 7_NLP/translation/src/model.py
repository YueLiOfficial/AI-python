import torch
from torch import nn
import math
from config import *

class PositionalEncodingModel(nn.Module):
    def __init__(self, max_len=MAX_LEN, dim=D_MODEL):
        super().__init__()

        # 定义位置编码矩阵
        pe = torch.zeros(max_len, dim)

        # 预计算
        for pos in range(max_len):
            for i in range(0, dim, 2):
                pe[pos, i] = math.sin(pos / 10000 ** (i / dim))
                pe[pos, i + 1] = math.cos(pos / 10000 ** (i / dim))

        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x +self.pe[0: x.shape[1]]
        return x
        
class TranslationModel(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size):
        super().__init__()

        #两个embedding层
        self.src_embedding = nn.Embedding(src_vocab_size, D_MODEL)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, D_MODEL)

        # 一个位置编码层
        self.positional = PositionalEncodingModel()

        # transformer层
        self.transformer = nn.Transformer(D_MODEL, N_HEAD, NUM_ENCODER_LAYERS, NUM_DECODER_LAYERS, batch_first=True)

        self.linear = nn.Linear(D_MODEL, tgt_vocab_size)

    def forward(self, src_data, tgt_data, tgt_mask, src_key_padding_mask, tgt_key_padding_mask):
        # 编码
        memory = self.encode(src_data, src_key_padding_mask)
        output = self.decode(tgt_data, memory, tgt_mask, tgt_key_padding_mask, src_key_padding_mask)

        return output

    def encode(self, src_data, src_key_padding_mask):
        embed = self.src_embedding(src_data)

        pos_data = self.positional(embed)

        memory = self.transformer.encoder(pos_data, src_key_padding_mask = src_key_padding_mask)

        return memory

    def decode(self, tgt_data, memory, tgt_mask, tgt_key_padding_mask, memory_key_padding_mask):
        embed = self.tgt_embedding(tgt_data)

        pos_data = self.positional(embed)

        output = self.transformer.decoder(pos_data, memory = memory, tgt_mask = tgt_mask,
            tgt_key_padding_mask = tgt_key_padding_mask, 
            memory_key_padding_mask = memory_key_padding_mask
        )

        output = self.linear(output)

        return output
