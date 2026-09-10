import torch
from torch import nn


class Attention(nn.Module):
    # 初始化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # 前向传播
    def forward(self, decoder_hidden, encoder_outputs: torch.Tensor):
        # 计算相关性 decoder_hidden: (N, L_dec, hidden_size) encoder_output: (N, L_enc, hidden_size)
        score = decoder_hidden @ encoder_outputs.permute(0, 2, 1) # 输出 (N, L_dec, L_enc)

        # 计算注意力权重
        attn_weights = torch.softmax(score, dim=-1) # 输出 (N, L_dec, L_enc)

        # 计算上下文向量
        vectors = attn_weights @ encoder_outputs # 输出 (N, L_dec, hidden_size)

        # 解码信息融合
        context_matrix = torch.cat((vectors, decoder_hidden), dim=-1) # (N, L_dec, 2 * hidden_size)

        return context_matrix

if __name__ == "__main__":
    # 定义参数
    N = 32
    L_enc = 12
    L_dec = 15
    hidden_size = 128

    decoder_hidden = torch.randn(N, L_dec, hidden_size)
    encoder_output = torch.randn(N, L_enc, hidden_size)

    attn = Attention()

    output = attn(decoder_hidden, encoder_output)

    print(output.shape)