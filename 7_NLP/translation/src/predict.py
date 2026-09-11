import torch
from torch import nn
from model import TranslationModel
from tokenizer import ZhTokenizer, EnTokenizer
from dataset import get_dataloader
from config import *

def predict(model, text, src_tokenizer, tgt_tokenizer, device):
    ids = src_tokenizer.encode(text)

    inputs = torch.tensor([ids]).to(device)

    # 编码
    src_key_padding_mask = (inputs == src_tokenizer.pad_id)
    memory = model.encode(inputs, src_key_padding_mask)

    # 解码
    # 定义输入起始数据<sos>
    decoder_inputs = torch.tensor([[tgt_tokenizer.sos_id]]).to(device)

    # 循环进行自回归生成
    for _ in range(MAX_LEN):
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(decoder_inputs.shape[1]).bool().to(device)
        tgt_key_padding_mask = (decoder_inputs == tgt_tokenizer.pad_id)

        output = model.decode(decoder_inputs, memory, tgt_mask, tgt_key_padding_mask, src_key_padding_mask)

        this_token_id = torch.argmax(output[:, -1], dim=-1)

        decoder_inputs = torch.cat((decoder_inputs, this_token_id.unsqueeze(1)), dim=-1)

        if this_token_id == tgt_tokenizer.eos_id:
            break

    
    sentence = tgt_tokenizer.decode(decoder_inputs[0, 1: -1].tolist())

    print(sentence)

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() 
                          else "mps" if torch.backends.mps.is_available() else "cpu")

    text = "你叫什么名字?"

    src_tokenizer = ZhTokenizer.from_vocab(ZH_VOCAB_FILE)
    tgt_tokenizer = EnTokenizer.from_vocab(EN_VOCAB_FILE)

    model = torch.load(MODEL_FILE, map_location=device, weights_only=False).to(device)

    predict(model, text, src_tokenizer, tgt_tokenizer, device)
