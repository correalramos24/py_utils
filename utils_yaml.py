import yaml
from typing import Any

def get_yaml_content(yaml_f : str) -> Any:
    return yaml.safe_load(yaml_f)
