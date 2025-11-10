
from utils.utils_bash import command_output

from pathlib import Path

class GitProject:

    def __init__(self, path: Path):
        self.path = path

    @property
    def git_commit(self) -> str:
        return command_output("git rev-parse --abbrev-ref HEAD", self.path)

    @property
    def git_branch(self) -> str:
        return command_output("git rev-parse --short HEAD", self.path)

    @property
    def git_tag(self) -> str:
        return command_output("git describe --tags --abbrev=0", self.path)

    def __str__(self):
        return f"GIT> {self.git_commit} @ {self.git_branch} ({self.git_tag})"