from datasets import load_dataset

datasets = load_dataset("json", data_files={
    "train": "data/keywords_data_train.jsonl",
    "test": "data/keywords_data_test.jsonl"
})

datasets["train"] = datasets["train"].shuffle()
datasets["train"] = datasets["train"].select(range(16000))

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

from trl.trainer import SFTConfig
import os
os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs/06_peft_sft_demo"
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
    output_dir="./finetuned/06_peft_sft_demo/checkpoint",

    bf16=True,
    gradient_checkpointing=False,
    activation_offloading=False,
    max_length=700,
    # use_liger_kernel=
    # model_init_kwargs=

    assistant_only_loss=True,
    chat_template_path="./new_chat_template.jinja"
)

from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("./model/Qwen3-0.6B/")

lora_cfg = LoraConfig(
    task_type="CAUSAL_LM",
    r=8,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules="all-linear"
)

peft_model = get_peft_model(
    model=model,
    peft_config=lora_cfg,
)


from trl.trainer import SFTTrainer
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("./model/Qwen3-0.6B/")

trainer = SFTTrainer(
    model=peft_model,
    args=sft_cfg,
    train_dataset=converted_data["train"],
    eval_dataset=converted_data["test"],
    processing_class=tokenizer
)

trainer.train()

trainer.save_model("./finetuned/06_peft_sft_demo/model")