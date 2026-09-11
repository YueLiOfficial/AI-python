from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
PROCESSED_DIR_PATH = ROOT_PATH / "data/processed"
RAW_DATA_PATH = ROOT_PATH / "data/raw/online_shopping_10_cats.csv"
LOGS_DIR_PATH = ROOT_PATH / "logs"
MODELS_DIR_PATH = ROOT_PATH / "models"
PRETRAINED_DIR_PATH = ROOT_PATH / "pretrained"

BATCH_SIZE = 64
MAX_LEN = 128