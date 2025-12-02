from utils.bashScript import *
from utils.logger import *

from pathlib import Path
from unittest import TestCase

class TestBashCmd(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        print("Executing tests at", self.p)
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)

    def tearDown(self):
        print("Removing files generated...")
        for pattern in ["*.sh", "*.log"]:
            for file in self.p.glob(pattern):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error removing {file}: {e}")

    def test_err_bash_cmd(self):
        r = BashCmd(rundir=self.p).run("alfa -hs")
        self.assertEqual(r.ret_code(), 127)

    def test_ok_bash_cmd(self):
        r = BashCmd(rundir=self.p).run("ls -la")
        print(r, r.ret_code(), r.output())

    def test_cmd_with_log(self):
        r = BashCmd(rundir=self.p) \
        .with_log(Path(self.p, "ls_cmd.log")) \
        .run("ls -la")
        print(r.ret_code())

