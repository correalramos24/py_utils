
from pathlib import Path
from unittest import TestCase

from utils.bash_cmd import BashCmd
from utils.logger import MyLogger, LoggerLevels

class TestBashCmd(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        print("Executing tests at", self.p)
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)

    def tearDown(self):
        print("Removing files generated...")
        for pattern in ["*.sh", "*.log"]:
            for file in self.p.glob(pattern):
                file.unlink(missing_ok=True)

    def test_err_bash_cmd(self):
        r = BashCmd(rundir=self.p).run("alfa -hs")
        self.assertNotEqual(r.ret_code(), 0)

    def test_ok_bash_cmd(self):
        r = BashCmd(rundir=self.p).run("ls -la")
        print(r, r.ret_code(), r.output())

    def test_cmd_with_log(self):
        r = BashCmd(rundir=self.p) \
        .with_log(Path(self.p, "ls_cmd.log")) \
        .run("ls -la")
        print(r.ret_code())
