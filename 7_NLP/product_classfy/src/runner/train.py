from preprocess.dataset import get_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding
import torch
from common.config import *
from torch import optim
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
from tqdm import tqdm
import time
from dataclasses import dataclass
from sklearn.metrics import accuracy_score, f1_score

@dataclass
class TrainConfig:
    batch_size: int = BATCH_SIZE
    epochs: int = EPOCHS
    lr: float = LR
    save_step: int = SAVE_STEP

    output_dir: str = MODELS_DIR
    logs_dir: str = LOGS_DIR

    early_stop_metric: str = "loss"
    early_stop_patience: int = 10

class Trainer:
    def __init__(self, model, train_dataset, valid_dataset, collate_fn, valid_fn, device, trainconfig=TrainConfig()):
        self.trainconfig = trainconfig
        self.device = device
        self.model = model.to(self.device)
        self.train_dataset = train_dataset
        self.valid_dataset = valid_dataset
        self.collate_fn = collate_fn
        self.valid_fn = valid_fn

        # 定义优化器
        self.optimizer = optim.Adam(model.parameters(), lr=self.trainconfig.lr)
        # 定义日志写入器
        self.writer = SummaryWriter(LOGS_DIR / time.strftime("%Y-%m-%d_%H-%M-%S"))
        # 当前的step
        self.step = 0
        # 定义AMPscaler
        self.scaler = torch.amp.GradScaler()

        # 早停
        self.early_stop_best_score = -float("inf")
        self.early_stop_counter = 0
        self.early_stop_metric = self.trainconfig.early_stop_metric

        self.best_model_path = Path(self.trainconfig.output_dir) / "best"
        self.checkpoint_path = Path(self.trainconfig.output_dir) / "last" / "checkpoint.pt"

    def _get_dataloader(self, dataset, shuffle=True):
        dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=shuffle, collate_fn=self.collate_fn)
    
        return dataloader

    def _train_one_batch(self, inputs):
        self.model.train()

        with torch.autocast(device_type=self.device.type, dtype=torch.float16):
            outputs = self.model(**inputs)

        self.scaler.scale(outputs.loss).backward()

        self.scaler.step(self.optimizer)
        self.scaler.update()

        self.optimizer.zero_grad()

        return outputs.loss

    def _should_early_stop(self, metrics):
        # 提取指标
        metric = metrics[self.trainconfig.early_stop_metric]

        # 统一指标为越大越好
        score = -metric if self.trainconfig.early_stop_metric == "loss" else metric

        # 判断指标，如果指标变好则保存模型并返回false，否则的话counter+1，如果counter超过patience则停止训练
        if score > self.early_stop_best_score:
            self.early_stop_best_score = score
            self.early_stop_counter = 0
            # 保存模型
            self.model.save_pretrained(self.best_model_path)
            tqdm.write("模型保存成功")
            return False
        
        else:
            self.early_stop_counter += 1

            if self.early_stop_counter >= self.trainconfig.early_stop_patience:
                return True
            else:
                return False

    def _load_checkpoint(self):
        if self.checkpoint_path.exists():
            checkpoint = torch.load(self.checkpoint_path)

            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            self.scaler.load_state_dict(checkpoint["scaler_state_dict"])
            self.step = checkpoint["step"]
            self.early_stop_counter = checkpoint["early_stop_counter"]
            self.early_stop_best_score = checkpoint["early_stop_best_score"]

            print("检查点加载成功")
        else:
            print("未发现检查点")
        

    def _save_checkpoint(self):
        checkpoint = {
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scaler_state_dict": self.scaler.state_dict(),
            "step": self.step,
            "early_stop_best_score": self.early_stop_best_score,
            "early_stop_counter": self.early_stop_counter
        }

        torch.save(checkpoint, self.checkpoint_path)
        print("检查点保存成功")

    def train(self):
        # 加载检查点
        self._load_checkpoint()

        train_dataloader = self._get_dataloader(self.train_dataset, shuffle=True)

        for epoch in range(self.trainconfig.epochs):
            for batch in tqdm(train_dataloader, desc=f"[训练] 第{epoch + 1}/{self.trainconfig.epochs}轮"):
                inputs = {k: v.to(self.device) for k, v in batch.items()}

                self.step += 1
                loss = self._train_one_batch(inputs=inputs)

                # 每100个step评估一次
                if self.step % self.trainconfig.save_step == 0:
                    # tqdm.write(f"loss = {loss:.6f}")

                    # 写入日志
                    self.writer.add_scalar("loss", loss, self.step)

                    # 验证评估
                    metrics = self.evaluate()
                    tqdm.write(f"[evaluation] step = {self.step}, {metrics}")

                    # 判断是否需要保存模型和早停
                    if self._should_early_stop(metrics):
                        tqdm.write("早停")
                        return

                    # 保存检查点
                    self._save_checkpoint()


    def evaluate(self):
        pred_list = []
        true_list = []
        total_loss = 0

        valid_dataloader = self._get_dataloader(self.valid_dataset, shuffle=False)

        self.model.eval()
        with torch.no_grad():
            for batch in tqdm(valid_dataloader, desc=f"[evaluation]"):
                inputs = {k: v.to(self.device) for k, v in batch.items()}

                outputs = self.model(**inputs)

                y_pred = outputs.logits.argmax(dim=-1)
                y_true = inputs["labels"]

                pred_list.extend(y_pred.tolist())
                true_list.extend(y_true.tolist())

                total_loss += outputs.loss.item()

        avg_loss = total_loss / len(valid_dataloader)
        
        result = self.valid_fn(true_list, pred_list)

        metrics = {"loss": avg_loss, **result}

        return metrics


def train():
    # 1. 定义设备
    device = torch.device(
        "cuda" if torch.cuda.is_available() 
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )

    # 2. 定义模型
    # 加载label列表
    with open(LABEL_FILE, "r", encoding="utf-8")as f:
        label_list = f.read().split('\n')

    # 转换成id和label的映射
    id2label = {label_id: label for label_id, label in enumerate(label_list)}
    label2id = {label: label_id for label_id, label in enumerate(label_list)}

    # 定义模型
    model = AutoModelForSequenceClassification.from_pretrained(
        str(PRETRAINED_MODEL),
            num_labels=len(label_list),
            id2label=id2label,
            label2id=label2id
        )
    model.to(device)

    # 3. 获取数据加载器
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL)
    train_dataset = get_dataset("train")
    valid_dataset = get_dataset("valid")

    # 4. 定义对齐函数和评估函数
    collate_fn = DataCollatorWithPadding(tokenizer)
    def valid_fn(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="macro")

        return {"acc": acc, "f1": f1}
    

    # 5. 开始训练
    trainconfig = TrainConfig(early_stop_metric="acc")
    trainer = Trainer(
        model=model,
        train_dataset=train_dataset,
        valid_dataset=valid_dataset,
        collate_fn=collate_fn,
        valid_fn=valid_fn,
        device=device,
        trainconfig=trainconfig
    )

    trainer.train()

if __name__ == "__main__":
    train()