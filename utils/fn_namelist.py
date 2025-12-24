
from pathlib import Path
import f90nml

from .utils_files import check_file_exists_exception


class FnNamelist:
    def __init__(self, namelist_path: Path):
        check_file_exists_exception(namelist_path)
        self.p = namelist_path

    def set_key(self, namelist_name: str, key: str, value: str):
        nml = f90nml.read(self.p)

        old_value = nml[namelist_name].get(key, None)
        if isinstance(old_value, bool):
            parsed_value = value.lower() in ['true', '.true.', '1']
        elif isinstance(old_value, int):
            parsed_value = int(value)
        elif isinstance(old_value, float):
            parsed_value = float(value)
        elif isinstance(old_value, list):
            parsed_value = [type(old_value[0])(v.strip()) for v in value.split(',')]
        else:
            parsed_value = value.strip("'\"")  # default: string

        nml[namelist_name][key] = parsed_value
        f90nml.write(nml, self.p, force=True)

    def get_key(self, namelist_name: str, key: str) -> object:
        nml = f90nml.read(self.p)
        return nml[namelist_name][key]

    def append_key(self, namelist_name: str, data: dict):
        nml = f90nml.read(self.p)
        if namelist_name not in nml:
            nml[namelist_name] = {}

        for key, value in data.items():
            if isinstance(value, list):
                nml[namelist_name][key] = value
            else:
                nml[namelist_name][key] = value

        f90nml.write(nml, str(self.p), force=True)
