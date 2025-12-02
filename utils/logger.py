"""
Logger implementation with several details of
verbosity and control the errors/warnings of an
execution.
"""

from enum import IntEnum
try:
    from termcolor import colored
except ImportError:
    def colored(x, _):
        """Placeholder for colored output."""
        return x

class LoggerLevels(IntEnum):
    """Definition for the verbosity levels of logger."""
    NO      = 0
    INFO    = 1
    LOG     = 2
    DEBUG   = 3
    VERBOSE = 4

class MyLogger:
    """Logger with several details of verbosity."""
    verbose_level: LoggerLevels = LoggerLevels.INFO

    _LEVELS = {
        "INFO":    {"level": LoggerLevels.INFO,  "color": None},
        "LOG":     {"level": LoggerLevels.LOG,   "color": "cyan"},
        "DEBUG":   {"level": LoggerLevels.DEBUG, "color": "blue"},
        "SUCCESS": {"level": LoggerLevels.INFO,  "color": "green"},
        "WARNING": {"level": LoggerLevels.INFO,  "color": "yellow"},
        "ERROR":   {"level": LoggerLevels.INFO,  "color": "red"},
        "CRITICAL":{"level": LoggerLevels.INFO,  "color": "red"},
    }
    _LJ_CHARS = 9
    _ALWAYS_PRINT = ("SUCCESS","WARNING","ERROR","CRITICAL")
    @classmethod
    def set_verbose_level(cls, level: LoggerLevels):
        """Set the verbosity level of the logger."""
        if level not in LoggerLevels:
            raise ValueError(f"Invalid log level: {level}")
        cls.verbose_level = level

    @classmethod
    def _log(cls, label: str, *args: str):
        info = cls._LEVELS[label]
        if cls.verbose_level >= info["level"] or label in cls._ALWAYS_PRINT:
            x = cls._LJ_CHARS
            l = label.ljust(x)
            text = f"{l+":"} {' '.join(str(a) for a in args)}"
            print(colored(text, info["color"]) if info["color"] else text)

    @classmethod
    def info(cls, *args: str):
        """Log an info message."""
        cls._log("INFO", *args)
    @classmethod
    def log(cls, *args: str):
        """Log an info message."""
        cls._log("LOG", *args)
    @classmethod
    def debug(cls, *args: str):
        """Log a debug message."""
        cls._log("DEBUG", *args)
    @classmethod
    def success(cls, *args: str):
        """Log a success message."""
        cls._log("SUCCESS", *args)
    @classmethod
    def warning(cls, *args: str):
        """Log a warning message."""
        cls._log("WARNING", *args)
    @classmethod
    def error(cls, *args: str):
        """Log an error message."""
        cls._log("ERROR", *args)
    @classmethod
    def critical(cls, *args: str):
        """Log a critical message."""
        cls._log("CRITICAL", *args)
