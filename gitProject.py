
from bashScript import BashCmd

from pathlib import Path

class GitProject:

    def __init__(self, path: Path):
        self.bManager = BashCmd(path)

    @property
    def git_commit(self) -> str:
        return self.bManager.run("git rev-parse --abbrev-ref HEAD").output()

    @property
    def git_branch(self) -> str:
        return self.bManager.run("git rev-parse --short HEAD").output()

    @property
    def git_tag(self) -> str:
        return self.bManager.run("git describe --tags --abbrev=0").output()

    def __str__(self):
        return f"GIT> {self.git_commit} @ {self.git_branch} ({self.git_tag})"