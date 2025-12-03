
import os, subprocess, shlex
from pathlib import Path
from typing import Optional, List

from .meta import MetaAbstractClass

class BashCmd(MetaAbstractClass):
    """Run a Bash command at a certain rundir"""

    def __init__(self, rundir: Optional[Path] = None):
        self.p = Path(rundir or os.getcwd())
        self._output: Optional[str] = None
        self._cmplt_run: Optional[subprocess.CompletedProcess] = None
        self._log_file: Optional[Path] = None
        self._args: List[str] = []
        self._env: Optional[dict] = None

    def with_env(self, env: dict) -> "BashCmd":
        self._env = env | self._env
        return self

    def with_args(self, args: List[str]) -> "BashCmd":
        self._args.extend(args)
        return self

    def with_log(self, log_file: Path) -> "BashCmd":
        self._log_file = log_file
        return self

    def run(self, cmd: str) -> "BashCmd":
        self._dbg("Launching", " ".join([cmd] + self._args))
        full_cmd = shlex.split(" ".join([cmd] + self._args))
        out_trg = subprocess.PIPE if self._log_file is None else None
        err_trg = subprocess.STDOUT
        try:
            if self._log_file:
                with open(self._log_file, "w", encoding="utf-8") as fd:
                    r = subprocess.run(full_cmd, cwd=self.p, check=False,
                                       text=True,stdout=fd, stderr=err_trg)
            else:
                r = subprocess.run(full_cmd, cwd=self.p, check=False,
                                   text=True, stdout=out_trg, stderr=err_trg)
                self._output = r.stdout.strip() if r.stdout else ""
                self._cmplt_run = r
        except FileNotFoundError:
            self._err(f"Command '{cmd}' not found")
        return self

    def output(self) -> Optional[str]:
        return self._output

    def ret_code(self) -> Optional[int]:
        return None if self._cmplt_run is None else self._cmplt_run.returncode
