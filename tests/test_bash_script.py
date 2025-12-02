
from unittest import TestCase
from pathlib import Path

from utils.bash_script import BashScript
from utils.logger import LoggerLevels, MyLogger
from utils.utils_files import ExpectFile, file_exists


class TestBashScript(TestCase):
    def setUp(self):
        self.p = Path(__file__).parent
        MyLogger.set_verbose_level(LoggerLevels.VERBOSE)
        print("Executing tests at", self.p)

    def tearDown(self):
        print("Removing files generated...")
        for pattern in ["*.sh", "*.log"]:
            for file in self.p.glob(pattern):
                file.unlink(missing_ok=True)


    def test_generate_dry_script(self):
        b_dir = Path(self.p, "test_dry.sh")
        a = BashScript(b_dir).with_cmds(["ls -la", "du -hs"])
        a.dry()

    def test_generate_bad_script(self):
        with self.assertRaises(ExpectFile):
            b_dir = Path(self.p)
            a = BashScript(b_dir).with_cmds(["ls -la", "du -hs"])
            a.dry()

    def test_run(self):
        b_dir = Path(self.p, "test_run.sh")
        rc = (BashScript(b_dir).with_cmds(["ls -la", "echo \"Disk usage:\"",  "du -hs"]).
              run().ret_code())
        self.assertEqual(rc, 0)

    def test_run_with_log(self):
        b_dir = Path(self.p, "test_run_with_log.sh")
        rc = (BashScript(b_dir).with_cmds(["ls -la", "echo \"Disk usage:\"",  "du -hs"])
              .with_log(Path(self.p, "l.log")).run().ret_code())
        self.assertEqual(rc, 0)
        self.assertTrue(file_exists(Path(self.p, "test_run_with_log.sh")))

    def test_run_gather_output(self):
        b_dir = Path(self.p, "test_run_with_output.sh")
        ret = (BashScript(b_dir).with_cmds(["du -hs"])
              .run().output())
        print("output:", ret)
