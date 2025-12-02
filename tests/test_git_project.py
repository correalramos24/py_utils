
from unittest import TestCase
from pathlib import Path

from utils.git_project import GitProject

class TestGitProject(TestCase):
    test_rundir = Path(__file__).parent

    def test_git_project(self):
        a = GitProject(Path(self.test_rundir))
        print(a)
