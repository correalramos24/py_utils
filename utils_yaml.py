import yaml
from pathlib import Path

def get_yaml_content(yaml_f : Path) -> dict:
    return yaml.safe_load(yaml_f)