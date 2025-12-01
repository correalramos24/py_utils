from enum import IntEnum
try:
    from termcolor import colored
except ImportError:
    colored = lambda x, y: x

class LoggerLevels(IntEnum):
    NO      = 0
    INFO    = 1
    LOG     = 2
    DEBUG   = 3
    VERBOSE = 4

class MyLogger:
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
    def info(cls, *args: str): cls._log("INFO", *args)
    @classmethod
    def log(cls, *args: str): cls._log("LOG", *args)
    @classmethod
    def debug(cls, *args: str): cls._log("DEBUG", *args)
    @classmethod
    def success(cls, *args: str): cls._log("SUCCESS", *args)
    @classmethod
    def warning(cls, *args: str): cls._log("WARNING", *args)
    @classmethod
    def error(cls, *args: str): cls._log("ERROR", *args)
    @classmethod
    def critical(cls, *args: str): cls._log("CRITICAL", *args)
