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
class DPOConfig:
    train_data_size: int = 20000
    
    lr: float = 3e-6
    batch_size: int = 2
    warmup_ratio: float = 0.1

    beta: float = 0.1

    test_data_size: int = 500
    test_iter: int = 100
    log_iter: int =100

    log_dir = "./logs/03_dpo_demo"
    save_dir:str = "./finetuned/03_dpo_demo"

# 获取训练数据集
def get_train_data(dpo_cfg: DPOConfig):
    train_data = load_dataset("./data/ultrafeedback_binarized")["train_prefs"]

    chosen_data_list = []
    rejected_data_list = []

    for i in range(dpo_cfg.train_data_size):
        chosen_data = train_data[i]["chosen"]
        rejected_data = train_data[i]["rejected"]

        chosen_data_list.append(chosen_data)
        rejected_data_list.append(rejected_data)

    chosen_token_ids = tokenizer.apply_chat_template(chosen_data_list, tokenize=True)["input_ids"]
    rejected_token_ids = tokenizer.apply_chat_template(rejected_data_list, tokenize=True)["input_ids"]

    return chosen_token_ids, rejected_token_ids

# 获取验证数据集
def get_eval_data(dpo_cfg: DPOConfig):
    eval_data = load_dataset("./data/ultrafeedback_binarized")["test_prefs"]

    chosen_data_list = []
    rejected_data_list = []

    for i in range(dpo_cfg.test_data_size):
        chosen_data = eval_data[i]["chosen"]
        rejected_data = eval_data[i]["rejected"]

        chosen_data_list.append(chosen_data)
        rejected_data_list.append(rejected_data)

    chosen_token_ids = tokenizer.apply_chat_template(chosen_data_list, tokenize=True)["input_ids"]
    rejected_token_ids = tokenizer.apply_chat_template(rejected_data_list, tokenize=True)["input_ids"]

    return chosen_token_ids, rejected_token_ids

# 获取assistant answer mask
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

def compute_log_prob(output_logits, labels: torch.Tensor, assistant_answer_mask):
    output_log_prob = torch.nn.functional.log_softmax(output_logits, dim=-1)

    output_token_log_prob = torch.gather(
        input=output_log_prob,
        dim=-1,
        index=labels.unsqueeze(-1)
    ).squeeze(-1)

    # shape: [batch_size, seq_len]
    masked_output_log_prob = output_token_log_prob * assistant_answer_mask

    log_prob = masked_output_log_prob.sum(-1)

    return log_prob

# 损失函数
def compute_loss(train_model_chosen_log_prob, train_model_rejected_log_prob, ref_model_chosen_log_prob, ref_model_rejected_log_porb, beta):
    # 每一个log_prob的shape都是(batch_size, )
    margin = (train_model_chosen_log_prob - train_model_rejected_log_prob) - (ref_model_chosen_log_prob - ref_model_rejected_log_porb)

    # 整批数据中每个样本的loss
    # loss的shape (batch_size, )
    loss = (-1) * torch.nn.functional.logsigmoid((beta * margin))

    # 样本平均损失 
    avg_loss = loss.mean()

    return avg_loss

# cosine学习率衰减
def cosine_decay(batch, total_batch, lr, warmup_ratio):
    warmup_batch = total_batch * warmup_ratio

    if batch < warmup_batch:
        k = lr / warmup_batch
        return k * (batch + 1)
    else:
        progress = (batch - warmup_batch) / (total_batch - warmup_batch)

        lr_decay = (np.cos(progress * np.pi) + 1) * 0.5

        return lr * lr_decay

# 模型评估
def get_eval_loss(train_model, ref_model, chosen_ids, rejected_ids, dpo_cfg: DPOConfig):
    # 分批
    total_batch = (len(chosen_ids) + dpo_cfg.batch_size - 1) / dpo_cfg.batch_size

    for batch in range(total_batch):
        # 获取每一批数据
        chosen_data = chosen_ids[batch * dpo_cfg.batch_size: (batch + 1) * dpo_cfg.batch_size]
        rejected_data = rejected_ids[batch * dpo_cfg.batch_size: (batch + 1) * dpo_cfg.batch_size]

        # padding
        chosen_max_len = max([len(seq) for seq in chosen_data])
        for seq in chosen_data:
            padding_len = chosen_max_len - len(seq)
            seq.append([tokenizer.pad_token_id] * padding_len)

        rejected_max_len = max([len(seq) for seq in rejected_data])
        for seq in rejected_data:
            padding_len = rejected_max_len - len(seq)
            seq.append([tokenizer.pad_token_id] * padding_len)

        # 转换为张量
        chosen_data = torch.tensor(chosen_data, dtype=torch.long, device=torch.device("cuda"))
        rejected_data = torch.tensor(rejected_data, dtype=torch.long, device=torch.device("cuda"))

        # 获取input_ids, labels, answer_mmask
        chosen_input_ids = chosen_data[:, : -1]
        chosen_labels = chosen_data[:, 1:]
        chosen_answer_mask = create_answer_mask(chosen_labels, tokenizer)

        rejected_input_ids = rejected_data[:, : -1]
        rejected_labels = rejected_data[:, 1:]
        rejected_answer_mask = create_answer_mask(rejected_labels, tokenizer)

        total_loss_list = []

        # 前向传播
        train_model.eval()
        ref_model.eval()
        with torch.no_grad():
            train_chosen_output_logits = train_model(chosen_input_ids).logits
            train_rejected_output_logits = train_model(rejected_input_ids).logits

            ref_chosen_output_logits = ref_model(chosen_input_ids).logits
            ref_rejected_output_logits = ref_model(rejected_input_ids).logits

            # 计算log_prob
            train_chosen_log_prob = compute_log_prob(train_chosen_output_logits, chosen_labels, chosen_answer_mask)
            train_rejected_log_prob = compute_log_prob(train_rejected_output_logits, rejected_labels, rejected_answer_mask)

            ref_chosen_log_prob = compute_log_prob(ref_chosen_output_logits, chosen_labels, chosen_answer_mask)
            ref_rejected_log_prob = compute_log_prob(ref_rejected_output_logits, rejected_labels, rejected_answer_mask)

            # 计算损失
            loss = compute_loss(train_chosen_log_prob, 
                                train_rejected_log_prob, 
                                ref_chosen_log_prob, 
                                ref_rejected_log_prob,
                                dpo_cfg.beta
                    )

            total_loss_list.append(loss.item())

    return sum(total_loss_list) / len(total_loss_list)

# 模型训练
def train(dpo_cfg: DPOConfig):
    device = torch.device("cuda")

    # 定义模型
    train_model = AutoModelForCausalLM.from_pretrained("./finetuned/02_sft_demo").to(device)
    ref_model = AutoModelForCausalLM.from_pretrained("./finetuned/02_sft_demo").to(device)

    # 定义优化器
    optimizer = optim.AdamW(train_model.parameters(), dpo_cfg.lr)

    # 获取训练数据
    train_chosen_ids, train_rejected_ids = get_train_data(dpo_cfg)

    # 获取验证数据
    eval_chosen_ids, eval_rejected_ids = get_eval_data(dpo_cfg)

    total_batch = (len(train_chosen_ids) + dpo_cfg.batch_size - 1) // dpo_cfg.batch_size

    writer = SummaryWriter(dpo_cfg.log_dir)

    total_loss = 0

    for batch in tqdm(range(total_batch), desc="[训练]"):
        train_model.train()
        ref_model.eval()

        # 获取每个batch的数据
        train_chosen_data = train_chosen_ids[batch * dpo_cfg.batch_size: (batch + 1) * dpo_cfg.batch_size]
        train_rejected_data = train_rejected_ids[batch * dpo_cfg.batch_size: (batch + 1) * dpo_cfg.batch_size]

        # padding
        chosen_max_len = max([len(seq) for seq in train_chosen_data])
        for seq in train_chosen_data:
            padding_len = chosen_max_len - len(seq)
            seq.extend([tokenizer.pad_token_id] * padding_len)

        rejected_max_len = max([len(seq) for seq in train_rejected_data])
        for seq in train_rejected_data:
            padding_len = rejected_max_len - len(seq)
            seq.extend([tokenizer.pad_token_id] * padding_len)

        # 转换为张量
        train_chosen_data = torch.tensor(train_chosen_data, dtype=torch.long, device=device)
        train_rejected_data = torch.tensor(train_rejected_data, dtype=torch.long, device=device)

        # 获取input_ids, labels, answer_mask
        train_chosen_input_ids = train_chosen_data[:, : -1]
        train_chosen_labels = train_chosen_data[:, 1:]
        train_chosen_mask = create_answer_mask(train_chosen_labels, tokenizer)

        train_rejected_input_ids = train_rejected_data[:, : -1]
        train_rejected_labels = train_rejected_data[:, 1:]
        train_rejected_mask = create_answer_mask(train_rejected_labels, tokenizer)

        # 前向传播
        train_chosen_output_logits = train_model(train_chosen_input_ids).logits
        train_rejected_output_logits = train_model(train_rejected_input_ids).logits

        with torch.no_grad():
            ref_chosen_output_logits = ref_model(train_chosen_input_ids).logits
            ref_rejected_output_logits = ref_model(train_rejected_input_ids).logits

        # 计算log_porb
        train_chosen_log_prob= compute_log_prob(train_chosen_output_logits, train_chosen_labels, train_chosen_mask)
        train_rejected_log_prob= compute_log_prob(train_rejected_output_logits, train_rejected_labels, train_rejected_mask)

        ref_chosen_log_prob= compute_log_prob(ref_chosen_output_logits, train_chosen_labels, train_chosen_mask)
        ref_rejected_log_prob= compute_log_prob(ref_rejected_output_logits, train_rejected_labels, train_rejected_mask)
                
        # 计算损失
        loss = compute_loss(train_chosen_log_prob, train_rejected_log_prob, ref_chosen_log_prob, ref_rejected_log_prob, dpo_cfg.beta)

        total_loss += loss.item()

        # 反向传播
        loss.backward()

        # 更新学习率
        lr = cosine_decay(batch, total_batch, dpo_cfg.lr, dpo_cfg.warmup_ratio)
        optimizer.param_groups[0]["lr"] = lr

        # 更新梯度
        optimizer.step()

        optimizer.zero_grad()

        if batch != 0 and batch % dpo_cfg.log_iter == 0:
            avg_loss = total_loss / dpo_cfg.log_iter
            writer.add_scalar("train_loss", avg_loss, batch)
            total_loss = 0

        if batch % dpo_cfg.test_iter == 0:
            eval_loss = get_eval_loss(train_model, ref_model, eval_chosen_ids, eval_rejected_ids, dpo_cfg)
            writer.add_scalar("eval_loss", eval_loss, batch)

    train_model.save_pretrained(dpo_cfg.save_dir)
    tokenizer.save_pretrained(dpo_cfg.save_dir)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("./finetuned/02_sft_demo")

    dpo_cfg = DPOConfig()
    train()