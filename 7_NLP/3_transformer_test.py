import torch
from torch import nn
import nltk
from nltk.tokenize import word_tokenize

class Tokenizer:
    def __init__(self, language):
        self.language = language

        self.special_token = ["<PAD>", "<UNK>", "<SOS>", "<EOS>"]

    def tokenize(self, text):
        if self.language == "zh":
            return list(text)

        elif self.language == "en":
            return word_tokenize(text)


