
from gitProject import *

from unittest import TestCase


class TestGitProject(TestCase):
    test_rundir = Path(__file__).parent

    def test_git_project(self):
        a = GitProject(Path(self.test_rundir))
        print(a)