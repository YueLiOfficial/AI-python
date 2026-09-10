import nltk
from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from abc import ABC, abstractmethod
from config import *

class BaseTokenizer(ABC):
    def __init__(self, vocab):
        self.vocab_size = len(vocab)
        self.id2token = vocab
        self.token2id = {token: token_id for token_id, token in enumerate(self.id2token)}

        self.pad_id = self.token2id[PAD_TOKEN]
        self.unk_id = self.token2id[UNK_TOKEN]
        self.sos_id = self.token2id[SOS_TOKEN]
        self.eos_id = self.token2id[EOS_TOKEN]

    @classmethod
    def create_vocab(cls, sentences, vocab_path):
        vocab = set()
        
        for text in sentences:
            tokens = cls._tokenize(text)
            vocab.update(tokens)

        vocab = [PAD_TOKEN, UNK_TOKEN, SOS_TOKEN, EOS_TOKEN] + list(vocab)

        with open(vocab_path, "w", encoding="utf-8") as f:
            f.write("\n".join(vocab))

    @classmethod
    def from_vocab(cls, vocab_path):
        vocab = []

        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab = [line.strip() for line in f]

        return cls(vocab)

    @staticmethod
    @abstractmethod
    def _tokenize(text):
        pass

    def encode(self, text, AddSosEos = False):
        tokens = self._tokenize(text)

        ids = [self.token2id.get(token, self.unk_id) for token in tokens]

        if AddSosEos:
            ids = [self.sos_id] + ids + [self.eos_id]

        return ids

class ZhTokenizer(BaseTokenizer):
    def __init__(self, vocab):
        super().__init__(vocab)

    @staticmethod
    def _tokenize(text):
        return list(text)

class EnTokenizer(BaseTokenizer):
    def __init__(self, vocab):
        super().__init__(vocab)

    @staticmethod
    def _tokenize(text):
        return word_tokenize(text)

    def decode(self, ids):
        tokens = [self.id2token[token_id] for token_id in ids]

        return TreebankWordDetokenizer().detokenize(tokens)

if __name__ == "__main__":
    text = "你在干什么"

    ZhTokenizer.create_vocab([text], "./text.txt")
    tokenizer = ZhTokenizer.from_vocab("text.txt")

    print(tokenizer.encode(text))
    
