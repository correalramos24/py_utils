
import stat
from pathlib import Path
from typing import Optional, List

from .utils_py import listify, stringfy
from .utils_files import ExpectFile, check_file_exists_exception
from .bash_cmd import BashCmd


class BashScript(BashCmd):
    BEGIN_SCRIPT = "AUTOMATED BASH WRAPPER GENERATION:"
    TRAILER_SCRIPT = "#" * 80

    def __init__(self, script_path: Path, template_p: Optional[Path] = None) -> None:
        self.s: Path = script_path
        self.__tmp_s: Path = template_p
        # Checks script file:
        if self.s.exists() and self.s.is_dir():
            raise ExpectFile(self.s)
        self._warn("Overwriting existing script @", self.s)

        # Checks template script file:
        if self.__tmp_s:
            check_file_exists_exception(self.__tmp_s)

        self.__cmds: Optional[List[str]] = None

        super().__init__(self.s.parent)

    def dry(self):
        if self.__tmp_s and self.__cmds:
            self._warn("Template & cmds provided!")
        if self.__tmp_s:
            self.__copy_template()
        elif self.__cmds:
            self._generate_script()

    def __copy_template(self) -> None:
        raise NotImplementedError()

    def _generate_script(self) -> None:
        """Generate a bash script file with the given commands."""
        content = "\n".join(["#!/bin/bash",
                             f"# {self.BEGIN_SCRIPT}", "",
                             self._cmds_str(),
                             "",
                             f"# {self.TRAILER_SCRIPT}"])
        self.s.write_text(content)
        self.s.chmod(self.s.stat().st_mode | stat.S_IXUSR)  # ADD EXEC RIGHTS
        self._ok("Generated bash script @", self.s)

    def _cmds_str(self) -> str:
        return '\n'.join([c.lstrip() for c in self.__cmds])

    def with_cmds(self, cmds: List[str] | str) -> "BashScript":
        self.__cmds = listify(cmds)
        self._dbg(f"BashScript {self.s} w/ cmd(s): {stringfy(cmds)}")
        return self

    def run(self, cmd=None) -> "BashScript":
        self.dry()
        self._info("Running script: ", self.s)
        if cmd:
            super().run(cmd)
        else:
            super().run("./" + str(self.s.name))
        return self
