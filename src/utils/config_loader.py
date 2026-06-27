import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def load_yaml(relative_path: str) -> dict:
    with open(ROOT / relative_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def env(name: str, default=None):
    return os.getenv(name, default)
