
from typing import Callable
from abc import abstractmethod

from meta import MetaAbstractClass


# ================================FRONTEND======================================
class AbstractFrontend(MetaAbstractClass):
    @abstractmethod
    def loop(self):
        pass


class AbstractCLI(AbstractFrontend):
    @abstractmethod
    def get_callbacks(self) -> dict[str, Callable]:
        pass

    def loop(self):
        self._pre_loop_txt()
        cmds = list(self.get_callbacks().keys())
        cmd: int = 0
        while cmd >= 0:
            cmd = self.__next_op()
            if cmd < 0:
                break
            if cmd > len(cmds):
                print("Invalid cmd:", cmd)
            else:
                self.get_callbacks()[cmds[cmd-1]]()
            print("-" * 80)
        self._post_loop_txt()

    def _pre_loop_txt(self):
        self._info("Initializing CLI!")

    def _post_loop_txt(self):
        self._info("Finishing CLI")

    def __next_op(self) -> int:
        for i, cmd in enumerate(list(self.get_callbacks().keys())):
            print('>', i + 1, cmd)
        try:
            return int(input("ENTER COMMAND: "))
        except (ValueError, KeyboardInterrupt):
            return 0
