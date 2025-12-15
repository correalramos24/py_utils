
import functools
from typing import Callable
from utils.logger import MyLogger
from dataclasses import field

def check_exceptions(func: Callable[[object], object]):
    @functools.wraps(func)
    def wrapper(*args: tuple[object], **kwargs: dict[str, object]):
        try:
            return func(*args, **kwargs)
        except Exception as e: # pylint: disable=broad-except
            MyLogger.error(str(e))
            return None
    return wrapper

def safe_return(default: object):
    def decorator(func: Callable[[object], object]):
        @functools.wraps(func)
        def wrapper(*args: tuple[object], **kwargs: dict[str, object]):
            try:
                return func(*args, **kwargs)
            except Exception as e: # pylint: disable=broad-except
                MyLogger.error(str(e))
                return default
        return wrapper
    return decorator

def opt_field(metadata=None):
    return field(default=None, metadata=metadata or {})
