
from unittest import TestCase
from pathlib import Path
from dataclasses import dataclass, Field
from typing import List
import shutil

from utils.x_domain import GenericObject, GenericDomain
from utils.logger import MyLogger, LoggerLevels

@dataclass
class Nota(GenericObject):
    title: str
    content: str = None
    tags: List[str] = None

    def get_id(self) -> bytes:
        return self.title.encode("utf-8")

    def __eq__(self, other):
        return isinstance(other, Nota) and self.get_id() == other.get_id()

    def __hash__(self):
        return hash(self.get_id())


class TestGenericDomain(TestCase):

    def setUp(self):
        self.db_root = Path(__file__).parent / "nota"
        MyLogger.set_verbose_level(LoggerLevels.DEBUG)

    def tearDown(self):
        print("Removing files generated...")
        shutil.rmtree(self.db_root)

    def test_simple(self):
        nota_domain = GenericDomain(self.db_root, Nota)

        nota = nota_domain.create(title="Example", content="whatever", tags=["TAG1", "33"])
        print(nota)

        id_hash = hash(nota)
        print(nota_domain.read(id_hash))

        nota_domain.update(id_hash, content="My updated content")
        print(nota_domain.read(id_hash))

        nota_domain.delete(id_hash)
        print(nota_domain.read(id_hash))

