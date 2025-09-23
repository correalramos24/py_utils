from .utils_print import myLogger

from typing import cast, Callable
from pathlib import Path
import functools

# =============================CHECK TYPES======================================
def is_list(var : object) -> bool: return isinstance(var, list)
def is_str(var: object) -> bool: return isinstance(var, str)
def is_path(var: object) -> bool: return isinstance(var, Path)
# =============================PATH METHODS=====================================
def path_to_str(p: Path) -> str: return str(p.name).replace("/", "-")
def fpath_to_str(p: Path) -> str: return str(p).replace("/", "-")
# =============================STRING METHODS===================================
def stringfy(var : Path | object | list[object] | object ) -> str:
    """Convert var to string, according to the type"""
    if isinstance(var, Path): return path_to_str(var)
    elif isinstance(var, list): return ','.join(str(e) for e in var)
    else: return str(var)

def listify(var: object| list[object] | None) -> list[object] | None:
    """Convert var to list, if it is not already a list or none"""
    if is_list(var) or var is None: return var
    else: return [var]

def search_char_in_str(s: str, char: str = "&") -> list[int]:
    return [i for i, c in enumerate(s) if c == char]
# =============================LIST METHODS=====================================
def intersect_lists(l1: list[object], l2: list[object]) -> list[object]:
    return [e for e in l1 if e in l2]
# =============================DICT METHODS=====================================
def get_key(d: dict[object, object], key: object,
    build: Callable[[object], object],dflt: object = None) -> object:
    """Get key from dict, if it exists, otherwise return default,
    may raise exception in the builder"""
    return build(d[key]) if key in d else dflt

def safe_get_key(d: dict[object, object], k: object,
    build: Callable[[object], object],dflt: object = None) -> object:
    """Get key from dict, if it exists, otherwise return default"""
    if k in d.keys():
        try: return build(d[k])
        except Exception: return dflt
    else:
        return dflt

def inter_dict_keys(d: dict[str, object],k: list[str]) -> dict[str, object]:
    """Intersect dict keys with a list of keys"""
    return {_k: d[_k] for _k in k if _k in d}

def remove_keys(d: dict[str, object], k: list[str]) -> dict[str, object]:
    """Remove keys from dict"""
    return {_k: v for _k, v in d.items() if not _k in k}

# ==============================DECORATORS=====================================
def check_exceptions(func: Callable[[object], object]):
    @functools.wraps(func)
    def wrapper(*args: tuple[object], **kwargs: dict[str, object]):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            myLogger.error(str(e))
    return wrapper

def safe_return(default: object):
    def decorator(func: Callable[[object], object]):
        @functools.wraps(func)
        def wrapper(*args: tuple[object], **kwargs: dict[str, object]):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                myLogger.error(str(e))
                return default
        return wrapper
    return decorator
