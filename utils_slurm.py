from .utils_print import *
from pathlib import Path
import subprocess, re, os
from typing import Any, NamedTuple

slurm_syntax = {
    "nodes" : "-N",
    "mpi" : "--ntasks-per-node",
    "cpus" : "-c",
    "tasks" : "--ntasks",
    "account": "-A",
    "queue" : "--qos",
    "time_limit" : "--time",
    "wait" : "-W",
    "contiguous" : "--contiguous",
    "workdir" : "-D",
    "exclusive" : "--exclusive",
    "job_name" : "--job-name",
    "perfparanoid" :"-C perfparanoid"
}

def generate_slurm_script(f_path: Path, log_file: str,
                          slurm_directives: dict[str, Any],
                          cmds: list[str]):
    formatted_directives = ""
    for directive, val in slurm_directives.items():
        aux = directive.replace("slurm_","")
        if isinstance(val, bool):
            val = ""
        formatted_directives += f"#SBATCH {slurm_syntax[aux]} {val}\n"
    if log_file:
        formatted_directives += f"#SBATCH --output {log_file}"
    cmds_with_end_line = '\n'.join(cmds)
    with open(f_path, mode="w") as bash_file:
        bash_file.write(f"""#!/bin/bash
{formatted_directives}
# {"="*80}
# AUTOMATED SLURM SCRIPT WRAPPER GENERATION:\n
{cmds_with_end_line}
# {"="*80}
""")
        log(f"Created", f_path)

def execute_slurm_script(script, args, rundir, env=None):
    if args:
        args_str = "with " + args
    else:
        args = ""
        args_str = "without args"

    info(f"Submitting {script} {args_str} at {rundir}")
    if env:
        info(f"Using env str", env)
        env = f"--export ALL,{env}"
    else:
        env = ""
    submission_str = f"sbatch --parsable {env} {script} {args}"
    print("Submitting", submission_str)
    subprocess.run(submission_str, cwd=rundir,
            shell=True, text=True, stderr=subprocess.STDOUT)

class SlurmEnv(NamedTuple):
    nodes: int
    mpi: int
    omp: int
    tasks: int

def slurm_env(env_file: Path) -> SlurmEnv:
    text = env_file.read_text()

    def find(pattern: str) -> int:
        return int(m.group(1)) if (m := re.search(pattern, text)) else -1

    return SlurmEnv(
        find(r"SLURM_NNODES=(\d+)"),
        find(r"SLURM_TASKS_PER_NODE=(\d+)"),
        find(r"SLURM_CPUS_PER_TASK=(\d+)"),
        find(r"SLURM_NTASKS=(\d+)")
    )

def get_slurm_env(env_file: Path) -> tuple[int,int,int,int]:
    regex_num_nodes = re.compile(r'SLURM_NNODES=(\d+)')
    regex_mpi_per_node = re.compile(r'SLURM_TASKS_PER_NODE=(\d+)')
    regex_tasks        = re.compile(r'SLURM_NTASKS=(\d+)')
    regex_omp_per_node = re.compile(r'SLURM_CPUS_PER_TASK=(\d+)')

    nodes, mpi, omp, tasks = -1,-1,-1,-1
    try:
        with open(env_file) as slurm_env_file:
            for line in slurm_env_file.readlines():
                match_nodes = regex_num_nodes.search(line)
                match_mpi_per_node = regex_mpi_per_node.search(line)
                match_omp_per_node = regex_omp_per_node.search(line)
                match_tasks        = regex_tasks.search(line)
                if match_nodes:
                    nodes = int(match_nodes.group(1))
                if match_mpi_per_node:
                    mpi = int(match_mpi_per_node.group(1))
                if match_omp_per_node:
                    omp = int(match_omp_per_node.group(1))
                if match_tasks:
                    tasks = int(match_tasks.group(1))
    except Exception as e:
        print(e)
    finally:
        return nodes, mpi, omp, tasks