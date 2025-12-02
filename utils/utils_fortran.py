
from pathlib import Path

import f90nml

def update_f90nml_key_value(nml_path: Path, nml_name: str, key: str, value: str):
    nml = f90nml.read(nml_path)

    # Intenta inferir el tipo original del valor
    old_value = nml[nml_name].get(key, None)
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

    nml[nml_name][key] = parsed_value
    f90nml.write(nml, nml_path, force=True)

def get_f90nml_key_value(nml_path: Path, nml_name: str, key: str):
    nml = f90nml.read(nml_path)
    return nml[nml_name][key]


def add_f90nml(nml_path: Path, nml_name: str, payload: dict):
    nml = f90nml.read(nml_path)

    if nml_name not in nml:
        nml[nml_name] = {}

    for key, value in payload.items():
        if isinstance(value, list):
            nml[nml_name][key] = value
        else:
            nml[nml_name][key] = value

    f90nml.write(nml, str(nml_path), force=True)
