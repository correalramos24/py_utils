
from unittest import TestCase
from pathlib import Path

from utils.logger import MyLogger, LoggerLevels
from utils.yaml_file import YAMLFile, YAMLObject


class TestYAMLFile(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        print("Executing tests at", self.p)
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)

    def test_parser(self):
        yaml_file = YAMLFile(self.p / "test.yaml")
        f = YAMLObject(yaml_file.content)
        print(f)


    def test_minimal(self):
        f = YAMLFile(self.p / "test.yaml")
        print(f)