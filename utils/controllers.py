from pathlib import Path
import pickle as pkl
from typing import Callable, Any
from abc import ABC, abstractmethod

from utils_files import create_dir, check_path_exists
from meta import MetaAbstractClass

# ================================BACKEND=======================================
class AbstractPersistance(MetaAbstractClass):
    def __init__(self, root_path: Path):
        self.root : Path = root_path
        self.meta : Path = Path(self.root, "meta.data")
        self.entities : dict[str, Any] = dict()

        if check_path_exists(root_path):
            self._info("INIT @", root_path)
            self._load_metadata()
            self._log("METADATA:", self.entities)
        else:
            self._info("NEW PERSISTANCE @", root_path)
            create_dir(self.root, False)
            self._save_metadata()

    #========================INTERFACE METHODS==================================
    @abstractmethod
    def store(self, content: Any, pers_id : str):
        pass

    @abstractmethod
    def load(self, pers_id: str):
        pass

    def exist(self, pers_id):
        return pers_id in self.entities

    def list_entities(self):
        return list(self.entities.keys())
    #==========================PRIVATE METHODS==================================
    def _load_metadata(self):
        with open(self.meta, "rb") as md_file:
            self.entities = pkl.load(md_file)

    def _save_metadata(self):
        with open(self.meta, "wb") as md_file:
            pkl.dump(self.entities, md_file)

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
        cmd : int = 0
        while cmd >= 0:
            cmd = self.__next_op()
            if cmd < 0: break
            if cmd > len(cmds): print("Invalid cmd:", cmd)
            else: self.get_callbacks()[cmds[cmd-1]]()
            print("-"*80)
        self._post_loop_txt()

    def _pre_loop_txt(self):
        self._info("Initializing CLI!")

    def _post_loop_txt(self):
        self._info("Finishing CLI")

    def __next_op(self) -> int:
        for i, cmd in enumerate(list(self.get_callbacks().keys())):
            print('>',i+1, cmd)
        try:
            return int(input("ENTER COMMAND: "))
        except (ValueError, KeyboardInterrupt):
            return 0

class AbstractDomain(MetaAbstractClass):
    def __init__(self, db_root : Path):
        self._info("Initializing domain...")
        self.instances : dict[str, Any] = dict()
        self.database  : AbstractPersistance = self.init_database(db_root)
        self._ok("DONE!")

    @abstractmethod
    def init_database(self, db_root=None) -> AbstractPersistance:
        pass

    @abstractmethod
    def _create_new_instance(self):
        """Create an empty domain instance"""
        pass

    def get_avail_instances(self) -> list[str]:
        return [instance for instance in self.database.list_entities()]

    def _get_instance(self, dom_id: str, create_if_missing=False):
        instance = self.instances.get(dom_id)
        if instance is not None:
            return instance
        else:
            self._dbg(dom_id, "not found in domain, checking database...")
            if self.database.exist(dom_id):
                self.instances[dom_id] = self.database.load(dom_id)
                return self.instances[dom_id]
            elif create_if_missing:
                self.instances[dom_id] = self._create_new_instance()
                self._dbg("CREATED new instance with", dom_id)
            else:
                raise Exception("Loading invalid entity", dom_id)
            return self.instances[dom_id]

    def _update_instance(self, dom_id : str, data: object, save=False):
        self._dbg("UPDATING", dom_id, "->", id(data))
        self.instances[dom_id] = data
        if save:
            return self._save_domain(dom_id)

    def _save_domain(self, dom_id) -> None:
        self._dbg(f"SAVE {dom_id} ({id(self.instances[dom_id])})")
        self.database.store(self.instances[dom_id], dom_id)
