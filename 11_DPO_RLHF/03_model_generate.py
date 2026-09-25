from transformers import AutoModelForCausalLM, AutoTokenizer
from argparse import ArgumentParser
import torch

# 解析命令行参数
# 03_model_generate.py --prompt xxx --model-path xxx

parser = ArgumentParser()
parser.add_argument("--prompt", type=str)
parser.add_argument("--model_path", type=str)

args = parser.parse_args()

prompt= args.prompt
model_path = args.model_path

# 自回归生成
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 分词
messages_list = [{"role": "user", "content": prompt}]

token_ids = tokenizer.apply_chat_template(messages_list, tokenize=True, add_generation_prompt=True)["input_ids"]

input_ids = torch.tensor([token_ids], dtype=torch.long, device=device)

# 进行自回归生成
result = model.generate(input_ids, max_new_tokens=500, eos_token_id=151645)

# 对结果进行切片，将输入的prompt给切出去
res_token_ids = result[:, len(token_ids):]

# 解码
res_text = tokenizer.decode(res_token_ids[0])

print(res_text)
