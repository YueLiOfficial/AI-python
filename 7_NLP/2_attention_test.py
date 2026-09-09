import torch
from torch import nn

class Attention(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self, decoder_hidden, encoder_outputs):
        # 计算相关度 decoder_hidden: (N, L_dec, hiddensize), encoder_outputs: (N, L_enc, hiddensize)
        score = decoder_hidden @ encoder_outputs.permute(0, 2, 1) # (N, L_dec, L_enc)

        # 计算注意力权重 
        weights = torch.softmax(score, dim=-1)

        # 计算上下文向量  (N, L_dec, hiddensize)
        vectors = weights @ encoder_outputs

        # 解码信息融合 (N, L_dec, 2 * hiddensize)
        matrix = torch.cat((vectors, decoder_hidden), dim=-1)

        return matrix

attn = Attention()

N = 32
L_enc = 15
L_dec = 12
hidden_size = 512

encoder_outputs = torch.randn(N, L_enc, hidden_size)
decoder_hidden = torch.randn(N, L_dec, hidden_size)

output = attn(decoder_hidden, encoder_outputs)

print(output.shape)
