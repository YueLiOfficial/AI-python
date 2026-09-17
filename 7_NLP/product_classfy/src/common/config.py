from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

RAW_DATA_DIR = ROOT_DIR / "data/raw"
PREPROCESSED_DATA_DIR = ROOT_DIR / "data/processed"
LOGS_DIR = ROOT_DIR / "logs"
MODELS_DIR = ROOT_DIR / "models"
PRETRAINED_MODEL = ROOT_DIR / "pretrained/bert-base-chinese"

SRC_DIR = ROOT_DIR / "src"

CONFIG_FILE = SRC_DIR / "common/config.py"
LABEL_FILE = MODELS_DIR / "labels.txt"
# PREPROCESS_FILE = SRC_DIR / "preprocess/preprocess.py"

BATCH_SIZE = 32
EPOCHS = 50
LR = 1e-5
SAVE_STEP = 100