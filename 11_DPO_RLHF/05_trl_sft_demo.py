from datasets import load_dataset
from trl.trainer import SFTConfig
import os
from transformers import AutoModelForCausalLM
from trl.trainer import SFTTrainer
from transformers import AutoTokenizer

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

os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs/05_trl_sft_demo"
sft_cfg = SFTConfig(
    per_device_train_batch_size=1,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=32,
    max_steps=500,
    # num_train_epochs=

    logging_strategy="steps",
    logging_steps=25,
    report_to="tensorboard",

    learning_rate=3e-5,
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
    output_dir="./finetuned/05_trl_sft_demo/checkpoint",

    bf16=True,
    gradient_checkpointing=False,
    activation_offloading=False,
    max_length=700,
    # use_liger_kernel=
    # model_init_kwargs=

    assistant_only_loss=True,
    chat_template_path="./new_chat_template.jinja"
)

model = AutoModelForCausalLM.from_pretrained("./model/Qwen3-0.6B/")
tokenizer = AutoTokenizer.from_pretrained("./model/Qwen3-0.6B/")

trainer = SFTTrainer(
    model=model,
    args=sft_cfg,
    train_dataset=converted_data["train"],
    eval_dataset=converted_data["test"],
    processing_class=tokenizer
)

trainer.train()

trainer.save_model("./finetuned/05_trl_sft_demo/model")