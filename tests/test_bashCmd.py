from bashScript import *
from logger import *
import os
from pathlib import Path

from unittest import TestCase


class TestBashCmd(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        print("Executing tests at", self.p)
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)

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

