
from abc import ABC
from .logger import MyLogger

class MetaAbstractClass(ABC):
    #TODO: check classmethod
    def classname(self) -> str:
        return self.__class__.__name__
    @classmethod
    def _info(cls, *msg):
        MyLogger.info(*msg)
    @classmethod
    def _log(cls, *msg):
        MyLogger.log(*msg)
    @classmethod
    def _dbg(cls, *msg):
        MyLogger.debug(*msg)
    @classmethod
    def _ok(cls, *msg):
        MyLogger.success(*msg)
    @classmethod
    def _warn(cls, *msg):
        MyLogger.warning(*msg)
    @classmethod
    def _err(cls, *msg):
        MyLogger.error(*msg)
    @classmethod
    def _critical(cls, *msg):
        MyLogger.critical(*msg)
