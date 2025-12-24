
import yaml
from pathlib import Path
from typing import Any

from .utils_files import check_file_exists_exception


class YAMLObject:
    def __init__(self, content: dict[str, Any]):
        self.content = self.parse_from_content(content)

    @staticmethod
    def parse_from_content(content : dict[str, Any]):
        ret = dict()
        for k, v in content.items():
            if isinstance(v, dict):
                ret[k] = YAMLObject(v)
            else:
                ret[k] = v
        return ret

    def __str__(self):
        ret = ""
        for k, v in self.content.items():
            if isinstance(v, YAMLObject):
                ret += k + " :\n"
                ret += YAMLObject.__str__(v)+"\n"
            else:
                ret += str(k) + "->" + str(v) + "\n"

        return ret


class YAMLFile:
    def __init__(self, path: Path):
        check_file_exists_exception(path)
        self.p = path
        self.content = yaml.safe_load(path.read_text())

    def __str__(self):
        ret = ""
        for k, v in self.content.items():
            ret += f"{k}: {v}\n"
        return ret


def get_yaml_content(yaml_fd) -> dict[str, object]:
    return yaml.safe_load(yaml_fd)
