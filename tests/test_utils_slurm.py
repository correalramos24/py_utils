
from pathlib import Path
from unittest import TestCase

from utils.slurm import SlurmDirectives
from utils.logger import MyLogger, LoggerLevels
from utils.slurm import SlurmScript

class TestSlurmScript(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        self.test_directives = {
            "account" : "test_acct",
            "nodes" : 3, "mpi" : 112,
            "omp" : 1, "exclusive" : True,
        }
        print("Executing tests at", self.p)
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)

    def tearDown(self):
        print("Removing files generated...")
        for pattern in ["*.sh", "*.log", "*.slurm"]:
            for file in self.p.glob(pattern):
                file.unlink(missing_ok=True)

    def test_parse_slurm_env(self):
        f = self.p / "env.log"
        a = SlurmDirectives.from_env_file(f)
        print(a)

    def test_slurm_script(self):
        aux = SlurmDirectives(**self.test_directives)
        (SlurmScript(Path(self.p, "test.slurm")).
        with_directives(aux).
        with_cmds("ls -la").dry())


    def test_slurm_submission(self):
        aux = SlurmDirectives(**self.test_directives)
        (SlurmScript(Path(self.p, "test_submit.slurm")).
         with_directives(aux).
         with_cmds("ls -la").run())

    def test_slurmDirectives(self):
        a = SlurmDirectives(**self.test_directives)

        print("Formatting directives:")
        print(a.fmt_dirs())
        print(a)