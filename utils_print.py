from termcolor import colored
from enum import IntEnum

class myLoggerLevels(IntEnum):
    NO      = 0
    INFO    = 1
    LOG     = 2
    DEBUG   = 3
    VERBOSE = 4

class myLogger:

    verbose_level : myLoggerLevels = myLoggerLevels.INFO

    @classmethod
    def set_verbose_lvl(cls, log_level : myLoggerLevels):
        if log_level not in myLoggerLevels:
            raise Exception("Invalid log_level", log_level)
        cls.verbose_level = log_level

    @classmethod
    def info(cls, *msg_args: str):
        if cls.verbose_level >= myLoggerLevels.INFO:
            print("INFO:".ljust(9), *msg_args)

    @classmethod
    def log(cls,*msg_args: str):
        if cls.verbose_level >= myLoggerLevels.LOG:
            print(colored("LOG:".ljust(10) + " ".join(str(arg) for arg in msg_args), "cyan"))

    @classmethod
    def debug(cls,*msg_args: str):
        if cls.verbose_level >= myLoggerLevels.DEBUG:
            print(colored("DEBUG:".ljust(10) + " ".join(str(arg) for arg in msg_args), "blue"))

    @classmethod
    def success(cls,*msg_args: str):
        print(colored("SUCCES!".ljust(10) + " ".join(str(arg) for arg in msg_args), "green"))

    @classmethod
    def warning(cls,*msg_args: str):
        print(colored("WARN!".ljust(10) + " ".join(str(arg) for arg in msg_args), "yellow"))

    @classmethod
    def error(cls,*msg_args: str):
        print(colored("ERROR!".ljust(10) + " ".join(str(arg) for arg in msg_args), "red"))

    @classmethod
    def critical(cls,*msg_args: str):
        print(colored("CRITICAL!".ljust(10) + " ".join(str(arg) for arg in msg_args), "red"))
