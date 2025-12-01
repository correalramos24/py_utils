from bash import *

import os
from pathlib import Path

from unittest import TestCase


class TestBashCommand(TestCase):
    test_rundir = Path(__file__).parent
    print("Executing tests at", test_rundir)

    def test_err_bash_cmd(self):
        BashManager(rundir=self.test_rundir).run_output("alfa -hs")

    def test_ok_bash_cmd(self):
        r = BashManager(rundir=self.test_rundir).run_output("ls -la")
        print(r)

    def test_cmd_with_log(self):
        BashManager(rundir=self.test_rundir) \
        .with_log(Path(self.test_rundir, "log")) \
        .run("ls -la")


class TestBashScript(TestCase):
    test_rundir = Path(__file__).parent
    print("Executing tests at", test_rundir)

    def test_generate_script(self):
        b_dir = Path(self.test_rundir, "test_bash_script")
        BashScript(b_dir).with_cmds(["ls -la"]).run()

    def test_run_output(self):
        ...