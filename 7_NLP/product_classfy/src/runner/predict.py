from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

from common.config import *

class Predictor:
    def __init__(self, model, tokenizer, device):
        self.device = device
        self.model = model.to(self.device)
        self.tokenizer = tokenizer

    def predict(self, text: str | list[str]) -> str | list[str]:
        is_str = isinstance(text, str)

        if is_str:
            text = [text]

        # 分词
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model(**inputs)

        predict_ids = outputs.logits.argmax(dim=-1).tolist()

        predict_labels = [self.model.config.id2label[label_id] for label_id in predict_ids]

        if is_str:
            return predict_labels[0]

        return predict_labels

def predict():
    device = torch.device("cuda" if torch.cuda.is_available()
                                  else "mps" if torch.backends.mps.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)

    model = AutoModelForSequenceClassification.from_pretrained(MODELS_DIR / "best")

    predictor = Predictor(
        model=model,
        tokenizer=tokenizer,
        device=device
    )

    text = "好奇心钻装纸尿裤L40片9-14kg"
    
    print(predictor.predict(text))

if __name__ == "__main__":
    predict()

