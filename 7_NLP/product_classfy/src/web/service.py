
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

from runner.predict import Predictor
from common.config import *

class TitlePredictService:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(MODELS_DIR / "best")
        self.tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)
        self.device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )

        self.predictor = Predictor(self.model, self.tokenizer, self.device)

    def predict_classification(self, title):
        return self.predictor.predict(title)

        