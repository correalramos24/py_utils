
import os
from typing import Iterable, Callable
from pathlib import Path


# =============================CHECK TYPES======================================
def is_list(var: object) -> bool:
    return isinstance(var, list)


def is_str(var: object) -> bool:
    return isinstance(var, str)


def is_path(var: object) -> bool:
    return isinstance(var, Path)


def pathfy(var: str | Path) -> Path:
    return Path(var)


def to_int_list(items: Iterable) -> list[int]:
    return list(map(int, items))
# =============================PATH METHODS=====================================


def path_to_str(p: Path) -> str:
    return str(p.name).replace("/", "-")


def fpath_to_str(p: Path) -> str:
    return str(p).replace("/", "-")


# =============================STRING METHODS===================================
def stringfy(var: Path | object | list[object]) -> str:
    """Convert var to string, according to the type"""
    if is_path(var):
        return path_to_str(var)
    if is_list(var):
        return ",".join(str(e) for e in var)
    return str(var)


def search_char_in_str(s: str, char: str = "&") -> list[int]:
    return [i for i, c in enumerate(s) if c == char]


# =============================LIST METHODS=====================================
def listify(var: object | list[object] | None) -> list[object] | None:
    """Convert var to list, if it is not already a list or none"""
    if is_list(var) or var is None:
        return var
    return [var]


def intersect_lists(l1: list[object], l2: list[object]) -> list[object]:
    return [e for e in l1 if e in l2]


# =============================DICT METHODS=====================================

def get_key(
    d: dict[object, object],
    key: object,
    build: Callable[[object], object],
    dflt: object = None,
) -> object:
    """Get key from dict, if it exists, otherwise return default,
    may raise exception in the builder"""
    return build(d[key]) if key in d else dflt


def safe_get_key(
    d: dict[object, object],
    k: object,
    build: Callable[[object], object],
    dflt: object = None,
) -> object:
    """Get key from dict, if it exists, otherwise return default"""
    if k in d.keys():
        try:
            return build(d[k])
        except (ValueError, TypeError):
            return dflt
    return dflt


def inter_dict_keys(d: dict[str, object], k: Iterable[str]) -> dict[str, object]:
    """Intersect dict keys with a list of keys"""
    return {_k: d[_k] for _k in k if _k in d}


def remove_keys(d: dict[str, object], k: Iterable[str]) -> dict[str, object]:
    """Remove keys from dict"""
    return {_k: v for _k, v in d.items() if _k not in k}


# ===============================BASH VARS=====================================
def expand_bash_env_vars(value: str | list[str]) -> str | list[str] | None:
    """Convert the bash variables ($VAR or ${VAR}) to the value."""
    if isinstance(value, str):
        return os.path.expandvars(value) if "$" in value else None
    if isinstance(value, list) and any("$" in v for v in value):
        return [os.path.expandvars(v) for v in value]
    return None
