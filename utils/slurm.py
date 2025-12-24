
from pathlib import Path
import stat
from dataclasses import dataclass, fields, field
from typing import Any, Optional

from .decorators import opt_field
from .bash_script import BashScript


@dataclass
class SlurmDirectives:
    nodes: int = opt_field(metadata={"syntax": "-N", "env": 'SLURM_NNODES'})
    mpi: int = opt_field(
        metadata={"syntax": "--ntasks-per-node", "env": 'SLURM_TASKS_PER_NODE'}
    )
    tasks: int = opt_field(metadata={"syntax": "--ntasks", "env": 'SLURM_NTASKS'})
    omp: int = opt_field(metadata={"syntax": "-c", "env": 'SLURM_CPUS_PER_TASK'})
    account: str = opt_field(metadata={"syntax": "-A", "env": 'SLURM_JOB_ACCOUNT'})
    queue: str = opt_field(metadata={"syntax": "--qos", "env": 'SLURM_JOB_QOS'})
    t_lim: str = opt_field(metadata={"syntax": "--time", "env": 'SBATCH_TIMELIMIT'})
    job_name: str = opt_field(metadata={"syntax": "-J", "env": "SLURM_JOB_NAME"})
    workdir: str = opt_field(metadata={"syntax": "-D", "env": 'SLURM_SUBMIT_DIR'})

    wait: bool = field(default=False, metadata={"syntax": "-W", "env": "SBATCH_WAIT"})
    contiguous: bool = field(default=False, metadata={"syntax": "--contiguous"})
    perfparanoid: bool = field(default=False, metadata={"syntax": "-C perfparanoid"})
    exclusive: bool = field(default=True, metadata={"syntax": "--exclusive",
                                                    "env": "SBATCH_EXCLUSIVE"})

    @classmethod
    def from_env_file(cls, env_file: Path) -> "SlurmDirectives":
        kwargs = {}
        try:
            with open(env_file, encoding='utf-8') as f:
                lines = [line for line in f.readlines() if "SLURM_" in line
                         or "SBATCH_" in line]

            env_vals = {
                k: v.strip()
                for line in lines
                if "=" in line
                for k, v in [line.split("=", 1)]
            }

            for f_field in fields(cls):
                env = f_field.metadata.get("env")
                if env and env in env_vals:
                    kwargs[f_field.name] = env_vals[env]
        except OSError as e:
            print("While parsing", env_file, ":", e)

        return cls(**kwargs)

    def set_directive(self, directive, value):
        if directive in fields(self):
            setattr(self, directive, value)
        else:
            raise ValueError(f"Directive {directive} is not a valid directive")

    def __dir_val(self, directive: str) -> Any:
        return getattr(self, directive)

    def fmt_dirs(self) -> str:
        bool_dirs = [
            f"#SBATCH {f.metadata.get('syntax')}"
            for f in fields(self)
            if self.__dir_val(f.name) and isinstance(self.__dir_val(f.name), bool)
        ]

        dirs = [
            f"#SBATCH {f.metadata.get('syntax')} {self.__dir_val(f.name)}"
            for f in fields(self)
            if self.__dir_val(f.name) is not None and
            not isinstance(self.__dir_val(f.name), bool)
        ]

        return "\n".join(dirs + bool_dirs)

    def __str__(self):
        return "\n".join(
            [f"{f.metadata.get('syntax')} {self.__dir_val(f.name)}"
             for f in fields(self)]
        )


class SlurmScript(BashScript):
    BEGIN_SCRIPT = "# AUTOMATED SLURM SCRIPT WRAPPER GENERATION:"

    def __init__(self, script_path: Path, template_p: Optional[Path] = None) -> None:
        super().__init__(script_path, template_p)

        self.dirs = SlurmDirectives()
        self.slurm_job: Optional[int] = None
        self.slurm_env: Optional[str] = None

    def with_directives(self, directives: SlurmDirectives) -> "SlurmScript":
        self.dirs = directives
        return self

    def with_directive(self, directive, value: str) -> "SlurmScript":
        self.dirs.set_directive(directive, value)
        return self

    def with_slurm_env(self, env: str) -> "SlurmScript":
        self.slurm_env = env
        return self

    def _generate_script(self) -> None:
        content = "\n".join(
            [
                "#!/bin/bash",
                self.dirs.fmt_dirs(),
                "",
                self.BEGIN_SCRIPT,
                "",
                self._cmds_str(),
                "",
                self.TRAILER_SCRIPT,
                "",
            ]
        )

        self.s.write_text(content)
        self.s.chmod(self.s.stat().st_mode | stat.S_IXUSR)  # ADD EXEC RIGHTS
        self._ok("Generated slurm script @", self.s)

    def __env_fmt(self) -> str:
        if self.slurm_env is None:
            return ""
        return f"--export ALL,{self.slurm_env}"

    def run(self, cmd=None):
        self._info(f"Submitting SLURM script {self.s}")
        env = self.__env_fmt()
        if env:
            cmd = f"sbatch --parsable {env} {self.s.name}"
        else:
            cmd = f"sbatch --parsable {self.s.name}"
        super().run(cmd)
