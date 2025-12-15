
from abc import abstractmethod, ABC
from dataclasses import dataclass, fields
from pathlib import Path
import hashlib
from typing import Any, Hashable, Type, TypeVar

from .x_persistance import GenericPersistance
from .meta import MetaAbstractClass

T = TypeVar("T", bound="GenericObject")

@dataclass
class GenericObject(Hashable, ABC):
    @abstractmethod
    def get_id(self) -> bytes:
        ...

    def __hash__(self):
        return int(hashlib.md5(self.get_id()).hexdigest(), 16)


class GenericDomain(MetaAbstractClass):
    def __init__(self, db_root: Path, domain_type: Type[GenericObject]):
        self.persistance = GenericPersistance(db_root)
        self.domain_type = domain_type

    def create(self, **kwargs):
        field_names = {f.name for f in fields(self.domain_type)}
        missing = field_names - kwargs.keys()
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        obj = self.domain_type(**kwargs)
        self.persistance.store(hash(obj), obj)
        return obj

    def read(self, identifier: Hashable) -> Hashable:
        return self.persistance.load(identifier)

    def update(self, identifier: Hashable, **kwargs):
        if self.persistance.exist(identifier):
            i = self.persistance.load(identifier)
            for k, v in kwargs.items():
                if hasattr(i, k):
                    setattr(i, k, v)
            self.persistance.store(identifier, i)
        else:
            self._err(f"Trying to update non-bound identifier {identifier}")


    def delete(self, identifier: Hashable):
        self.persistance.remove(identifier)

