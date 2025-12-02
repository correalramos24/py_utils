import yaml

def get_yaml_content(yaml_fd) -> dict[str, object]:
    return yaml.safe_load(yaml_fd)
