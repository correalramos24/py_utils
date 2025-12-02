
from pathlib import Path

from .bash_script import BashCmd

class GitProject:
    """Information of a git repository."""
    def __init__(self, path: Path):
        self.b_manager = BashCmd(path)

    def git_commit(self) -> str:
        """Get the git commit hash."""
        return self.b_manager.run("git rev-parse --abbrev-ref HEAD").output()


    def git_branch(self) -> str:
        """Get current git branch name."""
        return self.b_manager.run("git rev-parse --short HEAD").output()

    def git_tag(self) -> str:
        """Get current git tag name."""
        r = self.b_manager.run("git describe --tags --abbrev=0")
        if r.ret_code() != 0:
            return "NO TAG"
        return r.output()

    def __str__(self):
        return f"GIT> {self.git_commit} @ {self.git_branch} ({self.git_tag})"
