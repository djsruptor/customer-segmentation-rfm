from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONFIG_PATH = PROJECT_ROOT / 'configs/default.yaml'

DATA_DIR = PROJECT_ROOT / 'data'
RAW_DIR = DATA_DIR / 'raw'
MART_DIR = DATA_DIR / 'mart'

# API_NAME = 'Complaint Priority Scorer'
# API_VERSION = '1.0.0'