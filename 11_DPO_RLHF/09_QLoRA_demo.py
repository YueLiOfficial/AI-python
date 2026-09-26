from transformers import BitsAndBytesConfig, AutoModelForCausalLM
import torch
from datasets import load_dataset
from trl.trainer import SFTConfig
import os
from transformers import AutoModelForCausalLM
from trl.trainer import SFTTrainer
from transformers import AutoTokenizer

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4", # 量化类型，使用nf4
    bnb_4bit_use_double_quant=False, # 是否使用双重量化
    bnb_4bit_compute_dtype=torch.bfloat16
)

quantized_model = AutoModelForCausalLM.from_pretrained(
    "./model/Qwen3-8B",
    quantization_config=quantization_config
)

from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

lora_cfg = LoraConfig(
    task_type="CAUSAL_LM",
    r=8,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules="all-linear"
)

prepared_quantized_model = prepare_model_for_kbit_training(model=quantized_model)

quantized_peft_model = get_peft_model(model=prepared_quantized_model, peft_config=lora_cfg)


datasets = load_dataset("json", data_files={
    "train": "data/psychology_data.jsonl",
})

datasets["train"] = datasets["train"].shuffle()
datasets["train"] = datasets["train"].select(range(16000))
datasets = datasets["train"].train_test_split(0.05)

def convert_func(batch):
    conversation_lists = batch["conversation"]

    message_list = []

    for conversation in conversation_lists:
        human_msg = conversation[0]["human"]
        assistant_msg = conversation[0]["assistant"]

        message = [
            {"role": "user", "content": human_msg},
            {"role": "assistant", "content": assistant_msg}
        ]

        message_list.append(message)

    batch["messages"] = message_list

    return batch

converted_data = datasets.map(convert_func, batched=True, remove_columns=datasets["train"].column_names)

os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs/09_QLoRA_demo"
sft_cfg = SFTConfig(
    per_device_train_batch_size=1,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=32,
    max_steps=500,
    # num_train_epochs=

    logging_strategy="steps",
    logging_steps=25,
    report_to="tensorboard",

    learning_rate=3e-4,
    lr_scheduler_type="cosine",
    warmup_steps=0.1,
    # optim="" 默认是adamw

    eval_strategy="steps",
    eval_steps=50,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    load_best_model_at_end=True,
    save_strategy="steps",
    save_steps=50,
    save_total_limit=3,
    output_dir="./finetuned/09_QLoRA_demo/checkpoint",

    bf16=True,
    gradient_checkpointing=False,
    activation_offloading=False,
    max_length=700,
    # use_liger_kernel=
    # model_init_kwargs=

    assistant_only_loss=True,
    chat_template_path="./new_chat_template.jinja"
)

tokenizer = AutoTokenizer.from_pretrained("./model/Qwen3-8B/")

trainer = SFTTrainer(
    model=quantized_peft_model,
    args=sft_cfg,
    train_dataset=converted_data["train"],
    eval_dataset=converted_data["test"],
    processing_class=tokenizer
)

trainer.train()

trainer.save_model("./finetuned/09_QLoRA_demo/model")