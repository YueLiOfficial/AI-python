from datasets import load_dataset

dataset = load_dataset("./data/ultrafeedback_binarized")

new_dataset = dataset.remove_columns(['prompt', 'prompt_id', 'messages', 'score_chosen', 'score_rejected'])

from trl.trainer import DPOConfig
import os
os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs/07_peft_dpo_demo"
dpo_cfg = DPOConfig(
    per_device_train_batch_size=1,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=32,
    max_steps=500,
    # num_train_epochs=

    logging_strategy="steps",
    logging_steps=25,
    report_to="tensorboard",

    learning_rate=3e-6,
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
    output_dir="./finetuned/07_peft_dpo_demo/checkpoint",

    bf16=True,
    gradient_checkpointing=False,
    # activation_offloading=False,
    max_length=700,
    # use_liger_kernel=
    # model_init_kwargs=

    # assistant_only_loss=True,
    # chat_template_path="./new_chat_template.jinja"
    beta=0.1
)

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl.trainer import DPOTrainer

lora_cfg = LoraConfig(
    task_type="CAUSAL_LM",
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules="all-linear"
)

model = AutoModelForCausalLM.from_pretrained("./finetuned/05_trl_sft_demo/model")
tokenizer = AutoTokenizer.from_pretrained("./finetuned/05_trl_sft_demo/model")
model.warnings_issued={}

peft_model = get_peft_model(
    model=model,
    peft_config=lora_cfg
)

trainer = DPOTrainer(
    model=peft_model,
    args=dpo_cfg,
    train_dataset=new_dataset["train_prefs"],
    eval_dataset=new_dataset["test_prefs"],
    processing_class=tokenizer
)

trainer.train()
trainer.save_model("./finetuned/07_peft_dpo_demo/model")