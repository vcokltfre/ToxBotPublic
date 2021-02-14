from yaml import safe_load
from pathlib import Path

def load():
    with Path("config.yml").open(encoding='utf-8') as f:
        return safe_load(f)
