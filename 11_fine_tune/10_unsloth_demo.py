from unsloth import FastLanguageModel
from unsloth.chat_templates import train_on_responses_only
from trl.trainer.sft_trainer import SFTTrainer
from trl.trainer.sft_config import SFTConfig
from datasets import load_dataset
import os

quantized_model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="./model/Qwen3-8B",
    load_in_4bit=True,

    use_exact_model_name=True,
    local_files_only=True
)

peft_model = FastLanguageModel.get_peft_model(
    model=quantized_model,
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    # target_modules= 默认是所有线性层
)

datasets = load_dataset("json", data_files={
    "train": "data/psychology_data.jsonl",
})

datasets["train"] = datasets["train"].shuffle()
datasets["train"] = datasets["train"].select(range(16000))
datasets = datasets["train"].train_test_split(0.05)

def convert_func(batch):
    conversation_lists = batch["conversation"]

    text_lists = []

    for conversation in conversation_lists:
        human_msg = conversation[0]["human"]
        assistant_msg = conversation[0]["assistant"]

        message = [
            {"role": "user", "content": human_msg},
            {"role": "assistant", "content": assistant_msg}
        ]

        texts = tokenizer.apply_chat_tamplate(message, tokenize=False)

        text_lists.append(texts)

    batch["text"] = text_lists

    return batch

converted_data = datasets.map(convert_func, batched=True, remove_columns=datasets["train"].column_names)

os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs/10_unsloth_demo"
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
    optim="paged_adamw_32bit", # 默认是adamw, paged_adamw_32bit是分页优化器

    eval_strategy="steps",
    eval_steps=50,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    load_best_model_at_end=True,
    save_strategy="steps",
    save_steps=50,
    save_total_limit=3,
    output_dir="./finetuned/10_unsloth_demo/checkpoint",

    bf16=True,
    gradient_checkpointing=False,
    activation_offloading=False,
    max_length=700,
    # use_liger_kernel=
    # model_init_kwargs=

    # assistant_only_loss=True,
    # chat_template_path="./new_chat_template.jinja"
)

trainer = SFTTrainer(
    model=peft_model,
    args=sft_cfg,
    train_dataset=converted_data["train"],
    eval_dataset=converted_data["test"],
    processing_class=tokenizer
)

trainer = train_on_responses_only(
    trainer=trainer,
    instruction_part="<|im_start|>user\n",
    response_part="<|im_start|assistant>\n"
)

trainer.train()

trainer.save_model("./finetuned/10_unsloth_demo/model")
