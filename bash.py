from io import TextIOWrapper

from utils_py import listify, stringfy
from utils_controllers import MetaAbstractClass

import os, subprocess
from pathlib import Path
from textwrap import dedent
from typing import Optional, List

# =============================BASH VARS======================================
def expand_bash_env_vars(value:  str|list[str]) -> str|list[str] | None:
    """Convert the bash variables ($VAR or ${VAR}) to the value."""
    if isinstance(value, str):
          return os.path.expandvars(value) if "$" in value else None
    if isinstance(value, list) and any("$" in v for v in value):
          return [os.path.expandvars(v) for v in value]
    return None

# =============================BASH SCRIPTS====================================
class BashManager(MetaAbstractClass):
    def __init__(self, rundir: Optional[Path]):
        self.p      = rundir
        if not rundir: self.p = Path(os.getcwd())
        self.output = None
        self.log_fd = None
        self._dbg("Bash manager @", rundir)

    def with_log(self, log_file: Path) -> "BashManager":
        self.log_fd = open(log_file, mode="w")
        self._dbg("Adding logfile @", log_file)
        return self

    def run_output(self, cmd : str) -> str:
        try:
            self.output = subprocess.check_output(
                cmd, cwd=self.p, shell=True,
                stderr=subprocess.STDOUT).strip().decode('utf-8')
            return self.output
        except Exception as e:
            self._err(e)
            return "Error"

    def run(self, cmd : str) -> None:
        subprocess.run(cmd, cwd=self.p, shell=True, text=True,
                       stdout=self.log_fd, stderr=subprocess.STDOUT)
        if self.log_fd is not None: self.log_fd.close()

class BashScript(BashManager):
    BEGIN_SCRIPT = "AUTOMATED BASH WRAPPER GENERATION:"
    TRAILER_SCRIPT = "#" * 80

    def __init__(self, s_path: Path) -> None:
        self.__cmds = None
        self.full_path   = s_path
        self.script_path = s_path.name
        self.script_dir  = s_path.parent
        super().__init__(self.script_dir)

    def with_cmds(self, cmds : List[str]) -> "BashScript":
        self.__cmds = cmds
        return self

    def run_output(self, cmd : str) -> str:
        self.__generate_script()
        return super().run_output("")

    def run(self, cmd : str = "") -> None:
        self.__generate_script()
        return super().run("")


    def __generate_script(self) -> None:
        """Generate a bash script file with the given commands."""
        script_content = dedent(f"""\
            #!/bin/bash
            # {self.BEGIN_SCRIPT}

            {'\n'.join(self.__cmds)}

            # {self.TRAILER_SCRIPT}
        """)
        self.full_path.write_text(script_content)


