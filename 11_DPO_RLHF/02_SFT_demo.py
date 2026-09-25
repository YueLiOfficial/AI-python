from dataclasses import dataclass
import torch
from transformers import PreTrainedTokenizerFast
from typing import List
import numpy as np
from transformers import AutoModelForCausalLM
from torch import optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from transformers import AutoTokenizer
from datasets import load_dataset

@dataclass
class SFTConfig:
    train_data_size: int = 20000
    
    lr: float = 3e-5
    batch_size: int = 2
    warmup_ratio: float = 0.1

    test_data_size: int = 500
    test_iter: int = 100
    log_iter: int =100

    log_dir = "./logs/02_sft_demo"
    save_dir:str = "./finetuned/02_sft_demo"

device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

def get_train_data(sft_cfg: SFTConfig):
    train_data = load_dataset("./data/ultrachat_200k")["train_sft"]

    token_ids_list = []

    for i in range(sft_cfg.train_data_size):
        messages_list = train_data[i]["messages"]

        token_ids = tokenizer.apply_chat_template(messages_list, tokenize=True, truncation=True, max_length = 2400)["input_ids"]

        token_ids_list.append(token_ids)

    return token_ids_list

def get_test_data(sft_cfg: SFTConfig):
    test_data = load_dataset("./data/ultrachat_200k")["test_sft"]

    total_test_ids = []

    for i in range(sft_cfg.test_data_size):
        messages_list = test_data[i]["messages"]
        input_ids = tokenizer.apply_chat_template(messages_list, tokenize=True)["input_ids"]

        total_test_ids.append(input_ids)

    return total_test_ids

def create_answer_mask(labels,tokenizer:PreTrainedTokenizerFast):
    """
    创建answer mask，从labels当中找出assistant回答的部分，然后输出一个与labels相同shape的mask
    """
    # 构建answer mask，输入的labels为批量 tokenize之后的数据，对于每一条数据，查找当中assistant回答的部分，将其设置为1

    # 1. 构造一个和labels相同shape的全0矩阵
    answer_mask = torch.zeros_like(labels)

    # 2、找到<|im_end|> 所对应的token_id
    eos_token_id = tokenizer.encode("<|im_end|>")[0]

    # 3、遍历labels中的每一个样本
    # labels.shape: batch_size, seq_len
    for idx,ids in enumerate(labels):
        # 3.1、获取到所有的eos_position
        eos_position:List = torch.where(ids == eos_token_id)[0].tolist()
        # 3.2、解析获得user_ends和assistant_ends
        user_ends,assistant_ends = _parse_conversation_turns(eos_position)
        # 3.3、设置answer mask
        _set_answer_masks(answer_mask[idx],user_ends,assistant_ends)   
    
    # 4、结果返回:
    return answer_mask

def _parse_conversation_turns(eos_positions:List[int]):
    """
    输入eos_positions，输出user所对应的end位置和assistant所对应的end位置。

    以下面的对话为例：
    <|im_start|>user
    什么是习惯？<|im_end|>
    <|im_start|>assistant
    习惯是指在一定时间内重复执行的行为。<|im_end|>
    <|im_start|>user
    如何培养一个习惯<|im_end|>
    <|im_start|>assistant
    21天培养法，每天坚持xxx<|im_end|>

    假设第一个eos_token_id index为10，第二个为15，第三个为20，第四个为25
    那么输入的eos_token_id为：[10,15,20,25]
    user_turns为从第一个开始取，每隔一个取一次，assistant_turns为从第二个开始取，每隔一个取一次。

    输出结果为：
        user_turns:[10,20]
        assistant_ends:[15,25]
    """

    use_ends = [pos for pos in eos_positions[::2]]
    assistant_ends = [pos for pos in eos_positions[1::2]]

    return use_ends,assistant_ends

def _set_answer_masks(mask,user_ends,assistant_ends):
    """
    将mask当中，assistant回答的部分，设置为1（原地修改，不返回新的mask），其余部分保持为0

    以下面的对话为例：
    <|im_start|>user
    什么是习惯？<|im_end|>
    <|im_start|>assistant
    习惯是指在一定时间内重复执行的行为。<|im_end|>
    <|im_start|>user
    如何培养一个习惯<|im_end|>
    <|im_start|>assistant
    21天培养法，每天坚持xxx<|im_end|>

    假设第一个eos_token_id index为10，第二个为15，第三个为20，第四个为25
    那么user_turns:[10,20]，assistant_ends:[15,25]

    
    要想获取到assistant的回答的起始位置，就需要跳过<|im_end|>, \n, <|im_start|>,assistant , \n 这5个token
    要想获取到assistant的回答的结束位置，需要将<|im_end|>也包括进去，又因为列表切片是左闭右开的，所以需要向后移动一位
    """
    num_user_turns = len(user_ends)
    num_assistant_turns = len(assistant_ends)
    # 多轮对话没有被截断或者最后一轮整个assistant回答被截断，user轮数和assistant轮数一致
    if num_user_turns == num_assistant_turns:
        for user_end,assistant_end in zip(user_ends,assistant_ends):
            answer_start = user_end + 5
            answer_end = assistant_end + 1
            mask[answer_start:answer_end] = 1

    # 最后一轮，assistant回答被部分截断，此时user轮数比assistant轮数多一轮
    elif num_user_turns == num_assistant_turns + 1:
        for user_end,assistant_end in zip(user_ends[:-1],assistant_ends):
            answer_start = user_end + 5
            answer_end = assistant_end + 1
            mask[answer_start:answer_end] = 1
        
        # 处理最后一轮被截断的助手回答
        last_user_end = user_ends[-1] 
        last_answer_start = last_user_end + 5
        mask[last_answer_start:] = 1

# output_logits: shape [batch_size, seq_len, vocab_size]
# labels: shape [batch_size, seq_len]
# assistant_answer_mask: shape [batch_size, seq_len]
def compute_loss(output_logits, labels, assistant_answer_mask):
    log_probs = torch.nn.functional.log_softmax(output_logits, dim=-1)

    label_probs = torch.gather(
        input=log_probs, 
        dim=-1, 
        index=labels.unsqueeze(-1)
    ).squeeze(-1)

    mask_label_probs = label_probs * assistant_answer_mask

    return (-1) * (mask_label_probs.sum() / assistant_answer_mask.sum())

def cosine_decay(batch, total_batch, lr, warmup_ratio):
    warmup_batch = warmup_ratio * total_batch

    if batch < warmup_batch:
        k = lr / warmup_batch
        return k * (batch + 1)
    else:
        progress = (batch - warmup_batch) / (total_batch - warmup_batch)

        decay_value = (np.cos(progress * np.pi) + 1) * 0.5

        return decay_value * lr

def get_eval_loss(model, test_data, sft_cfg: SFTConfig):
    model.eval()

    total_loss_list = []

    total_batchs = (len(test_data) + (sft_cfg.batch_size - 1)) // sft_cfg.batch_size

    with torch.no_grad():
        for batch in range(total_batchs):
            batch_data = test_data[batch * sft_cfg.batch_size: (batch  + 1) * sft_cfg.batch_size]

            max_len = max([len(seq) for seq in batch_data])
            for seq in batch_data:
                padding_len = max_len - len(seq)
                seq.extend([tokenizer.pad_token_id] * padding_len)

            batch_data = torch.tensor(batch_data, dtype=torch.long, device=device)

            input_ids = batch_data[:, : -1]
            labels = batch_data[:, 1:]
            assistant_answer_mask = create_answer_mask(labels, tokenizer)

            # 前向传播
            output_logits = model(input_ids).logits

            # 计算损失
            cur_loss = compute_loss(output_logits, labels, assistant_answer_mask)

            total_loss_list.append(cur_loss.item())

    return sum(total_loss_list) / len(total_loss_list)

def train(sft_cfg: SFTConfig):
    """
    1、初始化模型，优化器等状态    
    2、张量准备：遍历数据，对input_ids进行padding，获取input_ids以及labels， assistant_answer_mask； 
    3、模型前向传播：前向传播，获取lm head logits； 
    4、损失计算：对logits和labels，使用损失函数，计算当前batch损失； 
    5、反向传播：反向传播，计算梯度； 
    6、调度学习率，做参数更新：使用余弦调度器去调度学习率，再使用特定的优化器（例如AdamW）对参数进行更新。
    """
    
    model = AutoModelForCausalLM.from_pretrained("./model/Qwen3-0.6B-Base")
    model.to(device)

    optimizer = optim.AdamW(model.parameters(), sft_cfg.lr)

    # 获取数据
    token_ids = get_train_data(sft_cfg)

    test_ids = get_test_data(sft_cfg)

    batch_nums = (len(token_ids) + sft_cfg.batch_size - 1) // sft_cfg.batch_size

    total_loss = 0

    writer = SummaryWriter(sft_cfg.log_dir)
    
    for batch in tqdm(range(batch_nums), desc="训练: "):
        model.train()
        
        # 获取每批数据 [0:4] [4:8] [8:12]
        batch_data = token_ids[batch * sft_cfg.batch_size: (batch + 1) * sft_cfg.batch_size]

        #padding 
        max_len = max([len(seq) for seq in batch_data])
        for seq in batch_data:
            padding_len = max_len - len(seq)
            seq.extend([tokenizer.pad_token_id] * padding_len)

        # 转换为tensor
        batch_data = torch.tensor(batch_data, dtype=torch.long, device=device)

        input_ids = batch_data[:, : -1]
        labels = batch_data[:, 1:]
        assistant_answer_mask = create_answer_mask(labels, tokenizer)

        # 向前传播
        output_logits = model(input_ids).logits

        # 计算损失
        loss = compute_loss(output_logits, labels, assistant_answer_mask)

        total_loss += loss.item()

        # 反向传播
        loss.backward()

        lr = cosine_decay(batch, batch_nums, sft_cfg.lr, sft_cfg.warmup_ratio)
        writer.add_scalar("lr", lr, batch)

        optimizer.param_groups[0]["lr"] = lr

        # 计算梯度
        optimizer.step()

        optimizer.zero_grad()

        should_eval = batch % sft_cfg.test_iter == 0
        if should_eval:
            eval_loss = get_eval_loss(model, test_ids, sft_cfg)

            writer.add_scalar("eval_loss", eval_loss, batch)

        should_log = batch % sft_cfg.log_iter == 0 and batch != 0
        if should_log:
            train_log_loss = total_loss / sft_cfg.log_iter

            writer.add_scalar("train_loss", train_log_loss, batch)

            total_loss = 0

    model.save_pretrained(sft_cfg.save_dir)
    tokenizer.save_pretrained(sft_cfg.save_dir)

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("./model/Qwen3-0.6B-Base")

    sft_cfg = SFTConfig()

    train(sft_cfg)