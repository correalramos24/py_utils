import os, re, subprocess
from pathlib import Path
from textwrap import dedent
from typing import Optional

# =============================BASH VARS======================================

def expand_bash_env_vars(value:  str|list[str]) -> str|list[str] | None:
    """Convert the bash variables ($VAR or ${VAR}) to the value."""
    if isinstance(value, str):
          return os.path.expandvars(value) if "$" in value else None
    if isinstance(value, list) and any("$" in v for v in value):
          return [os.path.expandvars(v) for v in value]
    return None

# =============================BASH SCRIPTS====================================
def generate_bash_script(f_path: Path, cmds: list[str]):
    """Generate a bash script file with the given commands."""
    script_content = dedent(f"""\
        #!/bin/bash
        # AUTOMATED BASH WRAPPER GENERATION:

        {'\n'.join(cmds)}
    """)
    f_path.write_text(script_content)

def execute_script(script: str, args: str|None, rundir: Path, log_file=None) -> int:
    if not args: args = ""
    if not rundir: rundir = os.getcwd()

    file_desc = open(log_file, mode="w") if log_file else None
    r = subprocess.run(f"/bin/bash {script} {args}", cwd=rundir,
            shell=True, text=True,
            stderr=subprocess.STDOUT, stdout=file_desc)
    if log_file is not None:file_desc.close()

    return r.returncode

def execute_command(cmd: str, rundir: Path):
    subprocess.run(f"{cmd}", cwd=rundir,
            shell=True, text=True,
           stderr=subprocess.STDOUT)

def command_output(cmd: str, rundir: Optional[Path] = None):
    return execute_command_get_ouput(cmd, rundir)

def execute_command_get_ouput(cmd: str, rundir: Optional[Path] = None):
    try:
        if not rundir: rundir = Path(os.getcwd())
        ret = subprocess.check_output(
            cmd, cwd=rundir,
            stderr=subprocess.STDOUT,shell=True).strip().decode('utf-8')
        return ret
    except Exception as e:
        print(e)
        return "ERROR"
