import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding
from sklearn.metrics import accuracy_score, f1_score
from preprocess.dataset import get_dataset
from runner.train import Trainer
from common.config import *

def evaluate():
    device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )

    model = AutoModelForSequenceClassification.from_pretrained(MODELS_DIR / "best")

    test_dataset = get_dataset("test")

    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)
    collate_fn = DataCollatorWithPadding(tokenizer)

    def valid_fn(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="macro")

        return {"acc": acc, "f1": f1}

    trainer = Trainer(
        model=model,
        train_dataset=None,
        valid_dataset=test_dataset,
        collate_fn=collate_fn,
        valid_fn=valid_fn,
        device=device
    )

    matrics = trainer.evaluate()

    print(matrics)

if __name__ == "__main__":
    evaluate()
