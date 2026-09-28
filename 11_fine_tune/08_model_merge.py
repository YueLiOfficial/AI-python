"""
将LoRA微调·后的适配器的模型权重，和基座模型，做合并，从而避免，LoRA微调之后，推理有额外的开销
"""
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./model/Qwen3-0.6B")
adapter_path = "./finetuned/06_peft_sft_demo/model"
tokenizer = AutoTokenizer.from_pretrained(adapter_path)

peft_model = PeftModel.from_pretrained(
    model=model,
    model_id=adapter_path
)

merged_model = peft_model.merge_and_unload()

merged_model.save_pretrained("./finetuned/lora_merged_model")
tokenizer.save_pretrained("./finetuned/lora_merged_model")
